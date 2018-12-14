from datetime import datetime
from vmt.command import Command

"""
0–15 Sixteen virtual registers, usage described below
16–255 Static variables (of all the VM functions in the VM program)
256–2047 Stack
2048–16483 Heap (used to store objects and arrays)
16384–24575 Memory mapped I/O
"""

VM_TRUE = 0xffff
VM_FALSE = 0x0000


def write_comment(f):
    f.write("// Generated {:%B %d, %Y %I:%M:%S%p}\n".format(datetime.now()))


def write_push(f, command):
    line_count = 0
    f.write("// write_push\n")
    if command["arg1"] == "constant":
        f.write("@" + command["arg2"] + "\n")
        f.write("D=A\n")
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("M=D\n")
        f.write("@SP\n")
        f.write("M=M+1\n")
        line_count = 7
    else:
        raise NotImplementedError("segment unsupported")
    return line_count


def write_pop(f, command):
    f.write("// write_pop\n")
    return 1


def write_arithmetic(f, command, label_suffix):
    f.write("// write_" + command["arg1"] + "\n")
    if command["arg1"] == "add":
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("D=M\n")
        f.write("A=A-1\n")
        f.write("D=M+D\n")
        f.write("M=D\n")
        f.write("@SP\n")
        f.write("M=M-1\n")
    elif command["arg1"] == "sub":
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("D=M\n")
        f.write("A=A-1\n")
        f.write("D=M-D\n")
        f.write("M=D\n")
        f.write("@SP\n")
        f.write("M=M-1\n")
    elif command["arg1"] == "neg":
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("M=-M\n")
    elif command["arg1"] == "eq":
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("D=M\n")
        f.write("A=A-1\n")
        f.write("D=M-D\n")
        f.write("@IsEq" + label_suffix + "\n")
        f.write("D;JEQ\n")
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("A=A-1\n")
        f.write("M=0\n")
        f.write("@End" + label_suffix + "\n")
        f.write("0;JMP\n")
        f.write("(IsEq" + label_suffix + ")\n")
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("A=A-1\n")
        f.write("M=-1\n")
        f.write("(End" + label_suffix + ")\n")
        f.write("@SP\n")
        f.write("M=M-1\n")
    elif command["arg1"] == "gt":
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("D=M\n")
        f.write("A=A-1\n")
        f.write("D=M-D\n")
        f.write("@IsGt" + label_suffix + "\n")
        f.write("D;JGT\n")
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("A=A-1\n")
        f.write("M=0\n")
        f.write("@End" + label_suffix + "\n")
        f.write("0;JMP\n")
        f.write("(IsGt" + label_suffix + ")\n")
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("A=A-1\n")
        f.write("M=-1\n")
        f.write("(End" + label_suffix + ")\n")
        f.write("@SP\n")
        f.write("M=M-1\n")
    elif command["arg1"] == "lt":
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("D=M\n")
        f.write("A=A-1\n")
        f.write("D=M-D\n")
        f.write("@IsLt" + label_suffix + "\n")
        f.write("D;JLT\n")
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("A=A-1\n")
        f.write("M=0\n")
        f.write("@End" + label_suffix + "\n")
        f.write("0;JMP\n")
        f.write("(IsLt" + label_suffix + ")\n")
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("A=A-1\n")
        f.write("M=-1\n")
        f.write("(End" + label_suffix + ")\n")
        f.write("@SP\n")
        f.write("M=M-1\n")
    elif command["arg1"] == "and":
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("D=M\n")
        f.write("A=A-1\n")
        f.write("D=M&D\n")
        f.write("M=D\n")
        f.write("@SP\n")
        f.write("M=M-1\n")
    elif command["arg1"] == "or":
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("D=M\n")
        f.write("A=A-1\n")
        f.write("D=M|D\n")
        f.write("M=D\n")
        f.write("@SP\n")
        f.write("M=M-1\n")
    elif command["arg1"] == "not":
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("M=!M\n")
    else:
        raise ValueError("unrecognized arithmetic command")
    return 1


def write_file(filename, commands):
    idx = filename.find('.vm')
    if idx >= 0:
        asm_file = filename[:idx] + ".asm"
        line_count = 0
        with open(asm_file, mode='w') as f:
            write_comment(f)
            line_count += 1
            j = 1
            for c in commands:
                if c["command_type"] == Command.POP:
                    line_count += write_pop(f, c)
                elif c["command_type"] == Command.PUSH:
                    line_count += write_push(f, c)
                elif c["command_type"] == Command.ARITHMETIC:
                    label_suffix = format(int(j), 'd').zfill(3)
                    line_count += write_arithmetic(f, c, label_suffix)
                    j += 1

        print("Wrote (" + str(line_count) + ") lines to " + asm_file)
