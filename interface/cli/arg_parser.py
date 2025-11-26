import shlex as sh


def parse_args(arg: str) -> list[str]:
    """Parse a string of arguments into a list, handling quoted substrings as single arguments.
    :param arg: The input string containing arguments.
    :return: A list of parsed arguments.
    """
    return sh.split(arg)
