import vdb, vision, base64

USAGE = f"""Welcome to the Vector DB Loader.
Write text to insert in the DB. 
Use `@[<coll>]` to select/create a collection and show the collections.
Use `*<string>` to vector search the <string>  in the DB.
Use `#<limit>`  to change the limit of searches.
Use `!<substr>` to remove text with `<substr>` in collection.
Use `!![<collection>]` to remove `<collection>` (default current) and switch to default.
"""

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

  out = f"{USAGE}Current collection is {collection} with limit {limit}"
  db = vdb.VectorDB(args, collection)
  inp = str(args.get('input', ""))

  # select collection
  if inp.startswith("@"):
    out = ""
    if len(inp) > 1:
       collection = inp[1:]
       out = f"Switched to {collection}.\n"
    out += db.setup(collection)
  # set size of search
  elif inp.startswith("#"):
    try: 
       limit = int(inp[1:])
    except: pass
    out = f"Search limit is now {limit}.\n"
  # run a query
  elif inp.startswith("*"):
    search = inp[1:]
    if search == "":
      search = " "
    res = db.vector_search(search, limit=limit)
    if len(res) > 0:
      out = f"Found:\n"
      for i in res:
        out += f"({i[0]:.2f}) {i[1]}\n"
    else:
      out = "Not found"
  # remove a collection
  elif inp.startswith("!!"):
    if len(inp) > 2:
      collection = inp[2:].strip()
    out = db.destroy(collection)
    collection = "default"
  # remove content
  elif inp.startswith("!"):
    count = db.remove_by_substring(inp[1:])
    out = f"Deleted {count} records."    
  elif inp != '':
    out = "Inserted "
    img = get_image(inp)

    if not inp: return {"output": "The input is not valid", "state": f"{collection}:{limit}"}

    vis = vision.Vision(args)
    out = vis.decode(base64.b64encode(img.content).decode())
    db.insert(out, inp)

  return {"output": out, "state": f"{collection}:{limit}"}
  

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

def tokenize(text):
    import re
    tokens = text.split()
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        if re.match(r'\d{1,2}[/-]\d{1,2}[/-]\d{4}', token):
            pass
        elif re.match(r"\w+'s", token):
            token = re.sub(r"(\w+)'s", r"\1 's", token)
        elif re.match(r"\w+'\w+", token):
            token = token.replace("'", "")
        elif re.match(r"\w+-\w+", token):
            pass
        elif re.match(r"\d+(,\d+)*", token):
            pass
        else:
            token = re.sub(r"([^\w\s]+)", r" \1 ", token)
        
        token = re.sub(r"(\w+)\.", r"\1", token)
        token = re.sub(r"(\w+),", r"\1", token)
        token = re.sub(r"U\.S\.A\.", r"U.S.A.", token)
        
        tokens[i] = token
        i += 1
    
    return tokens