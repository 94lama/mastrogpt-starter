import vdb

USAGE = f"""Welcome to the Vector DB Loader.
Write text to insert in the DB.
Start with * to do a vector search in the DB.
Start with ! to remove text with a substring.
"""

def load(args):

  collection = args.get("COLLECTION", "default")
  out = f"{USAGE}Current colletion is {collection}"
  inp = str(args.get('input', ""))
  db = vdb.VectorDB(args)
  
  if inp.startswith("*"):
    if len(inp) == 1:
      out ="please specify a search string"
    else:
      res = db.vector_search(inp[1:])
      if len(res) > 0:
        out = f"Found:\n"
        for i in res:
          out += f"({i[0]:.2f}) {i[1]}\n"
      else:
        out = "Not found"
  elif inp.startswith("!"):
    count = db.remove_by_substring(inp[1:])
    out = f"Deleted {count} records."
  elif inp != '':
    if inp.startswith("https://"):
      import requests
      from bs4 import BeautifulSoup as bs
      res = requests.get(inp)

      if res.status_code > 299:
        print(res)
        return {"output": "Ops, something went wrong!"}
      else:
        res = bs(res.text, 'html.parser').get_text()
        res = tokenize(res)
        out = f"Website content added to the database:\n"
        for i in res:
            out += f"{i}\n"

    elif inp.startswith("http://"):
      return {"output": "The URL you requested is not secure!"}
          
    res = db.insert(inp)
    out = "Inserted " 
    out += " ".join([str(x) for x in res.get("ids", [])])

  return {"output": out}
  

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