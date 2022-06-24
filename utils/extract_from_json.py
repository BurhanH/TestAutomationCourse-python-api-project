"""Extracting key-value pairs from JSON"""


def json_extractor(json, *args):
    result = []
    for i in list(json.items()):
        if i[0] in args:
            result.append(i)
    return dict(result)
