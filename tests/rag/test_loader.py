import os, requests as req, sys, time
sys.path.append("packages/rag/loader")

def test_vdb_int():
    vdb = os.environ.get("OPSDEV_HOST") + "/api/my/rag/loader"
    
    args = {"drop_collection": "test"}
    res = req.post(vdb, json=args).json()
    assert res.get("output").startswith("Welcome to the Vector DB Loader.")

    args = {"input": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHb4BkgDyZmbZLwhPymQwud_H7m8gevoO4_Q&s"}
    res = req.post(vdb, json=args).json()
    res.get("output").startswith("OK:")
    
    time.sleep(1)
    args = {"input": "*"}
    out = req.post(vdb, json=args).json().get("output")
    time.sleep(1)
    assert out.startswith("Found")
        
    assert out.count("image") >= 1
    
    args = {"input": "!"}
    res = req.post(vdb, json=args).json()
    assert res.get("output").find("Deleted") != -1

import vdb
#Sometimes the test returns error because of a faulty import (VectorDB)
def test_vdb():
    args = {"drop_collection": "test"}
    db = vdb.VectorDB(args, "default")

    db_list = db.destroy("test")
    assert "Dropped" in db_list

    db_list = db.setup("test")
    assert "test" in db_list

    assert len(db.embed("hello world")) == 1024
    assert len(db.vector_search("hello")) != -1

    db.insert("This is a test item", "rag/20250605083546")
    time.sleep(1)

    test = db.vector_search("screen")
    dblen = len(test)
    assert dblen != -1
    assert test[0][1] != -1

    assert db.remove_by_substring("screen") == dblen-1

import vision, base64
def test_vision_int():
    img = req.get("https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png") #placeholder image
    img = base64.b64encode(img.content)
    vis = vision.Vision({})
    res = vis.decode(img)
    assert res != -1

import bucket
def test_bucket():
    inp = "test"
    buck = bucket.Bucket({})
    record = buck.write(inp, "This is a test example")
    assert "OK" in record

    fake_record = buck.read("Does not exists")
    assert fake_record == ""
    record = buck.read(inp)
    assert record == b"This is a test example"

    record = buck.exturl(inp, 3600)
    assert "http://minio:9000/" in record

    size = buck.size(inp)
    assert size > 0

    record = buck.find("te")
    assert record[0] == "test"

    record = buck.remove(inp)
    assert record != -1

import loader
def test_loader():
    args = {}
    assert loader.verify_secured_url("https://google.com") == True
    assert loader.verify_secured_url("http://google.com") == False
    assert loader.get_image("https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png") != -1

#Sometimes the test returns error because of a faulty import (VectorDB)
def test_loader_int():
    args = {"input": "@test"}
    load = loader.loader(args)

    args = {"input": "#2"}
    load = loader.loader(args)
    assert "Search limit is now 2.\n" == load["output"]

    args = {"input": "https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png"}
    load = loader.loader(args)
    assert "<img src='data:image/png;base64," in load["html"]
    assert load["output"] != -1

    args = {"input": "!"}
    load = loader.loader(args)
    assert "Deleted" in load["output"]

    args = {"input": "!!test"}
    load = loader.loader(args)
    assert "Dropped test" in load["output"]
    
    args = {"input": ""}
    load = loader.loader(args)
    assert "Welcome to the Vector DB Loader.\nWrite text to insert in the DB." in load["output"]

    
