import os, requests as req, re

def test_load_int():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/vdb/load"

    inputs = [
        {"input": "*", "response": "^please specify a search string$"}, # Populate db
        {"input": "https://google.com/404", "response": "^Ops, something went wrong!$"}, # 404 Erorr management
        {"input": "https://google.com", "response": "^Inserted"}, # Populate with website requests
        {"input": "http://google.com", "response": "^The URL you requested is not secure!$"}, # Block HTTP requests
        {"input": "!https://google.com", "response": "^Deleted [\d]+ records\.$"}, # Deletes records
    ]
    
    for inp in inputs:
        args = {"input": inp["input"]}
        res = req.post(url, json=args).json()
        print(res)
        assert re.match(inp["response"], res["output"])
