import hashlib, time


def tiny_id() -> str:
    """
    Generate a short unique identifier.
    :return:
    """
    return hashlib.sha1(str(time.time()).encode()).hexdigest()[:8]

