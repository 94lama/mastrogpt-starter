import vdb, vision, base64

USAGE = f"""Welcome to the Vector DB Loader.
Write text to insert in the DB. 
Use `@[<coll>]` to select/create a collection and show the collections.
Use `*<string>` to vector search the <string>  in the DB.
Use `#<limit>`  to change the limit of searches.
Use `!<substr>` to remove text with `<substr>` in collection.
Use `!![<collection>]` to remove `<collection>` (default current) and switch to default.
"""

def verify_secured_url(url):
  return url.startswith("https://")

def get_image(url):
  if verify_secured_url(url):
    import requests
    res = requests.get(url)
    if res.status_code > 299:
      print(f"Error {res.status_code} while trying to open the URL")
      return False
    else:
      print("The URL parsed is valid, opening the image...")
      return res


def loader(args):
  print(args)
  # get state: <collection>[:<limit>]
  collection = "img" #If not present, creating a new colection will authomatically set the correct parameters
  limit = 30
  sp = args.get("state", "").split(":")
  if len(sp) > 0 and len(sp[0]) > 0:
    collection = sp[0]
  if len(sp) > 1:
    try:
      limit = int(sp[1])
    except: pass
  print(collection, limit)

  db = vdb.VectorDB(args, collection)
  inp = str(args.get('input', ""))
  response = {}
  response["output"] = f"{USAGE}Current collection is {collection} with limit {limit}"
  response["collection"] = f"{collection}:{limit}"

  # select collection
  if inp.startswith("@"):
    response["output"] = ""
    if len(inp) > 1:
       collection = inp[1:]
       response["output"] = f"Switched to {collection}.\n"
    response["output"] += db.setup(collection)
  # set size of search
  elif inp.startswith("#"):
    try: 
       limit = int(inp[1:])
    except: pass
    response["output"] = f"Search limit is now {limit}.\n"
  # run a query
  elif inp.startswith("*"):
    search = inp[1:]
    if search == "":
      search = " "
    res = db.vector_search(search, limit=limit)
    if len(res) > 0:
      response["output"] = f"Found:\n"
      for i in res:
        response["output"] += f"({i[0]:.2f}) {i[1]}\n"
    else:
      response["output"] = "Not found"
  # remove a collection
  elif inp.startswith("!!"):
    if len(inp) > 2:
      collection = inp[2:].strip()
    response["output"] = db.destroy(collection)
    collection = "default"
  # remove content
  elif inp.startswith("!"):
    count = db.remove_by_substring(inp[1:])
    response["output"] = f"Deleted {count} records."    
  elif inp != '':
    response["output"] = "Inserted "
    img = get_image(inp)
    if not inp: return {"output": "The input is not valid", "state": f"{collection}:{limit}"}

    import bucket, datetime
    buck = bucket.Bucket(args)
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    key = f"rag/{timestamp}"
    decoded_img = base64.b64encode(img.content)
    vis = vision.Vision(args)
    response["output"] = vis.decode(decoded_img)
    buck.write(key, decoded_img)
    db.insert(response["output"], key)
    if decoded_img:
       response["html"] = f"<img src='data:image/png;base64,{decoded_img.decode("utf-8")}'>"

  return response