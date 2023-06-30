import pickle
import pandas as pd
import streamlit as st
from sklearn.preprocessing import StandardScaler, LabelEncoder, OrdinalEncoder, MinMaxScaler

PATH_TO_MODEL = 'models/CatBoostClassifier.pickle'


def encode_features(df: pd.DataFrame) -> pd.DataFrame:
    """ 
    encoderfile = 'encoder.sav'
    with open('models/' + encoderfile, 'rb') as f:
        ordinal_encoder = pickle.load(f)
        ordinal_columns = ['Customer Type', 'Class', 'Gender']
        df[ordinal_columns] = ordinal_encoder.transform(df[ordinal_columns])
    """
    #df.drop('Gender', axis=1, inplace=True)
    df_full = pd.read_csv('./datasets/clients.csv')
    df_full.drop(['id'], axis=1, inplace=True)
    df_full.dropna(inplace=True)
    df_full.drop(df_full[df_full['satisfaction'] == '-'].index, inplace=True)
    ordinal_encoder = OrdinalEncoder()
    ordinal_columns = ['Customer Type', 'Class', 'Gender']
    ordinal_encoder = ordinal_encoder.fit(df_full[ordinal_columns])
    
    df[ordinal_columns] = ordinal_encoder.transform(df[ordinal_columns])
    df_full[ordinal_columns] = ordinal_encoder.transform(df_full[ordinal_columns])
    
    df = pd.get_dummies(data=df, prefix=['Travel'], columns=['Type of Travel'])
    df_full = pd.get_dummies(data=df_full, prefix=['Travel'], columns=['Type of Travel'])
    if 'Travel_Business travel' not in df.columns:
        df['Travel_Business travel'] = [0]
    else:
        df['Travel_Personal Travel'] = [0]
    scalerfile = 'scaler.sav'
    with open('models/' + scalerfile, 'rb') as f:
        print("Success!\n")
        #scaler = pickle.load(f)
        #df = pd.DataFrame(scaler.transform(df), columns=df.columns)
    scaler = MinMaxScaler()
    scaler.fit(df_full.drop(['satisfaction'], axis=1))
    df = pd.DataFrame(scaler.transform(df), columns=df.columns)
    return df


def encode_radio_input(input: str) -> int:
    return 0 if input == "skip" else int(input)


def load_model_and_predict(df, path=PATH_TO_MODEL):
    df = encode_features(df)
    st.write(df.head())
    df.to_csv('test.csv')
    with open(path, "rb") as f:
        model = pickle.load(f)
        #st.write(df.info())
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
