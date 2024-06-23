import streamlit as st
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.prompts import ChatMessagePromptTemplate, PromptTemplate, FewShotPromptTemplate
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the Groq API key from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(groq_api_key=groq_api_key, model="gemma-7b-it",temperature=1.5)

# Set Streamlit page configuration
st.set_page_config(page_title="VocabMaster", layout="centered")

# Set the header of the app
st.header("VocabMaster :books:")

def generate_vocabulary():
    # Template for generating vocabulary
    template = "Your name is VocabMaster. You are an expert in English vocabulary. Introduce yourself as VocabMaster. You can generate 5 English words that are useful in daily life to improve English speaking skills, along with example uses of each word. You are only allowed to answer vocabulary-related queries. If you don't know the answer, respond with 'I don't know the answer.' Also try not to repeat the words again."
    
    # Generate response from LLM
    response = llm.invoke(template)
    
    return response.content

def main():
    # Button to generate vocabulary
    if st.button('Generate Vocabulary'):
        vocabulary = generate_vocabulary()
        st.write(vocabulary)

# Run the main function
if __name__ == "__main__":
    main()
