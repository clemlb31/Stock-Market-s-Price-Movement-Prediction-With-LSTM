import yfinance as yf
import pandas as pd
import datetime as dt
import talib
import os

tickers = [
    "AC.PA",   # Accor  
    "AI.PA",   # Air Liquide  
    "AIR.PA",  # Airbus  
    "CS.PA",   # Axa  
    "BNP.PA",  # BNP Paribas  
    "EN.PA",   # Bouygues  
    "BVI.PA",  # Bureau Veritas  
    "CAP.PA",  # Capgemini  
    "CA.PA",   # Carrefour  
    "ACA.PA",  # Crédit Agricole  
    "BN.PA",   # Danone (attention : s'assurer du bon ticker, parfois “BN.PA” peut poser problème selon la source)  
    "DSY.PA",  # Dassault Systèmes  
    "EDEN.PA", # Edenred  
    "ENGI.PA", # Engie  
    "EL.PA",   # EssilorLuxottica  
    "ERF.PA",  # Eurofins Scientific  
    "RMS.PA",  # Hermès (note : sur Yahoo, Hermès peut être “RMS.PA”)  
    "KER.PA",  # Kering  
    "OR.PA",   # L’Oréal  
    "LR.PA",   # Legrand  
    "MC.PA",   # LVMH  
    "ML.PA",   # Michelin  
    "ORA.PA",  # Orange  
    "RI.PA",   # Pernod Ricard  
    "PUB.PA",  # Publicis Groupe  
    "RNO.PA",  # Renault  
    "SAF.PA",  # Safran  
    "SGO.PA",  # Saint-Gobain  
    "SAN.PA",  # Sanofi  
    "SU.PA",   # Schneider Electric  
    "GLE.PA",  # Société Générale  
    "STLAP.PA",# Stellantis  
    "STMPA.PA",# STMicroelectronics (avec le “.PA”)  
    "TEP.PA",  # Teleperformance  
    "HO.PA",   # Thales  
    "TTE.PA",  # TotalEnergies  
    "URW.PA",  # Unibail-Rodamco-Westfield  
    "VIE.PA",  # Veolia Environnement  
    "DG.PA",   # Vinci  
    "VIV.PA"   # Vivendi  
# ,"BOVA11.SA", "BBDC4.SA", "CIEL3.SA", "TIUB4.SA", "PETR4.SA"
]


# ------------------------------------------
# Download 10 years of data
# ------------------------------------------
# data = yf.download(
#     tickers,
#     period="7d",
#     interval="1min",
#     auto_adjust=False
# )
nb_days = 59
def date_max(date1 : dt.datetime,date2 : dt.datetime) -> dt.datetime:
    if date1 > date2:
        return date1.replace(hour=0, minute=0, second=0)
    else:
        return date2.replace(hour=0, minute=0, second=0)

def dl_data(company : str, start_date : dt.datetime, end_date : dt.datetime, interval : str) -> pd.DataFrame:
    if((end_date-start_date).days > 7):
        start_data = dl_data(company ,date_max(start_date, dt.datetime.now() - dt.timedelta(days=nb_days)), start_date + dt.timedelta(days=7), interval)
        end_data = dl_data(company ,start_date + dt.timedelta(days=7), end_date, interval)
        return pd.concat([start_data, end_data])
    else:
        data = yf.Ticker(company)
        data = data.history(start=start_date, end=end_date, interval=interval)
        data.reset_index(inplace=True)
        return data

# Only keep closing prices

if not os.path.exists("data"):
    os.makedirs("data")


for company in tickers:
    data = dl_data(company, dt.datetime.now() - dt.timedelta(days=nb_days), dt.datetime.now(), "15m")
    # count na
    na_count = data.isna().sum().sum()
    if na_count > 0:
        print(f"Na count for {company}: {na_count}")
    data = data.drop(columns=["Dividends","Stock Splits"])
    data.to_csv("data/" + company + ".csv")
