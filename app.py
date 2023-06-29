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
    show_radio_buttons()

        
def show_radio_buttons():
    radio_features = ['Inflight wifi service', 'Departure/Arrival time convenient',
                      'Ease of Online booking', 'Gate location', 'Food and drink', 
                      'Online boarding', 'Seat comfort', 'Inflight entertainment',
                      'On-board service', 'Leg room service', 'Baggage handling',
                      'Checkin service', 'Inflight service', 'Cleanliness']
    num_radio_buttons = len(radio_features)
    num_radio_cols = 2
    buttons_per_column = int(np.ceil(num_radio_buttons / num_radio_cols))
    
    with st.form("customer_form"):
        
        #
        age = st.slider("Age",min_value=1, max_value=100, value=20,
                            step=1)
        columns = st.columns(num_radio_cols)
        st.write("Inside the form")
        values = [0] * num_radio_buttons
        for i, label in enumerate(radio_features):
            with columns[i // buttons_per_column]:
                values[i] = st.radio(
                    f"{label}",
                    ["skip", "1", "2", "3", "4", "5"],
                    key=i,
                    horizontal=True
                )
        
        gender = st.selectbox("Gender", ("Male", "Female"))
        # Every form must have a submit button.
        

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("slider", values)

if __name__ == "__main__":
    process_main_page()
