import sys 
sys.path.append("packages/msciab/reverse")
import reverse

def test_reverse():
    res = reverse.reverse({})
    assert res["output"] == "reverse"

    args = {"input": "Ciao"}
    res = reverse.reverse(args)
    assert res["output"] == "oaiC"
