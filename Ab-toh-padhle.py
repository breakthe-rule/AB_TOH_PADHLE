import streamlit as st
import os
import glob
import openai
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import json
from functions import save_chat_history, display_chat_history
from pdf2text import required_txt
from vectordb import create_vectordb

#openai initialization
openai.api_base = "http://localhost:1234/v1"
openai.api_key = "not-needed"
            
# Initialize chat history (empty list)
if "chat_history_local" not in st.session_state:
    st.session_state.chat_history_local = []
    st.session_state.llm_history_local = [
                                    {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
                                   ]

st.write("# :white[Ab Toh Padhle 🤖]")
st.divider()

# Select textbook
directory = 'Material'
pdf_files = glob.glob(os.path.join(directory, '*.pdf'))
options = []
for pdf_file in pdf_files:
    options.append(pdf_file.split("\\")[-1][:-4])

with st.sidebar:
    # Select textbook
    selected_pdf = st.selectbox("Book name: ", options)
    click1 = st.button(":orange[Create Requirements]")
    if click1: 
        st.write(":green[Creating required pdf]")
        required_txt(f"{selected_pdf}.pdf")
        st.write(":green[Creating vectordb]")
        create_vectordb(f"required_{selected_pdf}.pdf")
        st.write(":green[Requirements loaded]")
    st.divider()
    
    # New chat
    click2 = st.button(":orange[New Chat]")
    if click2: 
        st.session_state.chat_history_local = []
        st.session_state.llm_history_local = [
                                        {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
                                    ]
        display_chat_history(st.session_state.chat_history_local)
        
user_message = st.chat_input("You:", key="user_message")

if user_message:
    # Retrival
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',model_kwargs={'device': 'cpu'})
    db = FAISS.load_local(f"vectordb/required_{selected_pdf}_vectordb", embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever()
    docs = retriever.invoke(user_message)
    context = ""; count = 0
    for i in range(len(docs)):
        context += docs[i].page_content
        count+=1
        if count==2: break
    st.session_state.chat_history_local.append({"You":user_message})
    st.session_state.llm_history_local.append({"role": "user", "content": context + "\n" + user_message})
    
    # Generation
    completion = openai.ChatCompletion.create(
        model="local-model", # this field is currently unused
        messages=st.session_state.llm_history_local,
        temperature=0.6,
        stream=True,
        )
    
    new_message = {"role": "assistant", "content": ""}
    answer = ''
    for chunk in completion:
        if chunk.choices[0].get("delta", {}).get("content"):
            new_message["content"] += chunk.choices[0].delta.content
            
    st.session_state.chat_history_local.append({"Bot":new_message["content"]})
    st.session_state.llm_history_local.append(new_message)

    save_chat_history(st.session_state.chat_history_local, f"History/{st.session_state.chat_history_local[0]['You'].strip().strip('?')}.json")
    
# Display chat history
display_chat_history(st.session_state.chat_history_local)