import base64
import io
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

#Initializing the connection with gemini model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Processing the model
def get_gemini_response(input,pdf_content,prompt):
    model= genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

#Converting PDF to image and scrapping data
def input_pdf_text(uploaded_file):
    if uploaded_file is not None:
        #Convert pdf to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())
        first_page=images[0]
        #convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr,format="JPEG")
        img_byte_arr=img_byte_arr.getvalue()
        
        pdf_parts = [
            {
            "mime_type":"image/jpeg",
            "data":base64.b64encode(img_byte_arr).decode() #encode base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")

#Stramlit App
st.set_page_config(page_title="ATS RESUME Experts")
st.header("ATS Traking System")
input_text=st.text_area("Job Description: ", key="input")
uploaded_file=st.file_uploader("Upload your Resume (PDF)",type=["pdf"])

if uploaded_file is not None:
    st. write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About The Resume")
# submit2 = st.button("How Can I Improvise my Skills")
submit3 = st.button("Percentage Match")

input_prompt1="""
You are an experinced HR with tech experince in the fiels of data science, Full stack web development,
Big data engineering, DEVOPS, Data analyst, your task is to review the provided resume against the job description for these profiles.
Please share your professional evaluation on wheather the candidate's profile align with the role. highlight the strengths and weakness of the applicant in relation
to the specified job requirements.
"""
input_prompt3="""
You are an skilled ATS (Application Tracking System) scanner with a deep understanding of data Science, Full Stack
web development,Big data engineering, DEVOPS, Data analyst and deep ATS funtionality,
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
job description. First the output should come as percentage and then keyword missing and last final thoughts.


"""

if submit1:
    if uploaded_file is not None:
        pdf_content= input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please uploaded the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content= input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please uploaded the resume")



