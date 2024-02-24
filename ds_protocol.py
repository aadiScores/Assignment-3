# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Aadi Shanker
# aadidevs@uci.edu
# 75948470

import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys
DataTuple = namedtuple('DataTuple', ['join', 'token', 'response'])

def extract_json(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  
  TODO: replace the pseudo placeholder keys with actual DSP protocol keys
  '''
  print(json_msg)
  try:
    json_obj = json.loads(json_msg)
    join = json_obj['join']
    token = json_obj['token']
    response = json_obj['response']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(join, token, response)

# json_msg = '{"response": {"type": "ok", "message": "Welcome back, f21demo", "token": "5e82abc4-f3b5-45ca-bb57-a7eb76adc2bf"}}'
# print(extract_json(json_msg))