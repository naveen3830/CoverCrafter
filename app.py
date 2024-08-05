import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from docx import Document
from io import BytesIO
from datetime import date

def generate_cover_letter(api_key, model, job_description, user_info, temperature):
    chat = ChatGroq(
        groq_api_key=api_key,
        model_name=model,
        temperature=temperature,
        max_tokens=2048
    )

    system_template = """
    You are a professional cover letter writer. Generate a well-structured cover letter in plain text format using the provided user information and job description.
    """

    human_template = f"""
    Create a cover letter based on the following user information and job description. The cover letter should be in plain text format, ready to be inserted into a Word document.

    User Information:
    Name: {user_info['name']}
    Address: {user_info['address']}
    City, State ZIP: {user_info['city_state_zip']}
    Position applying for: {user_info['position']}

    Company Information:
    Company Name: {user_info['company_name']}
    Company Address: {user_info['company_address']}
    Company City, State ZIP: {user_info['company_city_state_zip']}

    Job Description:
    {job_description}

    Use the following structure for the cover letter:

    [User's Name]
    [User's Address]
    [User's City, State ZIP Code]

    [Today's Date]

    [Company Name]
    [Company Address]
    [Company City, State ZIP Code]

    Dear Hiring Manager,

    [First paragraph: Introduction and statement of interest in the specific position]

    [Second paragraph: Highlight relevant skills and experiences based on the job description]

    [Third paragraph: Expand on why the applicant is a good fit for the role and the company]

    [Closing paragraph: Express enthusiasm and request for interview]

    Sincerely,

    [User's Name]

    Ensure the content of the letter is tailored to the job description and showcases the applicant's relevant skills and experiences. Use the provided user and company information in the appropriate places.
    """

    chat_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_template),
        HumanMessage(content=human_template)
    ])

    chain = chat_prompt | chat

    result = chain.invoke({
        "name": user_info['name'],
        "address": user_info['address'],
        "city_state_zip": user_info['city_state_zip'],
        "company_name": user_info['company_name'],
        "company_address": user_info['company_address'],
        "company_city_state_zip": user_info['company_city_state_zip'],
        "position": user_info['position'],
        "job_description": job_description
    })

    return result.content

def create_word_document(content):
    doc = Document()
    for paragraph in content.split('\n'):
        doc.add_paragraph(paragraph)
    return doc

st.set_page_config(page_title="CoverCrafter", layout="wide")

st.title("CoverCrafter: AI-Generated Cover Letters")

# Sidebar
st.sidebar.header("Settings")
st.sidebar.markdown("Customize the cover letter generation by providing the necessary details.")
api_key = st.sidebar.text_input("Enter your Groq API Key", type="password")
model = st.sidebar.selectbox("Select Model",["llama-3.1-70b-versatile","llama3-70b-8192", "mixtral-8x7b-32768", "gemma2-9b-it"])
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.1)

# Main page
st.header("User and Company Information")
col1, col2 = st.columns(2)

with col1:
    user_name = st.text_input("Your Name")
    user_address = st.text_input("Your Street Address")
    user_city_state_zip = st.text_input("Your City, State, Zip")

with col2:
    company_name = st.text_input("Company Name")
    company_address = st.text_input("Company Street Address")
    company_city_state_zip = st.text_input("Company City, State, Zip")

position = st.text_input("Position you're applying for")

st.header("Job Description")
job_description = st.text_area("Enter the job description", height=200)

# User information dictionary
user_info = {
    "name": user_name,
    "address": user_address,
    "city_state_zip": user_city_state_zip,
    "company_name": company_name,
    "company_address": company_address,
    "company_city_state_zip": company_city_state_zip,
    "position": position
}

generate_button = st.button("Generate Cover Letter")

if generate_button and api_key and job_description and all(user_info.values()):
    with st.spinner("Generating your cover letter..."):
        cover_letter_content = generate_cover_letter(api_key, model, job_description, user_info, temperature)
        st.subheader("Generated Cover Letter")
        st.text_area("Cover Letter", cover_letter_content, height=400)
        
        # Create and download Word document
        doc = create_word_document(cover_letter_content)
        bio = BytesIO()
        doc.save(bio)
        
        st.download_button(
            label="Download as Word Document",
            data=bio.getvalue(),
            file_name="cover_letter.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
elif generate_button:
    st.warning("Please fill in all fields and enter your Groq API key.")

st.markdown("---")
st.markdown("This app uses LangChain with the Groq API to generate personalized cover letters. Please ensure you have a valid Groq API key.")
