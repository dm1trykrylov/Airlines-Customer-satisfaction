import pickle
import pandas as pd
import streamlit as st
from sklearn.preprocessing import StandardScaler, LabelEncoder, OrdinalEncoder, MinMaxScaler

PATH_TO_MODEL = 'models/CatBoostClassifier.pickle'


def encode_features(df: pd.DataFrame) -> pd.DataFrame:
    encoderfile = 'encoder.sav'
    with open('models/' + encoderfile, 'rb') as f:
        ordinal_encoder = pickle.load(f)
        ordinal_columns = ['Customer Type', 'Class', 'Gender']
        df[ordinal_columns] = ordinal_encoder.transform(df[ordinal_columns])
    df = pd.get_dummies(data=df, prefix=['Travel'], columns=['Type of Travel'])
    if not ('Travel_Business travel' in df.columns):
        df['Travel_Business travel'] = [0]
        swap_columns(df, 'Travel_Business travel', 'Travel_Personal Travel')  
    else:
        df['Travel_Personal Travel'] = [0]
    st.write(df.head())
    scalerfile = 'scaler.sav'
    with open('models/' + scalerfile, 'rb') as f:
        print("S!\n")
        scaler = pickle.load(f)
        df = pd.DataFrame(scaler.transform(df), columns=df.columns)
    return df


def encode_radio_input(input: str) -> int:
    return 0 if input == "skip" else int(input)


def swap_columns(df, col1, col2):
    """
    Функция, позволяющая поменять местами два столбца таблицы
    """
    # Названия столбцов
    cols = df.columns
    
    # Индексы столбцов, которые нужно поменять
    col1_idx = cols.get_loc(col1)
    col2_idx = cols.get_loc(col2)
    
    # Перестановка двух столбцов по индексам
    df[[cols[col1_idx], cols[col2_idx]]] = df[[cols[col2_idx], cols[col1_idx]]]
    
    # Переименование столбцов
    df.rename(columns = {col1:col2, col2:col1}, inplace = True)

def load_model_and_predict(df, path=PATH_TO_MODEL):
    df = encode_features(df)
    st.write(df.head())
    df.to_csv('test.csv')
    with open(path, "rb") as f:
        model = pickle.load(f)
        # st.write(df.info())
        prediction = model.predict(df)
        # prediction = np.squeeze(prediction)
        prediction_proba = model.predict_proba(df)
        # prediction_proba = np.squeeze(prediction_proba)
    return prediction, prediction_proba


"""
    encode_prediction_proba = {
        0: "Вам не повезло с вероятностью",
        1: "Вы выживете с вероятностью"
    }

    encode_prediction = {
        0: "Сожалеем, вам не повезло",
        1: "Ура! Вы будете жить"
    }

    prediction_data = {}
    for key, value in encode_prediction_proba.items():
        prediction_data.update({value: prediction_proba[key]})

    prediction_df = pd.DataFrame(prediction_data, index=[0])
    prediction = encode_prediction[prediction]

    return prediction, prediction_df
"""
