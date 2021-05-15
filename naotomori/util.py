import logging
import time

from jikanpy import jikan

logger = logging.getLogger('NaoTomori')


def jikanCall(func, **args):
    """
    Send a request to the MAL api through Jikan.
    However, since MAL enforces limitations on the request rate, we stall the internal requests to this api.
    See https://jikan.docs.apiary.io/#introduction/information/rate-limiting.
    """
    while True:
        time.sleep(4.20)  # here we stall (we need at least 4 seconds in between requests)
        try:
            return func(**args)
        except jikan.APIException as e:
            if e.status_code == 503:
                logger.warning(f"Sending requests too fast (503): {str(e)}")
                pass    # woops, we might have sent that request too fast, try again
            else:
                logger.error(f"Error sending request to MAL using Jikan: {str(e)}")
                raise e
