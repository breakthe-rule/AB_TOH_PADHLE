from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
import langchain.schema.document as document  # Import the Document class
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

def create_vectordb(file_name):
    loader = DirectoryLoader("dummy", glob=file_name,loader_cls=PyPDFLoader)
    documents = loader.load()
    for i in range(len(documents)):
        dummy = documents[i].page_content
        dummy = dummy.replace(" \n", "")
        dummy = dummy.replace("\n", "")        
        new_doc = document.Document(page_content=dummy, metadata=documents[i].metadata)
        documents[i] = new_doc

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1800,chunk_overlap=300)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',model_kwargs={'device': 'cpu'})
    print("Creating db....`")
    db = FAISS.from_documents(texts, embeddings)
    print("saving...")
    db.save_local(f"vectordb/{file_name[:-4]}_vectordb")
    repath = f"dummy/{file_name}"
    os.remove(repath)
    print("Removed",file_name)

# Example usage
# create_vectordb("required_NCERT-Class-10-History.pdf")

# embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',model_kwargs={'device': 'cpu'})
# print("Loading vectordb.....")
# db = FAISS.load_local("required_Silberschatz_A_databases_6th_ed.pdf_vectordb", embeddings, allow_dangerous_deserialization=True)
# print("Loading done....")
# retriever = db.as_retriever()
# docs = retriever.invoke("what is dbms")
# context = ""; count = 0
# for i in range(len(docs)):
#     context += docs[i].page_content
#     print(docs[i].page_content)
#     count+=1
#     if count==2: break