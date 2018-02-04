# consume files starting at root
#   Descend through
import sys
import tokenize
import io
import pprint

class Token:
    """struct for tokeniziation"""
    def __init__(self, raw: str):
        self._raw = raw
        self.__tokenize()



    def __tokenize(self):
        """simplistic positional parser.
        Replace with actual parser that consumes tokens and results in a parse tree.
            @chains
                :type
                    :metadata
                    positional metadata is important.
            if type== task
                value can be name, compute.ram, compute.cpu etc.

        """
        self._type = self.type()
        self._target = self.target()


    def type(self):
        return self._raw.split(":")[1]


    def target(self):
        return self._raw.split(":")[2]


    def __str__(self):
        return pprint.pprint(vars(self))


def extract_comments(stream: io.TextIOBase) -> []:
    comments = []
    for token in tokenize.generate_tokens(stream.readline):
        # we can also use token.tok_name[toktype] instead of 'COMMENT'
        # from the token module

        if token.type == tokenize.COMMENT:
            if "@chains" in token.line:
                comments.append(token.line)

    return comments

def parse_chains(stream: io.TextIOBase) -> []:
    return None

# def process(path: str):
#     comments = extract_comments(path)
#
# def main(args):
#     if (len(sys.argv) != 2):
#         print(f'I need to see a root to start processing: {sys.argv}')
#         exit(1)
#     process(args[1])
#
# if __name__ == "__main__":
#     main(sys.argv)
