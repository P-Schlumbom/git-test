from flask import Flask, request
import json
import requests

app = Flask(__name__)

# This needs to be filled with the Page Access Token that will be provided
# by the Facebook App that will be created.
PAT = 'EAAFsUgXKDNgBAE4Ni76NlZBm1WKOWC8KRMZBsZCmkK6yCVRLUfjsw73qZBIb7rRHSAPibTDZBfPuY5GTcTYhZBI3wUYUDxTZCPZAG6QI5J114ezTPp7PCUygmZBh9rTmeHa0qIWIX56rKbRdiVIyzF7flfQltQrc5d7oJrtPhTkWITAZDZD'

@app.route('/', methods=['GET'])
def handle_verification():
  print("Handling Verification.")
  if request.args.get('hub.verify_token', '') == 'my_voice_is_my_password_verify_me':
    print("Verification successful!")
    return request.args.get('hub.challenge', '')
  else:
    print("Verification failed!")
    return 'Error, wrong validation token'

@app.route('/', methods=['POST'])
def handle_messages():
  print("Handling Messages")
  payload = request.get_data()
  print(payload)
  for sender, message in messaging_events(payload):
    print("Incoming from %s: %s" % (sender, message))
    send_message(PAT, sender, message)
  return "ok"

'''def messaging_events(payload):
  """Generate tuples of (sender_id, message_text) from the
  provided payload.
  """
  data = json.loads(payload)
  messaging_event = data["entry"][0]["messaging"]
  for event in messaging_event:
    if "message" in event and "text" in event["message"]:
      incoming = event["message"]["text"]
      greetings = ["hello", "hi", "good morning", "good afternoon", "good evening"]
      greeted = False
      if "hello" in incoming or "hi" in incoming or "good morning" in incoming or "good afternoon" in incoming or "good evening" in incoming:
        yield event["sender"]["id"], "Hi!"
      elif incoming == "every existing thing is born without reason":
        yield event["sender"]["id"], "and prolongs itself out of weakness"
      elif incoming == "jeder für sich":
          yield event["sender"]["id"], "und gott gegen alle"
      else:
        #yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
        yield event["sender"]["id"], "Yes, quite"
      yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
    else:
      yield event["sender"]["id"], "I can't echo this"'''
def messaging_events(payload):
  """Generate tuples of (sender_id, message_text) from the
  provided payload.
  """
  data = json.loads(payload)
  messaging_events = data["entry"][0]["messaging"]
  for event in messaging_events:
    if "message" in event and "text" in event["message"]:
      yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
    else:
      yield event["sender"]["id"], "I can't echo this"


def send_message(token, recipient, text):
  """Send the message text to recipient with id recipient.
  """

  r = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": token},
    data=json.dumps({
      "recipient": {"id": recipient},
      "message": {"text": text.decode('unicode_escape')}
    }),
    headers={'Content-type': 'application/json'})
  if r.status_code != requests.codes.ok:
    print(r.text)

if __name__ == '__main__':
  app.run()