import streamlit as st
import utils
import recipy
from pathlib import Path
from streamlit_extras.switch_page_button import switch_page
from streamlit.source_util import get_pages

st.title("Recipe preparation forms")
st.subheader("Do you have a lot of ingredients and don't know what to do with them?, insert one of those ingredients and select the way of" + \
    " preparation you prefer and I will show you lots of recipes that match your selection.")

ingredient_query = st.text_input("Search ingredients to add to the basket!!")

