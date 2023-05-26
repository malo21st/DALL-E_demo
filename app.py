import streamlit as st
import openai
import requests
from PIL import Image, ImageDraw

OPENAI_API_KEY = st.secrets.openai_api_key
openai.api_key = OPENAI_API_KEY

response = openai.Image.create(
  prompt="緑の草原と青い空",
  n=1,
  size="512x512"
)
image_url = response['data'][0]['url']
generated_image = requests.get(image_url).content  # download the image
with open("/img/generated_image.png", "wb") as image_file:
    image_file.write(generated_image)  # write the image to the file
im_base = Image.open("/img/generated_image.png") 
st.image(im_base)
