from chains import chains
import io

def test_extract_chains():
    doc = """
# generic comment
#@chains:name
some python code etc etc.
    """
    stream = io.StringIO(doc)
    chain = chains.extract_comments(stream)
    print(type(chain))
    assert(len(chain) == 1)

    assert(chain[0] == "#@chains:name\n")

def test_parse_chain():
    doc = """
#@chains:task:name:some_name
    """

    token = chains.Token(doc)

    print(token)
    assert(False)
