import re


def get_body(s: str) -> str:
    """
    Args:
        s (str): full html string

    Returns:
        string of the body of the html. Return empty string on nothing found.
    """
    match = re.search(r"<body>([.\s\S]*)<\/body>", s, re.MULTILINE)
    if match is None or len(match.groups()) < 1:
        return ''
    return match.group(1)
