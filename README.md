# AB-TOH-PADHLE
**🤖📚 Textbook Chatbot**

This project is a chatbot designed to assist students in interacting with their textbooks in a conversational manner. The chatbot has been developed using the RAG (Retrieval-Augmented Generation) model, which enables it to understand and respond to natural language queries. It can be run locally on a machine using LM Studio or accessed via the internet using the Hugging Face API.

**🌐 Features:**

* *Select a textbook of your choice and initiate a conversation with it.*
* *Accessible via a user-friendly interface created with Streamlit.*
* *Contains chat memory: reponse of each chat is based on previous chats.*
* *View chat history to keep track of conversations.*
* *Select LLM of your own.*
* *Runs on both local machine and via internet.*

## UI
![Home Screen](https://github.com/breakthe-rule/AB_TOH_PADHLE/assets/114070578/35a3071e-568a-4529-873e-e13f9141997b)
![Huggingface](https://github.com/breakthe-rule/AB_TOH_PADHLE/assets/114070578/f13f2583-8890-4d59-8723-3046d86f1a01)
![Chat_history](https://github.com/breakthe-rule/AB_TOH_PADHLE/assets/114070578/1b478f2a-b2b7-4ce5-9d94-aae6b36537db)

## Workflow

## Setup

1. `Clone this repo to your PC.`
2. `Install LM studio and download LLM which satisfy your hardware requirements.`
3. `Setup gpu on your PC based on your hardware.`
    * `Setup GPU on LM studio`
    * `In vectordb.py, Line 21; Ab-toh-padhle.py, Line 58 and 2_Huggingface.py, Line 73 change device to cuda`
3. `Add your huggingface token with read access in:- pages\2_Huggingface.py`
4. `Add required textbook in pdf format inside 'Material' folder.`
5. `streamlit run Ab-toh-padhle.py`
6. `In sidebar select book and click 'Create Requirements' (need to do only once if new textbook is added)`
7. `Whooo 🎉 Your setup is completed !!`


## Contact
I am open for any kind of suggetions/help regarding this project/domain. Feel free to reach me at [Mail](tanayfalor@gamil.com) and [Linkedin](https://www.linkedin.com/in/tanay-falor-a94802253/)


