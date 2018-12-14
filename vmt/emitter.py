from datetime import datetime
from vmt.command import Command

"""
0–15 Sixteen virtual registers, usage described below
16–255 Static variables (of all the VM functions in the VM program)
256–2047 Stack
2048–16483 Heap (used to store objects and arrays)
16384–24575 Memory mapped I/O
"""


assembly_name = ""


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
    elif command["arg1"] == "local":
        f.write("@" + command["arg2"] + "\n")
        f.write("D=A\n")
        f.write("@LCL\n")
        f.write("A=M+D\n")
        f.write("D=M\n")
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("M=D\n")
        f.write("@SP\n")
        f.write("M=M+1\n")
        line_count = 10
    elif command["arg1"] == "argument":
        f.write("@" + command["arg2"] + "\n")
        f.write("D=A\n")
        f.write("@ARG\n")
        f.write("A=M+D\n")
        f.write("D=M\n")
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("M=D\n")
        f.write("@SP\n")
        f.write("M=M+1\n")
        line_count = 10
    elif command["arg1"] == "this":
        f.write("@" + command["arg2"] + "\n")
        f.write("D=A\n")
        f.write("@THIS\n")
        f.write("A=M+D\n")
        f.write("D=M\n")
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("M=D\n")
        f.write("@SP\n")
        f.write("M=M+1\n")
        line_count = 10
    elif command["arg1"] == "that":
        f.write("@" + command["arg2"] + "\n")
        f.write("D=A\n")
        f.write("@THAT\n")
        f.write("A=M+D\n")
        f.write("D=M\n")
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("M=D\n")
        f.write("@SP\n")
        f.write("M=M+1\n")
        line_count = 10
    elif command["arg1"] == "temp":
        register = "@R{0}\n".format(5 + int(command["arg2"]))
        f.write(register)
        f.write("D=M\n")
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("M=D\n")
        f.write("@SP\n")
        f.write("M=M+1\n")
        line_count = 7
    elif command["arg1"] == "pointer":
        register = "@R{0}\n".format(3 + int(command["arg2"]))
        f.write(register)
        f.write("D=M\n")
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("M=D\n")
        f.write("@SP\n")
        f.write("M=M+1\n")
        line_count = 7
    elif command["arg1"] == "static":
        static_variable = "@{0}.{1}\n".format(
            command["assembly"], command["arg2"])
        f.write(static_variable)
        f.write("D=M\n")
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
    line_count = 0
    f.write("// write_pop\n")
    if command["arg1"] == "local":
        f.write("@" + command["arg2"] + "\n")
        f.write("D=A\n")
        f.write("@LCL\n")
        f.write("D=M+D\n")
        f.write("@R13\n")
        f.write("M=D\n")
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("D=M\n")
        f.write("@R13\n")
        f.write("A=M\n")
        f.write("M=D\n")
        f.write("@SP\n")
        f.write("M=M-1\n")
        line_count = 16
    elif command["arg1"] == "argument":
        f.write("@" + command["arg2"] + "\n")
        f.write("D=A\n")
        f.write("@ARG\n")
        f.write("D=M+D\n")
        f.write("@R13\n")
        f.write("M=D\n")
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("D=M\n")
        f.write("@R13\n")
        f.write("A=M\n")
        f.write("M=D\n")
        f.write("@SP\n")
        f.write("M=M-1\n")
        line_count = 16
    elif command["arg1"] == "this":
        f.write("@" + command["arg2"] + "\n")
        f.write("D=A\n")
        f.write("@THIS\n")
        f.write("D=M+D\n")
        f.write("@R13\n")
        f.write("M=D\n")
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("D=M\n")
        f.write("@R13\n")
        f.write("A=M\n")
        f.write("M=D\n")
        f.write("@SP\n")
        f.write("M=M-1\n")
        line_count = 16
    elif command["arg1"] == "that":
        f.write("@" + command["arg2"] + "\n")
        f.write("D=A\n")
        f.write("@THAT\n")
        f.write("D=M+D\n")
        f.write("@R13\n")
        f.write("M=D\n")
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("D=M\n")
        f.write("@R13\n")
        f.write("A=M\n")
        f.write("M=D\n")
        f.write("@SP\n")
        f.write("M=M-1\n")
        line_count = 16
    elif command["arg1"] == "temp":
        register = "@R{0}\n".format(5 + int(command["arg2"]))
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("D=M\n")
        f.write(register)
        f.write("M=D\n")
        f.write("@SP\n")
        f.write("M=M-1\n")
        line_count = 8
    elif command["arg1"] == "pointer":
        register = "@R{0}\n".format(3 + int(command["arg2"]))
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("D=M\n")
        f.write(register)
        f.write("M=D\n")
        f.write("@SP\n")
        f.write("M=M-1\n")
        line_count = 8
    elif command["arg1"] == "static":
        static_variable = "@{0}.{1}\n".format(
            command["assembly"], command["arg2"])
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("D=M\n")
        f.write(static_variable)
        f.write("M=D\n")
        f.write("@SP\n")
        f.write("M=M-1\n")
        line_count = 8
    else:
        raise NotImplementedError("segment unsupported")
    return line_count


def write_arithmetic(f, command, label_suffix):
    line_count = 0
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
        line_count = 9
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
        line_count = 9
    elif command["arg1"] == "neg":
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("M=-M\n")
        line_count = 4
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
        line_count = 25
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
        line_count = 25
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
        line_count = 25
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
        line_count = 9
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
        line_count = 9
    elif command["arg1"] == "not":
        f.write("@SP\n")
        f.write("A=M\n")
        f.write("A=A-1\n")
        f.write("M=!M\n")
        line_count = 4
    else:
        raise ValueError("unrecognized arithmetic command")
    return line_count


def write_file(filename, commands):
    idx = filename.find('.vm')
    if idx >= 0:
        asm_file = filename[:idx] + ".asm"
        line_count = 0
        with open(asm_file, mode='w') as f:
            write_comment(f)
            line_count += 1
            arithmetic_count = 1
            for c in commands:
                if c["command_type"] == Command.POP:
                    line_count += write_pop(f, c)
                elif c["command_type"] == Command.PUSH:
                    line_count += write_push(f, c)
                elif c["command_type"] == Command.ARITHMETIC:
                    label_suffix = format(int(arithmetic_count), 'd').zfill(3)
                    line_count += write_arithmetic(f, c, label_suffix)
                    arithmetic_count += 1

        print("Wrote (" + str(line_count) + ") lines to " + asm_file)
