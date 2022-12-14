# -*- coding: utf-8 -*-
"""Psiphon_key_check_bot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12t2YBYhP3sPrihSCG-G1Dj9YZ_J-NxE8

# Final Script
Required modules
"""

import requests
import json
import base64
from datetime import datetime
from pytz import timezone
from getpass import getpass
import re

"""# Variables

"""

base_url = "https://api.telegram.org/bot"

secret = getpass('Enter Code')
api_key= secret #your key

# Static variables
base_url_api_key = base_url+api_key

# Time Format
time_format = "%Y-%m-%dT%H:%M:%S"

# Dynamic variables 
owner_credits="Credits @iam_muni_baa"

match_var = "check"

"""# Matching pattern"""

def match(text):
  pattern = '\["([^\n]+)"\]'
  return re.findall(pattern,text)[-1]

"""#Reciving messages or Reading data"""

#Reciving messages or reading data
def read_message(offset):
  try:
    base_url=base_url_api_key+"/getUpdates"
    parameters = {
        "offset":offset,
    }
    res = requests.get(base_url,data = parameters)
    # print(res.text)
    data = res.json() # REsponse data converted into json data
    if data["result"]:
      chat_id = data["result"][-1]["message"]["chat"]["id"] # Getting the chat_id from the read dat or recived message
      key_in_chat=data["result"][-1]["message"]["text"]
      replay_message_id = data["result"][-1]["message"]["message_id"] # Getting replay data
      replaying_text = key_check(match(text=key_in_chat)) # Calling match function
      # print(replaying_text)

      for result in data["result"]:
        send_message(chat_id,replay_message_id,replaying_text) # Calling Send Function
      
      # # Debugging prints
      # print(chat_id, replay_message_id ,res.text)
  except:
    pass
  if data["result"]:

      return data["result"][-1]["update_id"] + 1 # Return the updated offset

"""# Sending Message code"""

#sending Message code
def send_message(chat_id,replay_message_id,replaying_text):
  base_url=base_url_api_key+"/sendMessage"
  # Parameters that we are used for 
  parameters = {
      "chat_id":chat_id, # For message we need to replay
      "text":replaying_text, #Text Message replaying here
      "reply_to_message_id": replay_message_id
  }
  res = requests.get(base_url,data = parameters)

"""# Psiphon key decode
Here its take the base64 value and return the decoded json data with date and time.
"""

def key_check(pkey):
  try:
    key_dt = json.loads(base64.b64decode(pkey))
    ExpirationDate= datetime.strptime(key_dt["Authorization"]["Expires"][0:19],time_format)
   
    now = datetime.strptime(present_time(),time_format) # For getting the local time
    
    # print(ExpirationDate)
    if ExpirationDate <= now:
      return (f"Expired {owner_credits}")
    elif ExpirationDate > now:
      return (f"\n{ExpirationDate - now} {owner_credits}")

  except :
     return "Not a valid data"

"""# For getting present time 
By using the 'PYTZ' timezones

"""

def present_time():
  now_utc = datetime.now(timezone('UTC'))
  return now_utc.strftime(time_format)
  # print(now_utc.strftime(format))

"""# Finally run code here"""

if __name__ == "__main__":
  offset = 0
  print("Iam working")
  print("")
  try:
    while True: # Its looking for messages always
      offset = read_message(offset)
      # print(offset)
  except KeyboardInterrupt:
    pass
