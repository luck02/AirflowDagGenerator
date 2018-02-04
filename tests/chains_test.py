from chains import chains
import io

def extract_chains():
    doc = """
# generic comment
#@chains:name
some python code etc etc.
    """
    stream = io.StringIO(doc)
    comments = chains.extractComments(stream)
    print(comments)
    assert(len(comments) == 1)

    assert(comments[0] == "#@chains:name\n")
