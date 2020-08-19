import time


def jikanCall(func, **args):
    """
    Send a request to the MAL api through Jikan.
    However, since MAL enforces limitations on the request rate, we stall the internal requests to this api.
    See https://jikan.docs.apiary.io/#introduction/information/rate-limiting.
    """
    time.sleep(6)  # here we stall (we need at least 4 seconds in between requests)
    return func(**args)
