import streamlit as st
<<<<<<< HEAD
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import re
=======
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.prompts import ChatMessagePromptTemplate, PromptTemplate, FewShotPromptTemplate
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
>>>>>>> 93a1b1e16b76f269d833b1d537e65677f56754d6

# Load environment variables
load_dotenv()

# Get the Groq API key from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")
<<<<<<< HEAD
llm = ChatGroq(groq_api_key=groq_api_key, model="gemma-7b-it", temperature=1)

# Set Streamlit page configuration
st.set_page_config(page_title="VocabMaster", layout="wide", initial_sidebar_state="expanded")

# Set the header of the app
st.title("VocabMaster :books:")
st.markdown("Expand your vocabulary with unique and useful English words!")

# Initialize session state for storing generated words
if 'generated_words' not in st.session_state:
    st.session_state.generated_words = set()

vocab_template = PromptTemplate(
    input_variables=["excluded_words"],
    template="""You are VocabMaster, an expert in English vocabulary. Generate 5 unique and diverse English words that are useful in daily life to improve English speaking skills. 
    Ensure that these words are not commonly used in everyday conversation and are different from any words you've generated before.
    Do not use any of these words: {excluded_words}
    For each word, provide:
    1. The word itself
    2. Its part of speech
    3. A brief definition
    4. An example sentence using the word

    Format each word's information as follows:
    **Word:** [word]
    **Part of Speech:** [part of speech]
    **Definition:** [definition]
    **Example:** [example sentence]

    Separate each word's information with a blank line."""
)

def generate_vocabulary():
    excluded_words = ", ".join(st.session_state.generated_words)
    response = llm.invoke(vocab_template.format(excluded_words=excluded_words))
    return response.content

def parse_word_info(word_info):
    patterns = {
        'word': r'\*\*Word:\*\* (.+)',
        'pos': r'\*\*Part of Speech:\*\* (.+)',
        'definition': r'\*\*Definition:\*\* (.+)',
        'example': r'\*\*Example:\*\* (.+)'
    }
    
    result = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, word_info, re.IGNORECASE | re.DOTALL)
        if match:
            result[key] = match.group(1).strip()
    
    return result if len(result) == 4 else None

def main():
    # Button to generate vocabulary
    if st.button('Generate Vocabulary'):
        with st.spinner('Generating vocabulary...'):
            vocabulary = generate_vocabulary()
        
        # Remove the header if present
        vocabulary = re.sub(r'\*\*New Words for Advanced English Speaking:\*\*\n*', '', vocabulary)
        
        # Parse and display the vocabulary
        words = re.split(r'\n\s*\n', vocabulary)
        for word_info in words:
            parsed_info = parse_word_info(word_info)
            if parsed_info:
                st.markdown(f"""
                **{parsed_info['word']}** ({parsed_info['pos']})
                
                *Definition:* {parsed_info['definition']}
                
                *Example:* {parsed_info['example']}
                """)
                st.session_state.generated_words.add(parsed_info['word'].lower())
            else:
                st.warning(f"Couldn't parse this word information:\n{word_info}")

    # Display the number of unique words generated so far
    st.sidebar.write(f"Unique words generated: {len(st.session_state.generated_words)}")
=======
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
>>>>>>> 93a1b1e16b76f269d833b1d537e65677f56754d6

# Run the main function
if __name__ == "__main__":
    main()
