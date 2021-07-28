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


# TODO: this can be easily masquerade
def get_client_ip(request):
    # https://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
