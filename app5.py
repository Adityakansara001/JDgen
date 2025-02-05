import streamlit as st
from groq import Groq

# Technical roles keywords - expanded to include IT managerial roles
TECHNICAL_KEYWORDS = [
    "engineer", "developer", "architect", "scientist", "analyst",
    "technician", "programmer", "devops", "security", "data",
    "cloud", "network", "system", "ai", "ml", "cyber",
    "software", "hardware", "technical", "it", "sre", "qa",
    "manager", "director", "lead", "project manager", "product manager"
]

client = Groq(api_key="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")

def is_technical_role(job_title):
    """Check if job title contains technical keywords, including IT managerial roles"""
    return any(keyword in job_title.lower() for keyword in TECHNICAL_KEYWORDS)


# Function to polish the prompt 
def polish_input(prompt):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,  # Lower temperature for less creativity
        max_tokens=200,
    )
    return response.choices[0].message.content

# Function to generate the Jd
def generate_jd(prompt):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,  # Higher temperature for creativity
        max_tokens=800,
    )
    return response.choices[0].message.content


# UI Title
st.title("AI Job Description Generator")

# Input Fields
with st.form("job_form"):
    job = st.text_input("Message JD*", placeholder="e.g., Senior Software Engineer")
    submitted = st.form_submit_button("Generate")

if submitted:
    if not job:
         st.error("Please fill required fields (*)")
    else:
        # Immedia Role Validation
        if not is_technical_role(job):
            st.error("❌ Error: We only support job roles within the IT and FinTech industries, including both technical and non-technical positions. Please enter a relevant position (e.g., Software Engineer, Data Scientist, Project Manager, Product Manager).")
            st.stop()

        # Step 1: Polish inputs
        # Proceed with valid technical role   
        with st.spinner("Polishing inputs"):
            polished_input = polish_input(f"Given the job : '{job}', refine and standardize it to be clear and professional, ensuring it aligns with IT & Fintech industry's technical and non technical roles.")


        # Step 2: Generate job description
        with st.spinner("Generating Job Description"):
            prompt = f"""
            Generate a detailed job description strictly for roles in the IT and FinTech industries for a {polished_input}. 
            The description should cover both technical and non-technical positions relevant to these sectors. 
            Exclude any roles that do not pertain to IT or FinTech. 
            Ensure that the responsibilities, qualifications, and skills mentioned are specific to the challenges and requirements of the IT and FinTech environments
            Experience Required: {polished_input}
            Key Skills: {polished_input}
            Qualifications: {polished_input}
            Company Values: {polished_input}

            Ensure clarity, role expectations, and industry standards.

            Structure the output with:
            - Company overview (1 paragraph)
            - Key Responsibilities (bulleted list)
            - Required Skills (bulleted list)
            - Qualifications (bulleted list)
            - Compensation & Benefits section 
            - Inclusion statement aligned with {polished_input}
            """
            output = generate_jd(prompt)

        # Display Polished Input:
        st.subheader("Polished Input")
        st.write(polished_input)

        # Display Job Description
        st.subheader("Generated Job Description")
        st.markdown(output)

        # Download button
        st.download_button("Download as TXT", output, file_name="job_description.txt")
        
        
