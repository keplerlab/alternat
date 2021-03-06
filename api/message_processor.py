import logging
from typing import Optional
import sys
from fastapi import FastAPI
import json
import pkt_handler as pkt_handler
from config import Config
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from alternat.generation.generator import Generator
from alternat.collection.collector import Collector

generator = Generator()
collector = Collector()


class ItemBase64(BaseModel):
    base64: str


class ItemURL(BaseModel):
    url: str
    context: dict = {}


# Import config
cfg = Config()

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/")
def read_root2():
    return {"Hello": "World in Post"}


@app.post("/generate_text_base64")
def read_item(inputPkt:ItemBase64):
    inputPktJson = jsonable_encoder(inputPkt)
    is_ok = pkt_handler.isRequestValid(inputPktJson)
    if is_ok is False:
        print("ERROR in request", flush=True)
        response_pkt = pkt_handler.prepare_response(inputPktJson, is_ok)
        return response_pkt
    else:
        base64_image = inputPktJson[pkt_handler._BASE64]
        result_json = generator.generate_alt_text_from_base64(base64_image)
        print("result_json", result_json,flush=True)
        response_pkt = pkt_handler.prepare_response(result_json, is_ok)
        return response_pkt


@app.post("/generate_text_url")
def read_item(inputPkt:ItemURL):
    inputPktJson = jsonable_encoder(inputPkt)
    is_ok = pkt_handler.isRequestValid(inputPktJson)
    if is_ok is False:
        print("ERROR in request", flush=True)
        response_pkt = pkt_handler.prepare_response(inputPktJson, is_ok)
        return response_pkt
    else:
        url = inputPktJson[pkt_handler._URL]
        try:
            base64_image = pkt_handler.get_as_base64(url)
            result_json = generator.generate_alt_text_from_base64(base64_image)
            print("result_json", result_json, flush=True)
            response_pkt = pkt_handler.prepare_response(result_json, is_ok)
            return response_pkt
        except Exception as e:
            print("Error: ", e, flush=True)
            inputPktJson["error"] = e
            response_pkt = pkt_handler.prepare_response(inputPktJson, False)
            return response_pkt
