import streamlit as st
import pandas as pd
import numpy as np
import json
from PIL import Image
from model import load_model_and_predict, encode_radio_input
from st_btn_select import st_btn_select

LANG = 'ru'
TRANSLATIONS_FILE = 'translations.json'

def process_main_page():
    st.set_page_config(
        layout="wide", page_title="Airline Customer Satisfaction", page_icon=":airplane:")
    show_language_selector()
    show_main_page()
    show_form()


def show_main_page():
    with open(TRANSLATIONS_FILE, 'r') as f:
        headers = json.load(f)[LANG]['paragraphs']
    st.title(headers['title'])
    image = Image.open('./images/Airline-satisfaction-cover-1-1536x590.png')
    st.image(image, use_column_width=True)
    st.subheader(headers['instructions'])


def show_language_selector():
    with st.sidebar:
        global LANG
        LANG = st_btn_select(('ru', 'en'))

def show_form():
    """
    Форма для сбора информации о полёте
    """
    show_buttons()


def show_buttons():
    # Характеристики полёта (как в датасете)
    features = ['Gender', 'Age', 'Customer Type', 'Type of Travel', 'Class',
                'Flight Distance', 'Departure Delay in Minutes', 'Arrival Delay in Minutes',
                'Inflight wifi service', 'Departure/Arrival time convenient',
                'Ease of Online booking', 'Gate location', 'Food and drink',
                'Online boarding', 'Seat comfort', 'Inflight entertainment',
                'On-board service', 'Leg room service', 'Baggage handling',
                'Checkin service', 'Inflight service', 'Cleanliness']
    radio_features = features[8:]
    # Вопросы, в которых предполагается оценка 0-5. Они будут распределены по столбцам
    user_df = pd.DataFrame(columns=features)
    user_df.loc[0] = [' '] * len(features)
    num_radio_buttons = len(radio_features)
    num_radio_cols = 2
    buttons_per_column = int(np.ceil(num_radio_buttons / num_radio_cols))
    with open(TRANSLATIONS_FILE, 'r') as f:
        feature_names = json.load(f)[LANG]['features']
    with st.form("customer_form"):
        columns = st.columns(num_radio_cols)
        user_input = dict()
        for i, label in enumerate(radio_features):
            with columns[i // buttons_per_column]:
                label_ru = feature_names[label]
                user_input[label] = st.radio(
                    f"{label_ru}",
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

        user_df.at[0,'Age'] = st.slider(feature_names["Age"], min_value=1, max_value=100, value=20,
                                      step=1)
        for key, value in categorial_feature_options.items():
            user_df.at[0,key] = st.selectbox(feature_names[key], value)
        user_df.at[0, 'Flight Distance'] = st.number_input(
            feature_names["Flight Distance"], min_value=0, max_value=16000)
        user_df.at[0, 'Departure Delay in Minutes'] = st.number_input(
            feature_names["Departure Delay in Minutes"], min_value=0, max_value=1440)
        user_df.at[0, 'Arrival Delay in Minutes'] = st.number_input(
            feature_names["Arrival Delay in Minutes"], min_value=0, max_value=1440)

        with open(TRANSLATIONS_FILE, 'r') as f:
            headers = json.load(f)[LANG]['paragraphs']
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write(headers['raw_df'], user_df.head())
            show_prediction(user_df)


def show_prediction(X: pd.DataFrame):
    with open(TRANSLATIONS_FILE, 'r') as f:
       headers = json.load(f)[LANG]['paragraphs']
    prediction, probs = load_model_and_predict(X, LANG)
    st.subheader(headers['prediction'])
    if prediction == 0:
        message = headers['dissatisfied']
    else:
        message = headers['satisfied']
    st.write(message)
    st.write(headers['probabilities'], probs)


if __name__ == "__main__":
    process_main_page()
