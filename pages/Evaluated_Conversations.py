import streamlit as st
from openai import OpenAI
import pandas as pd
import Chat_Bot_Interface

st.set_page_config(
    page_title="Evaluated Conversations",
    layout="wide"
)

if st.session_state['evaluate'] is True:
    st.write("You have clicked the evaluate button!")
    st.write(Chat_Bot_Interface.SYSTEM_MESSAGE)
