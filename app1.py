import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import random

# Load environment variables
load_dotenv()

# Get the Groq API key from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(groq_api_key=groq_api_key, model="gemma-7b-it", temperature=1.5)

# Set Streamlit page configuration
st.set_page_config(page_title="VocabMaster", layout="centered")

# Set the header of the app
st.header("VocabMaster :books:")

# Initialize session state for storing generated words
if 'generated_words' not in st.session_state:
    st.session_state.generated_words = set()

# Create a prompt template
vocab_template = PromptTemplate(
    input_variables=["excluded_words"],
    template="""Your name is VocabMaster. You are an expert in English vocabulary. Introduce yourself as VocabMaster. 
    Generate 5 unique and diverse English words that are useful in daily life to improve English speaking skills. 
    Ensure that these words are not commonly used in everyday conversation and are different from any words you've generated before.
    Do not use any of these words: {excluded_words}
    For each word, provide:
    1. The word itself
    2. Its part of speech
    3. A brief definition
    4. An example sentence using the word

    Present the information in a clear, formatted manner.
    You are only allowed to provide vocabulary-related information. 
    If you don't know the answer to something, respond with 'I don't know the answer.'"""
)

def generate_vocabulary():
    excluded_words = ", ".join(st.session_state.generated_words)
    response = llm.invoke(vocab_template.format(excluded_words=excluded_words))
    
    # Extract new words from the response (this is a simplistic approach and might need refinement)
    new_words = set([word.strip().lower() for word in response.content.split('\n') if word.strip() and not word.strip()[0].isdigit()])
    st.session_state.generated_words.update(new_words)
    
    return response.content

def main():
    # Button to generate vocabulary
    if st.button('Generate Vocabulary'):
        with st.spinner('Generating vocabulary...'):
            vocabulary = generate_vocabulary()
        st.markdown(vocabulary)

    # Display the number of unique words generated so far
    st.sidebar.write(f"Unique words generated: {len(st.session_state.generated_words)}")

# Run the main function
if __name__ == "__main__":
    main()