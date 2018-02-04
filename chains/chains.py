# consume files starting at root
#   Descend through
import sys
import tokenize
import io

def extractComments(stream: io.TextIOBase) -> []:
    comments=[]
    for token in tokenize.generate_tokens(stream.readline):
        # we can also use token.tok_name[toktype] instead of 'COMMENT'
        # from the token module

        if token.type == tokenize.COMMENT:
            if "@chains" in token.line:
                comments.append(token.line)

    return comments



def process(path: str):
    comments = extractComments(path)

def main(args):
    if (len(sys.argv) != 2):
        print(f'I need to see a root to start processing: {sys.argv}')
        exit(1)
    process(args[1])

if __name__ == "__main__":
    main(sys.argv)
