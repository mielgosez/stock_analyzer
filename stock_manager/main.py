import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from stock_manager import arima_analysis, data_loader
import tensorflow.keras as keras


def hist_variation(stock_df: pd.DataFrame, variable: str, interval: int = 1, bins: int = 20):
    interval_vec = stock_df[variable] - stock_df[variable].shift(interval)
    interval_vec.plot.hist(bins)
    plt.show()


def plot_correlation(stock_df: pd.DataFrame):
    sns.heatmap(stock_df.corr(), annot=True, fmt=".2f")


if __name__ == '__main__':
    fund_data = data_loader.load_all_data()
    google = fund_data["GOOG"]
    train = google[:500]
    train_diff = pd.DataFrame({'variation_1': (-train.shift(1)+train)/train.shift(1),
                               'variation_2': (-train.shift(2)+train.shift(1))/train.shift(2)})
    std_train = [train_diff.variation_1[(item - 30):item].std() for item in range(60, 500)]
    test = google[500:]
    test_diff = pd.DataFrame({'variation_1': (-test.shift(1)+test)/test.shift(1),
                               'variation_2': (-test.shift(2)+test.shift(1))/test.shift(2)})
    std_test = [test_diff.variation_1[(item-30):item].std() for item in range(60, 500)]
    plt.plot(std_test)
    model = keras.models.Sequential([
        keras.layers.SimpleRNN(20, return_sequence=True, input_shape=[None, 1]),
        keras.layers.SimpleRNN(20),
        keras.layers.Dense(10)
    ])
    # arima_model = arima_analysis.ArimaModel(df_fund=fund_data.iloc[:200, :], stock_name="MSFT")
    # arima_model.predict(df_test=fund_data.iloc[201:, :], plot_prediction=True)
