import sys

def strip_line(line):
    line = line.strip(' \r\n')
    if len(line) > 0:
        comment = line.rfind('//')
        if comment >= 0:
            line = line[:comment].strip(' \r\n')
    return line

def main(argv):
    with open(argv[1]) as f:
        for line in f:
            s = strip_line(line)
            if len(s) > 0:
                print(s)

    idx = argv[1].find('.vm')
    if idx >= 0:
        asm_file = argv[1][:idx] + ".asm"
        print("\noutput file: " + asm_file)

if __name__ == "__main__":
    main(sys.argv)
