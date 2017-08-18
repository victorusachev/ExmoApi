def recursive_transform(obj):
    """
    Recursive converting object to properly handle int and float.

    :param obj: json object
    :return: another json object
    """
    if isinstance(obj, dict):
        return {k: recursive_transform(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [recursive_transform(el) for el in obj]
    if isinstance(obj, (float, int, bool, type(None))):
        return obj
    if isinstance(obj, str):
        for typ in (int, float, str):
            try:
                rv = typ(obj)
                return rv
            except:
                pass
    return obj
