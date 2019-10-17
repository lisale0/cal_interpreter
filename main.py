import sys
from scanner import Scanner


def run_file():
    return


def run_prompt():
    while True:
        line = input(">> ")
        run(line)


def run(line):
    scanner = Scanner(line)
    scanner.scan_tokens()



def main():
    if len(sys.argv) > 2:
        print("Usage: [script]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        run_file(sys.argv[0])
    else:
        run_prompt()


if __name__ == "__main__":
    main()

