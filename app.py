from dotenv import load_dotenv
load_dotenv() #load al env variables from env files

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv(("GOOGLE_API_KEY")))

#function to load gemini pro

model=genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input, image, prompt):
    response=model.generate_content([input, image[0], prompt])
    return response.text


def input_img_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()
        image_parts=[
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
#initializing the app

st.set_page_config(page_title="Multilanguage Invoice Extractor")

st.header("MultiLanguage Invoice Extractor")
input=st.text_input("Input Prompt: ", key="input")
uploaded_file=st.file_uploader("Choose an image of the invoice ", type=["jpg", "jpeg", "png"])

image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded image.", use_column_width=True )


submit=st.button("Tell me about the invoice")


input_prompt="""
You are an expert in understanding invoices. we will upload a image as invoice and you will
have to answer based on the uploaded invoiice image
"""

#if submit id clicked

if submit:
    image_data=input_img_details(uploaded_file)
    response=get_gemini_response(input_prompt, image_data,input)
    st.subheader("The response is")
    st.write(response)