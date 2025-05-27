import re, os, requests as req
#MODEL = "llama3.1:8b"
MODEL = "phi4:14b"

def chat(args, inp):
  host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
  auth = args.get("AUTH", os.getenv("AUTH"))
  url = f"https://{auth}@{host}/api/generate"
  msg = { "model": MODEL, "prompt": inp, "stream": False}
  res = req.post(url, json=msg).json()
  out = res.get("response", "error")
  return  out
 
def extract_fen(out):
  print("activated fen method")
  pattern = r"([rnbqkpRNBQKP1-8]+\/){7}[rnbqkpRNBQKP1-8]+"
  fen = None
  m = re.search(pattern, out, re.MULTILINE)
  if m:
    fen = m.group(0)
  return fen

def puzzle(args):
  out = "If you want to see a chess puzzle, type 'puzzle'. To display a fen position, type 'fen <fen string>'."
  inp = args.get("input", "")
  res = {}
  if inp == "puzzle":
    res["form"] = [
        {"name": "rook", "label": "With a rook", "type": "checkbox", "required": "false"},
        {"name": "queen", "label": "With a queen", "type": "checkbox", "required": "false"},
        {"name": "knight", "label": "With a knight", "type": "checkbox", "required": "false"},
        {"name": "bishop", "label": "With a bishop", "type": "checkbox", "required": "false"},
    ]

  elif "form" in inp:
    form = inp["form"]
    inp = "generate a chess puzzle in FEN format"

    for field in form.keys():
      if form[field]:
        inp += f", include at least a ${field}"
      else:
        inp += f", exclude the ${field}s"

    out = chat(args, inp)
    fen = extract_fen(out)
    if fen:
       print(fen)
       res['chess'] = fen
    else:
      out = "Bad FEN position."

  elif inp.startswith("fen"):
    fen = extract_fen(inp)
    if fen:
       out = "Here you go."
       res['chess'] = fen
  elif inp != "":
    out = chat(args, inp)
    fen = extract_fen(out)
    print(out, fen)
    if fen:
      res['chess'] = fen

  res["output"] = out
  return res
