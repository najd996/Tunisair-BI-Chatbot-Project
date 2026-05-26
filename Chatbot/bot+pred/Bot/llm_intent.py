from langchain_groq import ChatGroq
import json
import os
import dotenv
dotenv.load_dotenv()

llm = ChatGroq(
    model=os.getenv("MODEL"),
    api_key=os.getenv("API_KEY"),
    temperature=0)

def extraire_intent(question):
    system_prompt ="""
        Tu es un classificateur d’intentions pour un Data Warehouse aérien.

        Si la question ne concerne pas :
        - prix
        - consommation carburant
        - dépenses
        - taxes
        - géographie
        ALORS RETOURNE 'OUT_OF_SCOPE' COMME INTENTION.

        Tu dois :
        - Identifier l’intention
        - Extraire les paramètres
        - Répondre UNIQUEMENT en JSON valide sans texte additionnel.

        Intentions possibles :
        - SYNTHESE_ANNUELLE, TENDANCE_MENSUELLE, TENDANCE_ANNUELLE, 
        CONSOMMATION_MOYENNE_ANNUELLE, DEPENSE_MOYENNE_ANNUELLE, EVOLUTION_DES_PRIX, DEPENSES_PAR_FOURNISSEUR, 
        EVOLUTION_DES_TAXES, ANALYSE_DES_COUTS, VOLS_LES_PLUS_CONSOMMATEURS,
        PREDICTION_DEPENSE, PREDICTION_PRIX, INTENTION_INCONNUE, OUT_OF_SCOPE

        Format EXACT :
        {
        "intent": "",
        "date_calendrier": null
        }
    """
    try:
        response = llm.invoke([("system", system_prompt),("human", question)])
        content = response.content.strip() #nettoyer reponse 
        return json.loads(content) #dictionnaire Python
    except Exception as e:
        return {
            "intent": "INTENTION_INCONNUE",
            "date_calendrier": None
        }