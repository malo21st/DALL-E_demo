import streamlit as st
import openai
import requests
from PIL import Image, ImageDraw
import numpy as np
import io

OPENAI_API_KEY = st.secrets.openai_api_key
openai.api_key = OPENAI_API_KEY
im_init = Image.open("img_transparency.png")

if "create" not in st.session_state:
    st.session_state["create"] = {"is_img": False, "img": im_init}
if "mask" not in st.session_state:
    st.session_state["mask"] = {"is_img": False, "img": im_init}
if "edit" not in st.session_state:
    st.session_state["edit"] = {"is_img": False, "img": im_init}

def image_to_bytes(img):
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    return img_bytes.getvalue()

def image_create(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size='256x256'
    )
    image_url = response['data'][0]['url']
    generated_image = requests.get(image_url).content  # download the image
    im_create = Image.open(io.BytesIO(generated_image))
    return im_create

def image_edit(prompt):
    create_bytes = image_to_bytes(st.session_state["create"]["img"])
    mask_bytes = image_to_bytes(st.session_state["mask"]["img"])
    response = openai.Image.create_edit(
        image = create_bytes,
        mask = mask_bytes,
        prompt = prompt,
        n=1,
        size='256x256'
    )
    image_url = response['data'][0]['url']
    generated_image = requests.get(image_url).content  # download the image
    im_edit = Image.open(io.BytesIO(generated_image))
    return im_edit

prompt_create = st.sidebar.text_input('**prompt (create)**', "")

if st.session_state["create"]["is_img"] == False and prompt_create == "":
    im_create = image_create(prompt_create)
    st.session_state["create"] = {"is_img": True, "img": im_create}
if st.session_state["create"]["is_img"]:
    prompt_edit = st.sidebar.text_input('**prompt (edit)**', "")
    if prompt_edit:
        im_edit = image_edit(prompt_edit)
        st.session_state["edit"] = {"is_img": True, "img": im_edit}

col1, col2, col3 = st.columns(3)
with col1:
   st.header("Create")
   st.image(st.session_state["create"]["img"])
with col2:
   st.header("Mask")
   st.image(st.session_state["mask"]["img"])
with col3:
   st.header("Edit")
   st.image(st.session_state["edit"]["img"])

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
