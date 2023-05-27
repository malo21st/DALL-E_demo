import streamlit as st
import openai
import requests
from PIL import Image, ImageDraw
import numpy as np

OPENAI_API_KEY = st.secrets.openai_api_key
openai.api_key = OPENAI_API_KEY

def image_create(prompt, size):
    response = openai.Image.create(
    prompt=prompt,
    n=1,
    size=size
    )
    image_url = response['data'][0]['url']
    generated_image = requests.get(image_url).content  # download the image
    with open("img/generated_image.png", "wb") as image_file:
      image_file.write(generated_image)  # write the image to the file
    im_base = Image.open("img/generated_image.png") 
    return im_base

prompt = st.sidebar.text_input('**prompt** (Required)', "")
size = st.sidebar.radio("**size** (Option)", index=1,
                        options=('256x256', '512x512', '1024x1024'))

if prompt:
    im_base = image_create(prompt, size)
    st.image(im_base)

# mask = Image.new("L", im_base.size, 255)
# draw = ImageDraw.Draw(mask)
# draw.ellipse((40, 50, 160, 170), fill=0)
# image_with_transparency = np.dstack((im_base, mask))
# im_mask = Image.fromarray(image_with_transparency)
# im_mask.save('img/mask_image.png')
# st.image(im_mask)


# response = openai.Image.create_edit(
#   image = open("img/generated_image.png", "rb"),
#   mask = open("img/mask_image.png", "rb"),
#   prompt = "UFOが飛んでいる",
#   n=1,
#   size="512x512"
# )
# image_url = response['data'][0]['url']
# generat_edit_image = requests.get(image_url).content  # download the image
# with open("img/generat_edit_image.png", "wb") as image_file:
#     image_file.write(generat_edit_image)  # write the image to the file
# im_edit = Image.open("img/generat_edit_image.png") 
# st.image(im_edit)

# col1, col2, col3 = st.columns(3)
# with col1:
#    st.header("Base")
#    st.image(im_base)
# with col2:
#    st.header("Mask")
#    st.image(im_mask)
# with col3:
#    st.header("Edit")
#    st.image(im_edit)
