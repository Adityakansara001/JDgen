import streamlit as st
from groq import Groq

# Initialize Groq client
client = Groq(api_key="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")

# Function to polish inputs
def polish_input(prompt):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,  # Lower temperature for less creativity
        max_tokens=200,
    )
    return response.choices[0].message.content

# Function to generate job description
def generate_job_description(prompt):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,  # Higher temperature for creativity
        max_tokens=800,
    )
    return response.choices[0].message.content

# UI Title
st.title("AI Powered JD Generator 🚀")

# Input fields
with st.form("job_form"):
    job_title = st.text_input("Job Title*", placeholder="e.g., Senior Software Engineer")
    experience = st.selectbox("Experience*", ["1-3 years", "3-5 years", "5+ years"])
    industry = st.selectbox("Industry*", ["Tech", "Healthcare", "Finance", "Other"])
    employment_type = st.selectbox("Employment Type*", ["Full-Time", "Part-Time", "Contract"])
    submitted = st.form_submit_button("Generate")

if submitted:
    if not job_title :
        st.error("Please fill required fields (*)")
    else:
        # Step 1: Generate job description
        with st.spinner("Generating job description..."):
            prompt = f"""
            Generate a job description for: {job_title} ({employment_type}) in the {industry} industry.
            Experience Required: {experience}
           
            

            Structure the output with:
            - Company overview (1 paragraph)
            - Key Responsibilities (bulleted list)
            - Required Skills (bulleted list)
            - Qualifications (bulleted list)
            - Compensation & Benefits section
            - Inclusion statement aligned with company core values
            """
            output = generate_job_description(prompt)

   

        # Display job description
        st.subheader("Generated Job Description")
        st.markdown(output)

        # Download button
        st.download_button("Download as TXT", output, file_name="job_description.txt")