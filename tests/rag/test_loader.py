import os, requests as req, sys, time
def test_vdb_int():
    vdb = os.environ.get("OPSDEV_HOST") + "/api/my/rag/loader"
    
    args = {"drop_collection": "test"}
    res = req.post(vdb, json=args).json()
    assert res.get("output").startswith("Welcome to the Vector DB Loader.")

    args = {"input": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHb4BkgDyZmbZLwhPymQwud_H7m8gevoO4_Q&s"}
    res = req.post(vdb, json=args).json()
    res.get("output").startswith("OK:")
    
    args = {"input": "*image"}
    # retry a few tims for timing issues
    for i in range(0, 10):
        out = req.post(vdb, json=args).json().get("output")
        assert out.startswith("Found")
        
    assert out.count("image") >= 1
    
    args = {"input": "!"}
    res = req.post(vdb, json=args).json()
    assert res.get("output").find("Deleted") != -1

sys.path.append("packages/rag/loader")
import vdb
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

