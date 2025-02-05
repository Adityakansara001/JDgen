import streamlit as st
from groq import Groq

client = Groq(api_key="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")

def generate_jd(job_title):

    prompt = f"""
    Generate a detailed, Fomal & professional job description for a {job_title}. 
    Follow this structure:
    Generate job descriptions exclusively only for technical roles within the fintech and technical industries. Ensure the descriptions are precise, industry-specific, and aligned with current market trends. 


If the job title "{job_title}" does not match a recognized standard job title respond with "Please provide a technical or fintech-related job title to generate an appropriate job description"

Follow this structure:
...


    1. **Job Title**: {job_title}
    2. **Experience**: 
    3. **Key Responsibilities**: 5-7 bullet points (tailored to seniority level)
    4. **Required Skills**: 5 bullet points (infer technical/soft skills from the job title)
    5. **Qualifications**: 3-5 bullet points (degrees, certifications, etc. based on seniority)
    6. **Company Culture**: 1-2 sentences emphasizing collaboration and innovation (generic if unknown)
    7. **Compensation & Benefits**: Placeholder text (e.g., "Competitive salary with benefits")

    Guidelines:
    - Assume industry-standard requirements for {job_title}.
    - Avoid generic phrases like "fast-paced environment".
    - Focus on {job_title.split()[-1]} domain (e.g., "Data Scientist" → ML, analytics).
    """
    
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,  # Balance creativity and focus
        max_tokens=800,
    )
    return response.choices[0].message.content

# Streamlit UI
st.title("AI Job Description Generator 🚀")
Prompt = st.text_input(" ", placeholder="Message JD")

if st.button("Generate"):
    if not Prompt:
        st.error("Please enter a job title")
    else:
        with st.spinner("Generating..."):
            jd = generate_jd(Prompt)
            st.markdown(jd)
            st.download_button("Download PDF", jd, file_name=f"{Prompt.replace(' ', '_')}_JD.pdf")