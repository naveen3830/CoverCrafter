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

    Ensure the content of the letter is tailored to the job description and showcases the applicant's relevant skills and experiences. Use the provided user and company information in the appropriate places. Also make sure that there should not be any input able content once the coverletter is generated.
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


st.set_page_config(page_title="CoverCrafter", layout="wide", page_icon="✍️")

st.markdown("""
    <style>
        .main-header {
            font-size: 32px;
            font-weight: bold;
            color: #007BFF;
            text-align: center;
            margin-bottom: 20px;
        }
        .sub-header {
            font-size: 20px;
            font-weight: bold;
            color: #007BFF;
        }
        .section-divider {
            background-color: #007BFF;
            height: 2px;
            border: none;
        }
        .stButton>button {
            background-color: #007BFF;
            color: white;
            border-radius: 5px;
            padding: 10px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #0056b3;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Main page content
st.header("✍️ CoverCrafter: AI-Generated Cover Letters", divider='rainbow')
st.markdown("""
Welcome to **CoverCrafter**, the smart solution for crafting personalized and professional cover letters. 📝 
Whether you're applying for your dream job or looking to make a strong first impression, our AI-driven platform generates tailored cover letters that highlight your unique skills, experiences, and aspirations. Simply input your details, and let **CoverCrafter** handle the rest, delivering a cover letter that sets you apart from the competition. 🚀
""")

with st.sidebar:
    st.sidebar.header("⚙️ Settings")
    st.sidebar.markdown("Customize the cover letter generation by providing the necessary details.")
    st.divider()
    with st.expander("Get Your API Key Here"):
        st.markdown("## How to use\n"
            "1. Enter your [Groq API key](https://console.groq.com/keys) below🔑\n" 
            "2. Fill in the user and company information📄\n"
            "3. Let CoverCrafter generate your cover letter!!!💬")
    
    groq_api_key = st.text_input("Enter your Groq API key:", type="password",
            placeholder="Paste your Groq API key here (gsk_...)",
            help="You can get your API key from https://console.groq.com/keys")
    
    st.divider()
    st.header("Model Parameters")
    model_name = st.selectbox("Select Model:",["gemma2-9b-it","llama-3.1-70b-versatile","llama3-70b-8192", "mixtral-8x7b-32768"])
    temperature = st.slider("Temperature: Determines the randomness of the output. Higher values produce more creative responses.", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    top_p = st.slider("Top-p: Controls the diversity of the generated text. Lower values make the output more focused.", min_value=0.0, max_value=1.0, value=1.0, step=0.1)

    st.divider()

st.header("📋 User and Company Information", divider='rainbow')

col1, col2 = st.columns(2)
with col1:
    user_name = st.text_input("👤 Your Name")
    user_address = st.text_input("🏠 Your Street Address")
    user_city_state_zip = st.text_input("🏙️ Your City, State, Zip")

with col2:
    company_name = st.text_input("🏢 Company Name")
    company_address = st.text_input("📍 Company Street Address")
    company_city_state_zip = st.text_input("🌆 Company City, State, Zip")

position = st.text_input("💼 Position you're applying for")

st.header("📝 Job Description",divider='rainbow')
job_description = st.text_area("Enter the job description", height=200)

user_info = {
    "name": user_name,
    "address": user_address,
    "city_state_zip": user_city_state_zip,
    "company_name": company_name,
    "company_address": company_address,
    "company_city_state_zip": company_city_state_zip,
    "position": position
}

generate_button = st.button("🎉 Generate Cover Letter")

if generate_button and groq_api_key and job_description and all(user_info.values()):
    with st.spinner("Generating your cover letter..."):
        cover_letter_content = generate_cover_letter(groq_api_key, model_name, job_description, user_info, temperature)
        st.subheader("📄 Generated Cover Letter")
        st.text_area("Cover Letter", cover_letter_content, height=400)
        doc = create_word_document(cover_letter_content)
        bio = BytesIO()
        doc.save(bio)
        
        st.download_button(
            label="💾 Download as Word Document",
            data=bio.getvalue(),
            file_name="cover_letter.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
elif generate_button:
    st.warning("⚠️ Please fill in all fields and enter your Groq API key.")

st.markdown("---")
st.markdown("This app uses LangChain with the Groq API to generate personalized cover letters. Please ensure you have a valid Groq API key.")