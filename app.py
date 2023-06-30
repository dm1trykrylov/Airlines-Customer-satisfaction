import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from model import load_model_and_predict, encode_radio_input


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
    features = ['Gender', 'Age', 'Customer Type', 'Type of Travel', 'Class',
                'Flight Distance', 'Departure Delay in Minutes', 'Arrival Delay in Minutes',
                'Inflight wifi service', 'Departure/Arrival time convenient',
                'Ease of Online booking', 'Gate location', 'Food and drink',
                'Online boarding', 'Seat comfort', 'Inflight entertainment',
                'On-board service', 'Leg room service', 'Baggage handling',
                'Checkin service', 'Inflight service', 'Cleanliness']
    radio_features = features[8:]
    user_df = pd.DataFrame(columns=features)
    #st.write(user_df.head())
    user_df.loc[0] = [' '] * len(features)
    #st.write(user_df.head())
    num_radio_buttons = len(radio_features)
    num_radio_cols = 2
    buttons_per_column = int(np.ceil(num_radio_buttons / num_radio_cols))

    user_input = dict()
    with st.form("customer_form"):

        #
        columns = st.columns(num_radio_cols)
        #st.write("Inside the form")

        for i, label in enumerate(radio_features):
            with columns[i // buttons_per_column]:
                user_input[label] = st.radio(
                    f"{label}",
                    ["skip", "1", "2", "3", "4", "5"],
                    key=i,
                    horizontal=True
                )
                user_input[label] = encode_radio_input(user_input[label])
                user_df.at[0, label] = user_input[label]
        categorial_feature_options = {
            'Gender': ('Male', 'Female'),
            'Customer Type': ('Loyal Customer', 'disloyal Customer'),
            'Type of Travel': ('Business travel', 'Personal Travel'),
            'Class': ('Business', 'Eco Plus', 'Eco'),
        }

        user_df.at[0,'Age'] = st.slider("Age", min_value=1, max_value=100, value=20,
                                      step=1)
        for key, value in categorial_feature_options.items():
            user_df.at[0,key] = st.selectbox(key, value)
        user_df.at[0, 'Flight Distance'] = st.number_input(
            "Flight Distance", min_value=0, max_value=16000)
        user_df.at[0, 'Departure Delay in Minutes'] = st.number_input(
            "Departure Delay in Minutes", min_value=0, max_value=1440)
        user_df.at[0, 'Arrival Delay in Minutes'] = st.number_input(
            "Arrival Delay in Minutes", min_value=0, max_value=1440)

        submitted = st.form_submit_button("Submit")
        if submitted:
            #for key, value in user_input.items():
            #    user_input[key] = [value]
            #user_df.append(user_input)
            st.write("Your data:", user_df.head())
            show_prediction(user_df)


def show_prediction(X):
    prediction, probs = load_model_and_predict(X)
    st.write(prediction)
    st.write(probs)


if __name__ == "__main__":
    process_main_page()
