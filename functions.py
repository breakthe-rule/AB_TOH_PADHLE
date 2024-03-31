import streamlit as st
import json

def save_chat_history(chat_history, file_path):
        with open(file_path, "w") as file:
            json.dump(chat_history, file)
            
def display_chat_history(session):
  for message in session:
    if message.get("You"):
        with st.chat_message("user",avatar = "😀"):
            st.write(message.get("You"))
    else:
        with st.chat_message("assistant",avatar = "🦖"):
            st.write(message.get("Bot"))