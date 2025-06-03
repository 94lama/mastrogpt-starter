import os, requests as req
import vision2 as vision
import bucket

USAGE = "Please upload a picture and I will tell you what I see"
FORM = [
  {
    "label": "Load Image",
    "name": "pic",
    "required": "true",
    "type": "file"
  },
]

def form(args):
  res = {}
  out = USAGE
  inp = args.get("input", "")

  if type(inp) is dict and "form" in inp:
    import base64
    buck = bucket.Bucket(args)
    img = inp.get("form", {}).get("pic", "")
    encoded_img = base64.b64decode(img)
    print(f"uploaded size {len(img)}")
    print("img: ", encoded_img)
    store_img(buck, encoded_img)
    vis = vision.Vision(args)
    out = vis.decode(img)
    res['html'] = f'<img src="data:image/png;base64,{img}">'
    
  res['form'] = FORM
  res['output'] = out
  return res

def store_img(buck, img):
  import datetime
  print("Storing the image in the bucket...")

  time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
  path = "form/"
  key=f"{path}{time}"
  res = buck.write(key, img)
  if res != "OK": return res
  return buck.exturl(key, 3600)