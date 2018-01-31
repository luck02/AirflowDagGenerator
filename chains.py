# consume files starting at root
#   Descend through
import sys
import tokenize

def printComments(path: str) -> None:
    fileObj = open(path, 'r')
    for token in tokenize.generate_tokens(fileObj.readline):
        # we can also use token.tok_name[toktype] instead of 'COMMENT'
        # from the token module

        if token.type == tokenize.COMMENT:
            print(f'comment:{token}')


def main(root):
    print(root);
    printComments(root[1])

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print(f'I need to see a root to start processing: {sys.argv}')
        exit(1)
    main(sys.argv)
