import pandas as pd
import numpy as np
from xgboost import XGBRegressor
import pickle

tunisair=pd.read_csv(r'C:\Users\trabe\Desktop\PFE\prediction\consumption_weekly.csv',parse_dates=["week_start"])
tunisair['sem_prc']   = tunisair['cost_usd'].shift(1)
tunisair['mois_prc']  = tunisair['cost_usd'].shift(4)
tunisair['avg_mois_prc']  = tunisair['cost_usd'].rolling(4).mean()
tunisair['avg_trimestre_prc']  = tunisair['cost_usd'].rolling(12).mean()
tunisair['est_ete'] = tunisair['month'].isin([6,7]).astype(int)
tunisair['decembre'] = tunisair['month'].isin([12]).astype(int)
tunisair= tunisair.dropna().reset_index(drop=True)
y=tunisair["cost_usd"]
x=tunisair.drop(["cost_usd", "week_start", "year", "month", "carrier_code", "carrier_name"], axis=1)

modelxgb = XGBRegressor(
    n_estimators=200,
    max_depth=3,
    learning_rate=0.05,
    reg_alpha=0.1,
    reg_lambda=1,
    subsample=0.8,
    random_state=1
)
modelxgb.fit(x,y)

features=["sem_prc","mois_prc","avg_mois_prc","avg_trimestre_prc","est_ete","decembre"]

with open("models/xgb_consommation.pkl", "wb") as f:
    pickle.dump(modelxgb, f)
with open("models/xgb_features.pkl", "wb") as f:
    pickle.dump(features, f)