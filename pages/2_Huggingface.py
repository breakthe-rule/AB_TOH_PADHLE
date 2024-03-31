from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import streamlit as st
import os
import json
import glob

from pdf2text import required_txt
from vectordb import create_vectordb
from functions import save_chat_history, display_chat_history

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

st.title("HUGGINGFACE :smile:")
st.divider()
             
if "chat_history" not in st.session_state:
    st.session_state.llm_history = 0
    st.session_state.chat_history = []

directory = 'Material'
pdf_files = glob.glob(os.path.join(directory, '*.pdf'))
options = []
for pdf_file in pdf_files:
    options.append(pdf_file.split("\\")[-1][:-4])

with st.sidebar:
    selected_pdf = st.selectbox("Book name: ", options)
    click1 = st.button(":orange[Create Requirements]")
    if click1: 
        st.write(":green[Creating required pdf]")
        required_txt(f"{selected_pdf}.pdf")
        st.write(":green[Creating vectordb]")
        create_vectordb(f"required_{selected_pdf}.pdf")
        st.write(":green[Requirements loaded]")
    
    selected_model = st.text_input("HF repo", value="mistralai/Mistral-7B-Instruct-v0.2",key = "model")
    st.divider()
    
    click2 = st.button(":orange[New Chat]")
    if click2: 
        st.session_state.llm_history = 0
        st.session_state.chat_history = []
        display_chat_history(st.session_state.chat_history)

llm = HuggingFaceEndpoint(
    repo_id= selected_model, 
    model_kwargs={"max_length": 512},
    temperature = 0.5,
    max_new_tokens = 216,
    )
memory = ConversationBufferMemory()
prompt = PromptTemplate(
    input_variables=["teacher"],
    template="You're the {teacher} and you didn't have to be sarcastic"
)
if st.session_state.llm_history: memory = st.session_state.llm_history
print("chain")
conversation = LLMChain(
    llm=llm,
    # verbose=True,
    prompt=prompt,
    memory=memory
)
       
user_message = st.chat_input("You:")

if user_message:
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',model_kwargs={'device': 'cpu'})
    db = FAISS.load_local(f"vectordb/required_{selected_pdf}_vectordb", embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever()
    docs = retriever.invoke(user_message)
    context = ""; count = 0
    for i in range(len(docs)):
        context += docs[i].page_content
        count+=1
        if count==2: break
        
    st.session_state.chat_history.append({"You":user_message})
    
    pred = conversation.invoke(input = user_message)
    st.session_state.llm_history = memory
    st.session_state.chat_history.append({"Bot":pred["text"]})
    
    save_chat_history(st.session_state.chat_history, f"History/{st.session_state.chat_history[0]['You'].strip('?')}.json")
    
display_chat_history(st.session_state.chat_history)