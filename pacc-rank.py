import os
import struct
import sys
import time
import datetime
import array
import enum
import urllib
import json
import re
import requests
import logging
from collections import Counter
from collections import OrderedDict

DEFAULT_CACHE_FOLDER:str = "cache"
DEFAULT_PROTOCOL_PATH:str = "protocol.txt"
REMOTE_PROTOCOL_REFERENCE:str = "https://rgk.vote.mod.gov.ua/protocol.txt"


class PaccRank():

    _remote_reference : str
    _values : Counter = Counter()
    _sorted_values : OrderedDict = OrderedDict()

       
    def __init__(self, remote_reference : str):
        self._remote_reference = remote_reference
        pass

    def process(self):
        tmp : dict = dict()
        for index, (key, value) in enumerate(self._values.items()):
            tmp[value] = key

        self._sorted_values = OrderedDict(sorted(tmp.items(), key=lambda item: item[0], reverse=True))
            
    def print_result(self):
        for index, (key, value) in enumerate(self._sorted_values.items()):
            print(str(index) + "). " + str(value) + " - " + str(key))

        
 

    def prepare_data(self):
        protocol_text:str

        if not os.path.exists(DEFAULT_CACHE_FOLDER):
            os.makedirs(DEFAULT_CACHE_FOLDER, exist_ok=True)
            content:bytes = self._load_protocol_from_remote()
            full_path = os.path.join(DEFAULT_CACHE_FOLDER, DEFAULT_PROTOCOL_PATH)
            with open(full_path, "w") as protocol_file:
                 protocol_file.write(content)
        
        full_path = os.path.join(DEFAULT_CACHE_FOLDER, DEFAULT_PROTOCOL_PATH)
        with open(full_path, "r") as protocol_file:
            for line in iter(protocol_file.readline, ''):
                index_begin = line.find("V=")
                if index_begin != -1:
                    index_begin += 2
                    index_end = line.find("\n", index_begin)
                    if index_end != -1:
                        eval = line[index_begin:index_end] 
                        elements = eval.split(",")
                        vals = list(map(int, elements))
                        self._store_values(vals)

    def _store_values(self, vals):
        self._values.update(vals)
   
    def _load_protocol_from_remote(self): 
        print("Loading from remote...")
        result = requests.get(REMOTE_PROTOCOL_REFERENCE)
        protocol:bytes = result.content.decode('utf-8')
        return protocol

if __name__ == "__main__":
    logging.basicConfig()
    print("Starting...")
    ss = PaccRank("")
    ss.prepare_data()
    ss.process()
    ss.print_result()
