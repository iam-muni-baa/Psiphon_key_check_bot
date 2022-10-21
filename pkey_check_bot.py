import requests
import json
import base64
from datetime import datetime

base_url = "https://api.telegram.org/bot"
api_key="" #YOur bot api key here

# Static variables
base_url_api_key = base_url+api_key
# Dynamic variables 
match_var = "check"

#Reciving messages or reading data
def read_message(offset):
  base_url=base_url_api_key+"/getUpdates"
  parameters = {
      "offset":offset,
  }
  res = requests.get(base_url,data = parameters)

  data = res.json() # REsponse data converted into json data
  if data["result"]:
    chat_id = data["result"][-1]["message"]["chat"]["id"] # Getting the chat_id from the read dat or recived message
    if "reply_to_message" in res.text :
      key_in_chat=data["result"][-1]["message"]["reply_to_message"]["text"]
      replay_message_id = data["result"][-1]["message"]["reply_to_message"]["message_id"] # GEtting replay data
      replaying_text = key_check(key_in_chat[2:-2])
      for result in data["result"]:
        if match_var in (result["message"]["text"]): # Checking the recived messages matches with ours or not
          send_message(chat_id,replay_message_id,replaying_text) # Calling Send Function

    # # Debugging prints
    # print(chat_id,  replay_message_id  )

  if data["result"]:

    return data["result"][-1]["update_id"] + 1
  
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

# Checks the validity
def key_check(pkey):
  try:
    key_dt = json.loads(base64.b64decode(pkey))
    ExpirationDate = datetime.strptime(key_dt["Authorization"]["Expires"][0:19],"%Y-%m-%dT%H:%M:%S")
    now = datetime.now()
    if ExpirationDate <= now:
      return "Expired"
    elif ExpirationDate > now:
      return (f"{ExpirationDate - now} Credits @iam_muni_baa")
  except :
     return "Not a valid data"
offset = 0
while True: # Its looking for messages always
  offset = read_message(offset)
  # print(offset)
