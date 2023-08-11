import requests


def args2url(url, **kwargs):
    if url[-1] == "/":  # if ends with /
        url = url[:-1] + "?"
    elif url.rfind("=") > url.rfind("?") and url[-1] != "&":
        url = url + "&"
    elif url[-1] != "?":
        url += "?"

    for key in kwargs:
        url += key + "=" + kwargs[key] + "&"
    return url[:-1]
