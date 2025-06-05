import os, requests as req, sys, time
sys.path.append("packages/rag/rag")

def test_vdb_int():
    vdb = os.environ.get("OPSDEV_HOST") + "/api/my/rag/rag"
    
    args = {"drop_collection": "test"}
    res = req.post(vdb, json=args).json()
    assert res.get("output").startswith("\nStart with")

    args = {"input": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHb4BkgDyZmbZLwhPymQwud_H7m8gevoO4_Q&s"}
    res = req.post(vdb, json=args).json()
    res.get("output").startswith("OK:")
    
    args = {"input": "*image"}
    # retry a few tims for timing issues
    for i in range(0, 10):
        out = req.post(vdb, json=args).json().get("output")
        assert out != -1
        
    assert out.count("image") >= 1

import bucket
def test_bucket():
    inp = "test"
    buck = bucket.Bucket({})

    #Check is the record exists. If it does not, it creates a new one
    record = buck.exturl(inp, 3600)
    if record:
        record = buck.write(inp, "This is a test example")
        assert "OK" in record
    else: assert "http://minio:9000/" in record


import rag
#Sometimes the test returns error because of a faulty initialization of VectorDB (unexpected keyword "shorten")
def test_rag_int():
    args = {"input": "test"}
    time.sleep(1)
    rag_ = rag.rag(args)
    assert rag_["output"] != -1