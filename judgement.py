import schedule
import time
import random
import numpy as np
import os
from slack_sdk import WebhookClient
import streamlit as st

# initialize web API client
client = WebhookClient(os.environ["SLACK_WEBHOOK_URL"])

## this is for test

def judgement():
    results = np.zeros((1,29), 'int32')[0]
    results = results.tolist()
    noise = random.randint(0,10)
    results.append(noise)

    res = st.text(results)

    if noise != 10:
        last_result = st.text('Not falling')
    else:
        last_result = st.text('Falling') # [check] display the result on the screen of streamlit
        response = client.send(text='Your grandmother fell down!')

schedule.every(5).seconds.do(judgement)


while True:
    schedule.run_pending()
    time.sleep(0.001)
