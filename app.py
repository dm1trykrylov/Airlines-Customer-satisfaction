import streamlit as st
import pandas as pd
import numpy as np

def process_main_page():
    show_main_page()

def show_main_page():
    st.set_page_config(layout="wide", page_title="Airline Customer Satisfaction", page_icon=":airplane:")
    '''
    # Предсказание удовлетворённости клиента авиакомпании перелётом

    Введите результаты опроса
    '''