import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

#loading env file
load_dotenv()

#configuring streamlit page setting
st.set_page_config(
    page_title="Chat with DoDo",
    page_icon= ":smiley:",
    layout="centered"
)

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

#setting up google gemini_ai_pro model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model=gen_ai.GenerativeModel('gemini-1.5-pro')


# function that translates user role between Gemini 1.5 pro and stramlit
def translate_role_for_streamlit(user_role):
    if (user_role=="model"):
        return "assitant"
    else:
        return user_role

#initialize Chat session in streamlit if alredy no present
if "chat_session" not in st.session_state:
    st.session_state.chat_session=model.start_chat(history=[])

#Displaying the chatbot title in page
#st.title("🦤")

# Using st.markdown for enhanced styling
st.markdown(
    """
    <div style='text-align: center;'>
        <h1 style='font-size: 3em; color: #005f87;'>
            🦤
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

#Displaying the mesaage
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown((message.parts[0].text))

#input fields for users message
user_prompt = st.chat_input("Ask DODO 🦤...")

if user_prompt:
    # add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    #Send user's message to gemini pro and get response
    gemini_response=st.session_state.chat_session.send_message(user_prompt)

    #display the response from model
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)



