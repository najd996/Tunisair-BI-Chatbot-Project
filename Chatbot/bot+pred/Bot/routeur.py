from requete import *
from pred import *
from exec import exec
def routeur(obj,intent):
    if intent== "PREDICTION_DEPENSE" or intent== "PREDICTION_PRIX":
        return prediction(obj)
    
    elif intent == "SYNTHESE_ANNUELLE" or intent == "INTENTION_INCONNUE":
        return exec(synthese_annuelle())

    elif intent == "TENDANCE_MENSUELLE":
        return exec(tendance_mensuelle())

    elif intent == "TENDANCE_ANNUELLE":
        return exec(tendance_annuelle())

    elif intent == "CONSOMMATION_MOYENNE_ANNUELLE":
        return exec(consommation_moyenne_annuelle())

    elif intent == "DEPENSE_MOYENNE_ANNUELLE":
        return exec(depense_moyenne_annuelle())
    
    elif intent == "EVOLUTION_DES_PRIX":
        return exec(evolution_des_prix())
    
    elif intent == "DEPENSES_PAR_FOURNISSEUR":
        return exec(depenses_par_fournisseur())
    
    elif intent == "EVOLUTION_DES_TAXES":
        return exec(evolution_des_taxes())
    
    elif intent == "ANALYSE_DES_COUTS":
        return exec(analyse_des_couts())
    
    elif intent == "VOLS_LES_PLUS_CONSOMMATEURS":
        return exec(vols_les_plus_consommateurs())
    elif intent == "OUT_OF_SCOPE":
        return None
    