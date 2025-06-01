import os, requests as req
import vision2 as vision
import sys

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
  buck = open_bucket(args)

  if type(inp) is dict and "form" in inp:
    img = inp.get("form", {}).get("pic", "")
    print(f"uploaded size {len(img)}")
    vis = vision.Vision(args)
    img = store_img(buck, img)
    out = vis.decode(img)
    res['html'] = f'<img src="data:image/png;base64,{img}">'
    
  res['form'] = FORM
  res['output'] = out
  return res

def open_bucket(args):
  print("Linking with your bucket...")
  import bucket
  return bucket.Bucket(args)

def store_img(buck, img):
  import datetime
  print("Storing the image in the bucket...")

  time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
  path = "form/"
  key=f"{path}{time}"
  res = buck.write(key, img)
  if res != "OK": return res

  return buck.exturl(key, 3600)