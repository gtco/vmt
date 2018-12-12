import sys

from vmt import parser, emitter


def main(argv):
    parser.load_file(argv[1])
    emitter.write_file(argv[1], parser.get_commands())


if __name__ == "__main__":
    main(sys.argv)
