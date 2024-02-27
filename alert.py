import os
from slack_sdk import WebhookClient
import time
import streamlit as st

# initialize web API client
client = WebhookClient(os.environ["SLACK_WEBHOOK_URL"])

falling = 0
sitting = 1
standing = 2

# send a message
first_result = st.text(falling) # [have to fix the variable]

#
results = []
if first_result == 0:
    for t in range(150):
        result = # [code later] detect it 150 times
        results.append(result)
        time.sleep(0.033)

if 1 in results or 2 in results:
    last_result = st.text('Not falling') # [check] display the result on the screen of streamlit
else:
    last_result = st.text('Falling') # [check] display the result on the screen of streamlit
    response = client.send(text='Falling')
