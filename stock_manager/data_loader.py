import yfinance as yf
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s | %(levelname)s | %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            filemode='w')
data = {
        "MSFT": 0.0904,
        "AAPL": 0.1006,
        "GOOG": 0.0470,
        "T": 0.0271,
        "FB": 0.0537,
        "DIS": 0.0301,
        "VZ": 0.0273,
        "VISA.VI": 0.0293,
        "INTC": 0.0207,
        "MA": 0.0205,
        "CMCSA": 0.02,
        "ADBE.VI": 0.0114,
        "CSCO": 0.0153,
        "NFLX": 0.0150,
        "NVDA": 0.0110,
        "ORCL": 0.0121,
        "QCOM": 0.0157,
        "CRM": 0.0135
    }


def load_all_data():
    all_data = dict()
    weight = 0
    for key, value in data.items():
        weight += value
        asset_info = yf.Ticker(key)
        all_data[key] = asset_info.history(period="10y", interval="1d")["Close"].dropna()
        logging.info("Adding {0}".format(key))
        try:
            all_data["fund"] = all_data["fund"] + all_data[key] * value
        except KeyError:
            all_data["fund"] = all_data[key] * value
    all_data["fund"] = all_data["fund"] / weight
    all_data = pd.DataFrame(all_data)
    all_data.dropna(inplace=True)
    return all_data
