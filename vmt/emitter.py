from datetime import datetime
from vmt.command import Command

"""
0–15 Sixteen virtual registers, usage described below
16–255 Static variables (of all the VM functions in the VM program)
256–2047 Stack
2048–16483 Heap (used to store objects and arrays)
16384–24575 Memory mapped I/O
"""

STACK_BEGIN = 256
stack_pointer = STACK_BEGIN


def write_comment(f):
    f.write("// Generated {:%B %d, %Y %I:%M:%S%p}\n".format(datetime.now()))


def write_push(f, command):
    line_count = 1
    f.write("// write_push\n")
    if command["arg1"] == "constant":
        f.write("@256\n")
        f.write("D=A\n")
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("D=D+A\n")
        f.write("@R13\n")
        f.write("M=D\n")
        f.write("@" + command["arg2"] + "\n")
        f.write("D=A\n")
        f.write("@R13\n")
        f.write("A=M\n")
        f.write("M=D\n")
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A+1\n")
        f.write("D=A\n")
        f.write("@SP\n")
        f.write("M=D\n")
        line_count = 18
    else:
        raise NotImplementedError("segment unsupported")
    return line_count


def write_pop(f, command):
    f.write("// write_pop\n")
    return 1


def write_arithmetic(f, command):
    f.write("// write_arithmetic\n")
    return 1


def write_file(filename, commands):
    idx = filename.find('.vm')
    if idx >= 0:
        asm_file = filename[:idx] + ".asm"
        line_count = 0
        with open(asm_file, mode='w') as f:
            write_comment(f)
            line_count += 1
            for c in commands:
                if c["command_type"] == Command.POP:
                    line_count += write_pop(f, c)
                elif c["command_type"] == Command.PUSH:
                    line_count += write_push(f, c)
                elif c["command_type"] == Command.ARITHMETIC:
                    line_count += write_arithmetic(f, c)
        print("Wrote (" + str(line_count) + ") lines to " + asm_file)
