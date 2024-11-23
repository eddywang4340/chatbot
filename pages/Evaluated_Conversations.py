import streamlit as st
from openai import OpenAI
import pandas as pd
import requests

st.set_page_config(
    page_title="Evaluated Conversations",
    layout="wide"
)

nausea_user_prompts = [
    "What do I do about the nausea that I'm having with Wegovy?",
    "1mg, I just increased last week.",
    "Maybe, I don’t know.",
    "I guess so, I'm not eating much."
]

nausea_expected_response = [
    "Got it, you're having nausea with Wegovy Let me ask you a few questions to better understand: what dose are you on and how long have you been at this dose?",
    "Nausea and stomach upset are common with GLP-1’s, especially when starting or increasing the dose. Usually, this gets better over time, typically within 2-4 weeks. Other things that can make nausea worse include high-fat foods, large meals, or eating too quickly. Do you think any of these could have worsened your nausea?",
    "Here are a few tips to try: eat smaller, more frequent meals, reduce portion sizes, and avoid high-fat foods. Stay hydrated! It's not about calories right now—focus on avoiding dehydration. Does that help?",
    "If your nausea becomes severe and you're unable to stay hydrated or eat for more than 48-72 hours, contact your doctor. GERD may also cause nausea, and anti-reflux medication could help. Let me know how it goes!"
]

if st.session_state['evaluate'] is True:
    # OpenAI client session
    client = OpenAI(api_key=st.secrets["API_KEY"])

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "evaluations" not in st.session_state:
        # Need to feed SYSTEM_MESSAGE into the model first before allowing user to type or select their prompt
        st.session_state.evaluations = [{"role": "system", "content": st.session_state['sys_message']}]
    for user_prompt, expected in zip(nausea_user_prompts, nausea_expected_response):
        st.session_state.messages[0] = {"role": "system", "content": st.session_state['sys_message']}
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model=st.session_state['model_option'],
            messages=st.session_state.messages,
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
            st.markdown("**EXPECTED**: " + expected)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.info('This is a purely informational message', icon="ℹ️")

        # # Call API request (get API endpoint name and API key from Shishir) to send over stream and expected
        # payload = {
        #     "client": client,
        #     "expected": expected,
        #     "actual": response
        # }
        # # TODO: Change the API endpoint to what Shishir sent it to be
        # response = requests.post("http://127.0.0.1:5000/api/analyze", json=payload)
        # if response.status_code == 200:
        #     result = response.json()
        #     st.write("Analysis Result:", result)
        
        st.markdown("---")

        # TODO: Work on adding filters to the conversations: filter by semantics value (adding a slider and a comparison oeprator), intent (boolean), factual (boolean), needs_human_review (boolean)
        # Work on organizing the conversations by conversation # (e.g.: Conversation #1: Nausea with Wegovy) - also add a filter for this
        # Work on layout of expected vs. actual (make it side by side instead of stacked upon each other)

