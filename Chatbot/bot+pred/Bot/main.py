from fastapi import FastAPI, HTTPException
from agent_bi import run_agent
import pickle
import pandas as pd
import numpy as np
from pydantic import BaseModel
from datetime import timedelta
from keras.models import load_model
from llm_interpret import interpret 
from connexiondb import get_db_connection
from typing import List

class datereq(BaseModel):
    date_pred:str
class ChatRequest(BaseModel):
    question: str
class FeedbackData(BaseModel):
    question: str
    reponse: str
    type: str
    intents: List[str]

app = FastAPI()

#importation des modèles

with open("C:\\Users\\DELL\\Desktop\\Stage\\chatbot\\bot+pred\\models\\xgb_consommation.pkl", "rb") as f:
    model = pickle.load(f)

with open("C:\\Users\\DELL\\Desktop\\Stage\\chatbot\\bot+pred\\models\\xgb_features.pkl", "rb") as f:
    features = pickle.load(f)
with open("C:\\Users\\DELL\\Desktop\\Stage\\chatbot\\bot+pred\\models\\scaler_price.pkl", "rb") as f:
        scaler = pickle.load(f)
with open("C:\\Users\\DELL\\Desktop\\Stage\\chatbot\\bot+pred\\models\\window.pkl", "rb") as f:
        window = pickle.load(f)
model_lstm = load_model("C:\\Users\\DELL\\Desktop\\Stage\\chatbot\\bot+pred\\models\\lstm_price.keras")

#importation des données historiques

historique = pd.read_csv("C:\\Users\\DELL\\Desktop\\Stage\\chatbot\\bot+pred\\consumption_weekly.csv",parse_dates=["week_start"])
historiquelstm = pd.read_csv("C:\\Users\\DELL\\Desktop\\Stage\\chatbot\\bot+pred\\jet_fuel_prices.csv",parse_dates=["date"])

def create_features_auto(df):
    df = df.copy()
    df['sem_prc'] = df['cost_usd'].shift(1)
    df['mois_prc'] = df['cost_usd'].shift(4)
    df['avg_mois_prc'] = df['cost_usd'].rolling(4).mean()
    df['avg_trimestre_prc'] = df['cost_usd'].rolling(12).mean()
    df['est_ete'] = df['month'].isin([6,7]).astype(int)
    df['decembre'] = df['month'].isin([12]).astype(int)
    df = df.dropna().reset_index(drop=True)
    return df

@app.get("/")
def home():
    return {"message": "Bienvenue sur Chatbot BI !"}


@app.post("/prediction_depense")
def depense_hebdommadaire(data: datereq):
    global historique

    try:
        date_prediction = pd.to_datetime(data.date_pred)
    except ValueError:
        return {"Format de date invalide"}
    
    current_date = historique['week_start'].max()
    if date_prediction <= current_date:
        return {
            "message": "Date déjà couverte",
            "last_date": str(current_date)
        }
    else :
        if date_prediction - current_date < timedelta(weeks=1):
            return {
                "date_prediction": str(date_prediction),
                "current_prediction": float(historique['cost_usd'].iloc[-1]),
                "noté_bien ": "les prédictions sont hebdommadaire"
            }
    df = historique.copy()

    max_steps =12
    steps = 0

    while current_date < date_prediction and date_prediction - current_date >= timedelta(weeks=1):

        df_feat = create_features_auto(df)
        X = df_feat[features].tail(1)

        pred = model.predict(X)[0]

        current_date += timedelta(weeks=1)

        new_row = df.iloc[-1].copy()
        new_row["week_start"] = current_date
        new_row["cost_usd"] = pred

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        steps += 1
    rmse_xgb = 0.135
    rmse_ajusté=  rmse_xgb *(1 + (0.1*steps))
    min_pred=pred*(1-rmse_ajusté)
    max_pred= pred*(1+rmse_ajusté)
    return {
        "date_prediction": str(date_prediction),
        "prediction":float(pred),
        "noté_bien ": "les prédictions sont hebdommadaire en USD",
        "interval": f"dépenses comprises entre [{min_pred:.2f}, {max_pred:.2f}]"
    }

@app.post("/prediction_prix")
def prix_carburant_hebdommadaire(data: datereq):
    global historiquelstm
    try:
        date_prediction = pd.to_datetime(data.date_pred)
    except ValueError:
        return {"Format de date invalide"}
    current_date = historiquelstm['date'].max()
    if date_prediction <= current_date:
        return {
            "message": "Date déjà couverte",
            "last_date": str(current_date)
        }
    else :
        if date_prediction - current_date < timedelta(weeks=1):
            return {
                "date_prediction": str(date_prediction),
                "current_prediction": float(historiquelstm['price_usd_per_gallon'].iloc[-1]),
                "noté_bien ": "les prédictions sont hebdommadaire"
            }
    df= historiquelstm.copy()
    max_steps = 12
    steps = 0  
    while current_date < date_prediction and date_prediction - current_date >= timedelta(weeks=1):
        if steps > max_steps:
            return {"Date trop éloignée, max 3 mois à l'avance."}
        last_window = df['price_usd_per_gallon'].values[-window:]
        last_window_scaled = scaler.transform(last_window.reshape(-1, 1)).reshape(1, window, 1)
        pred_scaled = model_lstm.predict(last_window_scaled)
        pred = scaler.inverse_transform(pred_scaled)[0][0]
        current_date += timedelta(weeks=1)
        new_row = df.iloc[-1].copy()
        new_row["date"] = current_date
        new_row["price_usd_per_gallon"] = pred
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        steps += 1

    rmse_lstm = 0.055
    rmse_ajusté=  rmse_lstm *(1 + (0.1*steps))
    min_pred=pred*(1-rmse_ajusté)
    max_pred= pred*(1+rmse_ajusté)
    return {
        "date_prediction": str(date_prediction),
        "prediction": float(pred),
        "noté_bien ": "les prédictions sont hebdommadaire en USD/GALLON",
        "interval": f"le prix compris entre[{min_pred:.2f}, {max_pred:.2f}]"
    }
@app.post('/chat')
def ask(request: ChatRequest): 
    try:
        return run_agent(request.question)
    except Exception as e:
        return {
            "intent": "ERROR",
            "response": "Erreur au niveau du serveur. Veuillez réessayer plus tard.",
            "resultat": None
        }
    
@app.post("/feedback")
def save_feedback(data: FeedbackData):
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        sql = """INSERT INTO CHATBOT_FEEDBACK (QUESTION, REPONSE, FEEDBACK_TYPE, INTENT) 
                 VALUES (:1, :2, :3, :4)"""

        for intent in data.intents:
            cursor.execute(
                sql,
                [data.question, data.reponse, data.type, intent]
            )

        connection.commit()
        cursor.close()

        return {"status": "success", "message": "Feedback enregistré"}

    except Exception as e:
        print(f"Erreur Oracle: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de l'insertion")

    finally:
        if connection:
            connection.close()

