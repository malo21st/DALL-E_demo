import streamlit as st
import openai
import requests
from PIL import Image, ImageDraw
import numpy as np
import io

OPENAI_API_KEY = st.secrets.openai_api_key
openai.api_key = OPENAI_API_KEY
im_init = Image.open("img_transparency.png")

if "mode" not in st.session_state:
    st.session_state["mode"] = dict()

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
    im_create_a = st.session_state["mode"].get("create", dict()).get("img", im_init)
#     im_create_a.putalpha(alpha=255)
    create_bytes = image_to_bytes(im_create_a)
    mask_bytes = image_to_bytes(st.session_state["mode"].get("mask", dict()).get("img", im_init))
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

def image_variation():
    im_edit = st.session_state["mode"].get("edit", dict()).get("img", im_init)
    edit_bytes = image_to_bytes(im_edit)
    response = openai.Image.create_variation(
        image = edit_bytes,
        n=3,
        size='256x256'
    )
    image_data_lst = response['data']
    im_variation_lst = list()
    for _, image_data in image_data_lst:
        variation_image = requests.get(image_data['url']).content  # download the image
        im_variation = Image.open(io.BytesIO(variation_image))
        im_variation_lst.append(im_variation)
    return im_variation_lst
    
def image_mask(im_base):
    mask = Image.new("L", im_base.size, 255)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((78, 78, 178, 178), fill=0)
    im_array = np.dstack((im_base, mask))
    im_mask = Image.fromarray(im_array)
    return im_mask
    
prompt_create = st.sidebar.text_input('**prompt (create)**', "")

if st.session_state["mode"].get("create", dict()).get("prompt", "") != prompt_create:
    im_create = image_create(prompt_create)
    st.session_state["mode"]["create"] = {"prompt": prompt_create, "img": im_create}
if st.session_state["mode"].get("create", dict()).get("img", False):
    prompt_edit = st.sidebar.text_input('**prompt (edit)**', "")
    if prompt_edit:
        im_mask = image_mask(st.session_state["mode"]["create"]["img"])
        st.session_state["mode"]["mask"] = {"img": im_mask}
        im_edit = image_edit(prompt_edit)
        st.session_state["mode"]["edit"] = {"prompt": prompt_edit, "img": im_edit}

col1, col2, col3 = st.columns(3)
with col1:
   st.header("Create")
   st.image(st.session_state["mode"].get("create", dict()).get("img", im_init))
with col2:
   st.header("Mask")
   st.image(st.session_state["mode"].get("mask", dict()).get("img", im_init))
with col3:
   st.header("Edit")
   st.image(st.session_state["mode"].get("edit", dict()).get("img", im_init))
    
# st.sidebar.write(st.session_state["mode"].get("create", dict()).get("prompt", "None"))
# st.sidebar.write(st.session_state["mode"].get("mask", dict()).get("prompt", "None"))
# st.sidebar.write(st.session_state["mode"].get("edit", dict()).get("prompt", "None"))
