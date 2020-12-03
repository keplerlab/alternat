from os import path


def extract_data_from_msg(pkt):
    return pkt["msg"]["data"]


def isRequestValid(pkt):
    if ("base64" not in pkt):
        print("base64 field missing", flush=True)
        return False
    return True


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
