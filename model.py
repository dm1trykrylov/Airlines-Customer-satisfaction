import pickle
import pandas as pd
import streamlit as st
from sklearn.preprocessing import StandardScaler, LabelEncoder, OrdinalEncoder, MinMaxScaler


def encode_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Кодировка категориальных признаков и масштабирование
    """
    encoderfile = 'encoder.sav'
    ordinal_encoder = load_encoder('models/' + encoderfile)
    ordinal_columns = ['Customer Type', 'Class', 'Gender']
    df[ordinal_columns] = ordinal_encoder.transform(df[ordinal_columns])
    df = pd.get_dummies(data=df, prefix=['Travel'], columns=['Type of Travel'])
    if not ('Travel_Business travel' in df.columns):
        df['Travel_Business travel'] = [0]
        swap_columns(df, 'Travel_Business travel', 'Travel_Personal Travel')
    else:
        df['Travel_Personal Travel'] = [0]
    scalerfile = 'scaler.sav'
    scaler = load_scaler('models/' + scalerfile)
    df = pd.DataFrame(scaler.transform(df), columns=df.columns)
    return df


@st.cache_data
def load_encoder(path):
    with open(path, 'rb') as f:
        # Используется кодировщик, обученный на данных из датасета
        encoder = pickle.load(f)
    return encoder


@st.cache_data
def load_scaler(path):
    with open(path, 'rb') as f:
        # Используется масштабирование с обучением на датасете
        scaler = pickle.load(f)
    return scaler


def encode_radio_input(input: str) -> int:
    """ 
    Кодирование ответов 'skip', 1-5 в 0-5
    """
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
    df.rename(columns={col1: col2, col2: col1}, inplace=True)


# Используется модель, показавшая наилучший результат - CatBoost Classifier
PATH_TO_MODEL = 'models/CatBoostClassifier.pickle'


@st.cache_data
def load_model_and_predict(df, path=PATH_TO_MODEL):
    """
    Загрузка обученной модели и получение предсказаний для пользовательских данных
    """
    df = encode_features(df)
    st.write("Данные из анкеты после кодировки и масштабирования:", df.head())
    df.to_csv('test.csv')
    model = load_model()
    prediction = model.predict(df)
    prediction_proba = model.predict_proba(df)
    return prediction, prediction_proba


@st.cache_data
def load_model(path=PATH_TO_MODEL):
    with open(path, "rb") as f:
        model = pickle.load(f)
    return model
