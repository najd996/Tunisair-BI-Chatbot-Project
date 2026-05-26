# agent.py
import json
import os
import dotenv
from groq import Groq

from requete import *
from pred import prediction
from exec import exec
from llm_interpret import interpret
from tools import TOOLS

dotenv.load_dotenv()

# client groq dupporte les tools mieux que langchain 
groq_client = Groq(api_key=os.getenv("API_KEY"))
MODEL = os.getenv("MODEL")

system_prompt = """Tu es un assistant BI senior spécialisé en analyse carburant aviation pour TUNISAIR.

Tu réponds UNIQUEMENT en appelant les tools disponibles.
Ne génère jamais de chiffres toi-même.
Ne réponds jamais sans appeler au moins un tool si la question concerne 
prix, consommation, dépenses, taxes, vols ou prévisions.
REGLE CRITIQUE : 
Si une question contient plusieurs axes d'analyse
(ex: fournisseurs ET prix, consommation ET dépenses, taxes ET tendance),
tu DOIS appeler TOUS les tools correspondants simultanément.
Ne jamais répondre avec un seul tool si la question en implique plusieurs.

Tu réponds UNIQUEMENT en appelant les tools disponibles.
Ne génère jamais de chiffres toi-même.
Si la question est hors périmètre : réponds directement sans tool."""


# ── Mapping tool_name → fonction Python
def _dispatch(tool_name, tool_args):
    #choix du tool
    handlers_sql = {
        "synthese_annuelle"           : synthese_annuelle,
        "tendance_mensuelle"          : tendance_mensuelle,
        "tendance_annuelle"           : tendance_annuelle,
        "consommation_moyenne_annuelle": consommation_moyenne_annuelle,
        "depense_moyenne_annuelle"    : depense_moyenne_annuelle,
        "evolution_des_prix"          : evolution_des_prix,
        "depenses_par_fournisseur"    : depenses_par_fournisseur,
        "evolution_des_taxes"         : evolution_des_taxes,
        "analyse_des_couts"           : analyse_des_couts,
        "vols_les_plus_consommateurs" : vols_les_plus_consommateurs,
    }

    # tool sql
    if tool_name in handlers_sql:
        requetes = handlers_sql[tool_name]()
        return exec(requetes)

    # tool pred
    elif tool_name in ("prediction_depense", "prediction_prix"):
        obj = {
            "intent"          : tool_name,
            "date_calendrier" : tool_args.get("date_calendrier")
        }
        return prediction(obj)

    return {"error": f"Tool inconnu : {tool_name}"}


def run_agent(question):
    """
    Pipeline complet :
    1. LLM choisit le(s) tool(s)
    2. Exécution des tools choisis
    3. LLM interprète les résultats
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": question},
    ]

    # ── ÉTAPE 1 : LLM sélectionne les tools
    response = groq_client.chat.completions.create(
        model       = MODEL,
        messages    = messages,
        tools       = TOOLS,
        tool_choice = "auto",
        temperature = 0,
    )

    msg        = response.choices[0].message
    tool_calls = msg.tool_calls or []

    # ── Pas de tool → question hors périmètre
    if not tool_calls:
        return {
            "question" : question,
            "tools": [],
            "resultat": None,
            "response"  : msg.content,
        }

    # ── ÉTAPE 2 : Exécuter chaque tool
    intent = None
    all_results = {}
    tool_messages = []

    for call in tool_calls:
        name   = call.function.name
        if intent is None:
            intent = name
        args   = json.loads(call.function.arguments)
        result = _dispatch(name, args)

        all_results[name] = result

        tool_messages.append({
            "role"        : "tool",
            "tool_call_id": call.id,
            "name"        : name,
            "content"     : json.dumps(result, ensure_ascii=False, default=str),
        })

    # ── ÉTAPE 3 : LLM interprète les résultats
    reponse = interpret(question, all_results)

    return {
        "question"     : question,
        "intent": intent,
        "tools": [c.function.name for c in tool_calls],
        "resultat"    : all_results,
        "response"      : reponse,
    }