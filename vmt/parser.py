from vmt.command import Command

arithmetic_keywords = ["add",
                       "sub",
                       "neg",
                       "eq",
                       "gt",
                       "lt",
                       "and",
                       "or",
                       "not"]

commands = []

def strip_line(line):
    line = line.strip(' \r\n')
    if len(line) > 0:
        comment = line.rfind('//')
        if comment >= 0:
            line = line[:comment].strip(' \r\n')
    return line


def parse_command(line):
    command = { "text" : line}
    tokens = line.split(" ")
    if len(tokens) >= 1:
        if tokens[0] == "push" and len(tokens) == 3:
            command["command_type"] = Command.PUSH
            command["arg1"] = tokens[1]
            command["arg2"] = tokens[2]
        elif tokens[0] == "pop" and len(tokens) == 3:
            command["command_type"] = Command.POP
            command["arg1"] = tokens[1]
            command["arg2"] = tokens[2]
        elif tokens[0] in arithmetic_keywords:           
            command["command_type"] = Command.ARITHMETIC
            command["arg1"] = tokens[0]
        else:
            pass
    else:
        raise ValueError("Empty token list for line " + line)
    return command


def load_file(filename):
    with open(filename) as f:
        for line in f:
            s = strip_line(line)
            if len(s) > 0:
                commands.append(parse_command(s))


def get_commands():
    return commands
