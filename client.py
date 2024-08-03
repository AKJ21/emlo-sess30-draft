import requests
import time
import streamlit as st
from streamlit_chat import message

def main():
    # load_dotenv()
    st.set_page_config(page_title="Felis V0")
    st.header("💬 Felis Chatbot")

    response=[]

    user_question = st.chat_input("Ask a question.")
    if user_question:
        url = "http://<aws_ip>:9080/infer"
        payload = {'text':user_question}
        response = requests.get(url, params=payload)

        # Layout of input/response containers
        response_container = st.container()

        with response_container:
            for i, messages in enumerate(st.session_state.chat_history):
                if i % 2 == 0:
                    message(messages.content, is_user=True, key=str(i))
                else:
                    message(messages.content, key=str(i))

if __name__ == '__main__':
    main()