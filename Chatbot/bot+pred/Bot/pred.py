
import requests

def prediction(objet):
    date_pred=objet.get("date_calendrier")
    if not date_pred:
        date_pred="format non valide"
    intent=objet.get("intent")
    if intent == "prediction_depense" :
        url = "http://localhost:8000/prediction_depense" 
    elif intent == "prediction_prix" :
        url = "http://localhost:8000/prediction_prix"
    else :
        return {"erreur": "Intent non supportée pour la prédiction."}
    try:
        response = requests.post(
                url,
                json={"date_pred": date_pred}
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"erreur": f"Erreur de connexion à l'API: {str(e)}"}

