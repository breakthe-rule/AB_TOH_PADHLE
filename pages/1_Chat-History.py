import json
import streamlit as st
import os
import glob
from functions import display_chat_history 
   
directory = 'History'
json_files = glob.glob(os.path.join(directory, '*.json'))
options = []
for json_file in json_files:
    options.append(json_file.split("\\")[-1][:-5])

Selected_Chat = st.selectbox("Chat:", options)

click1 = st.button(":orange[See Chat]")
if click1: 
    file_path = f"History\{Selected_Chat}.json"
    with open(file_path, "r") as file:
        chat_history = json.load(file)

    # Print the chat history
    display_chat_history(chat_history)