import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

def process_main_page():
    show_main_page()
    show_form()


def show_main_page():
    st.set_page_config(
        layout="wide", page_title="Airline Customer Satisfaction", page_icon=":airplane:")
    '''
    # Предсказание удовлетворённости клиента авиакомпании перелётом
    '''
    image = Image.open('./images/Airline-satisfaction-cover-1-1536x590.png')
    st.image(image, use_column_width=True)


def show_form():
    """
    st.markdown(\"\"\"
    <style>
    .stRadio [role=radiogroup]{
        align:center;
        align-items: center;
        justify-content: center;
    }
    </style\"\"\"
, unsafe_allow_html=True)
    """
    
    with st.form("my_form"):
        cols_count = 5
        columns = st.columns(cols_count)
        st.write("Inside the form")
        values =[0] * cols_count
        for i in range(cols_count):
            with columns[i]:
                values[i] = st.radio(
                    "Set label visibility 👇",
                    ["skip", "1", "2", "3", "4", "5"],
                    key=i,
                    horizontal=True
                )
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("slider", values)


if __name__ == "__main__":
    process_main_page()
