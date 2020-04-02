import yfinance as yf
import logging
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(level=logging.DEBUG,
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
         #"VISA.VI": 0.0293,
        "INTC": 0.0207,
        "MA": 0.0205,
        "CMCSA": 0.02
    }


def hist_variation(stock_df: pd.DataFrame, variable: str, interval: int=1, bins: int=20):
    interval_vec = stock_df[variable] - stock_df[variable].shift(interval)
    interval_vec.plot.hist(bins)
    plt.show()


def plot_correlation(stock_df: pd.DataFrame):
    sns.heatmap(stock_df.corr(), annot=True, fmt=".2f")


if __name__ == '__main__':
    all_data = dict()
    weight = 0
    time_horizon = 1
    for key, value in data.items():
        weight += value
        asset_info = yf.Ticker(key)
        all_data[key] = asset_info.history(period="1y")["Close"]
        logging.info("Adding {0}".format(key))
        try:
            all_data["fondo"] = all_data["fondo"] + all_data[key]*value
        except KeyError:
            all_data["fondo"] = all_data[key]*value
    all_data["fondo"] = all_data["fondo"]/weight
    all_data = pd.DataFrame(all_data)
    plot_correlation(all_data)
    hist_variation(all_data, "GOOG")