from os import path
import base64
import requests
import mimetypes
from exceptions import UnsupportedImageType, InvalidImageURL, ImageNotLoaded

_URL = "url"
_BASE64 = "base64"

_SUPPORTED_IMAGE_FORMATS = ["png", "jpeg", "jpg"]

def extract_data_from_msg(pkt):
    return pkt["msg"]["data"]


def get_as_base64(url):

    try:
        response = requests.get(url)
    except:
        raise ImageNotLoaded()
    image_content = response.content
    content_type = response.headers["content-type"]
    headers_list = content_type.split("/")
    print(" headers ", headers_list, flush=True)

    if headers_list[0].lower() == "image":
        image_type = headers_list[-1]

        if image_type.lower() not in _SUPPORTED_IMAGE_FORMATS:
            raise UnsupportedImageType()
        else:
            return base64.b64encode(image_content)
    else:
        raise InvalidImageURL()


def isRequestValid(pkt):

    is_valid = False
    if _BASE64 in pkt:
        is_valid = True
    elif _URL in pkt:
        is_valid = True
    else:
        print("Invalid request", flush=True)
    return is_valid


def prepare_response(pkt, is_ok):
    if is_ok:
        response_pkt = pkt
        response_pkt["response"] = {
            "status": True,
        }
        return response_pkt
    else:
        response_pkt = pkt
        response_pkt["response"] = {"status": False}
        return response_pkt
