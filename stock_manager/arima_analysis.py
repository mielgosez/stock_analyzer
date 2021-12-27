from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import pandas as pd


class ArimaVisualization:
    def __init__(self, model, df_fund, stock_name):
        self.__df_fund = df_fund
        self.__stock_name = stock_name
        self.__model = model

    def get_model(self):
        return self.__model

    def get_df_fund(self):
        return self.__df_fund

    def get_stock_name(self):
        return self.__stock_name

    def set_model(self, model, df_fund, stock_name):
        self.set_df_fund(df_fund)
        self.set_stock_name(stock_name)
        self.__model = model

    def set_df_fund(self, df_fund):
        self.__df_fund = df_fund

    def set_stock_name(self, stock_name):
        self.__stock_name = stock_name

    def plot_residuals(self, kind: str = 'kde'):
        residuals = pd.DataFrame(self.get_model().resid)
        print(residuals.describe())
        residuals.plot(kind=kind)
        plt.show()

    @staticmethod
    def plot_prediction(prediction, test, error, dates):
        plt.plot(dates, test, label="Test Set")
        plt.plot(dates, prediction, color='red', label="Prediction")
        plt.title("MSE: {0}".format(error))
        plt.legend()
        plt.grid()
        plt.show()

    def plot_tsa_decomposition(self):
        result = seasonal_decompose(self.get_df_fund()[self.get_stock_name()], model='multiplicative', freq=1)
        result.plot()
        plt.show()


class ArimaModel:
    def __init__(self, df_fund: pd.DataFrame, stock_name: str):
        self.__df_fund = df_fund
        self.__stock_name = stock_name
        arima_model = ARIMA(df_fund[stock_name], order=(5, 1, 0))
        self.__model = arima_model.fit(disp=0)
        self.plot = ArimaVisualization(model=self.__model, df_fund=df_fund, stock_name=stock_name)

    def get_model(self):
        return self.__model

    def get_df_fund(self):
        return self.__df_fund

    def get_stock_name(self):
        return self.__stock_name

    def set_model(self, df_fund: pd.DataFrame, stock_name: str):
        arima_model = ARIMA(df_fund[stock_name], order=(5, 1, 0))
        self.plot.set_model(arima_model, df_fund, stock_name)
        self.__model = arima_model

    def set_df_fund(self, df_fund: pd.DataFrame):
        self.set_model(df_fund, self.get_stock_name())
        self.__df_fund = df_fund

    def set_stock_name(self, stock_name: str):
        self.set_model(self.get_df_fund(), stock_name)
        self.__stock_name = stock_name

    def predict(self, df_test, verbose: bool = False, plot_prediction: bool = False):
        dates = df_test.index
        test_set = df_test[self.get_stock_name()].values
        history = [x for x in self.get_df_fund()[self.get_stock_name()]]
        predictions = list()
        for t in range(len(test_set)):
            model = ARIMA(history, order=(5, 1, 0))
            model_fit = model.fit(disp=0)
            output = model_fit.forecast()
            y_hat = output[0]
            predictions.append(y_hat)
            obs = test_set[t]
            history.append(obs)
            if verbose:
                print('predicted=%f, expected=%f' % (y_hat, obs))
        error = mean_squared_error(test_set, predictions)
        if verbose:
            print('Test MSE: %.3f' % error)
        if plot_prediction:
            self.plot.plot_prediction(prediction=predictions, test=test_set, error=error, dates=dates)
        return predictions, test_set, error

