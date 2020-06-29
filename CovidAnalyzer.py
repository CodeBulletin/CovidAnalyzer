from CovidTracker import CovidTracker
from datetime import datetime, timedelta
import numpy as np
import plotly
import plotly.graph_objs as go
from scipy.optimize import curve_fit
from random import uniform


class CovidAnalyzer:
    def __init__(self, Tracker: CovidTracker):
        self.Tracker = Tracker
        self.data: dict = {}
        self.predicted_data = {}
        self.pDays = []
        self.fitted_data: dict = {}
        self.fitted_data_log: dict = {}
        self.pop_size = 0
        self.ExtractData()

    def set_location(self, country: str, pr=False):
        self.Tracker.setTrackerLocation(country, pr=pr)
        self.ExtractData()

    def ExtractData(self):
        self.data = self.Tracker.getDataList()
        self.pop_size = self.Tracker.getTotalPopulation()
        if self.pop_size == 0:
            self.pop_size = 8000000000

    def Analyze_data(self, Prediction_days=3, pr=False):
        if pr:
            print("Analyzing")
        keys = list(self.data.keys())
        temp: dict = {}
        for i in keys:
            if i == "Dates":
                self.data[i] = [datetime.strptime((j + " 2020").replace(" ", "-"), "%b-%d-%Y") for j in self.data[i]]
            if self.data[i]:
                temp[i] = self.data[i]
        self.data = temp
        keys = list(self.data.keys())
        days_data = CovidAnalyzer.ConvertDates(self.data["Dates"])
        data_fit_log = {}
        data_fit = {}
        for i in keys:
            if i not in ['NewCasesPerDay', 'DeathPerDay', 'RecoveredPerDay',
                         'RecoveryPercentage', 'DeathPercentage', 'Dates']:
                data_fit_log[i], _ = curve_fit(CovidAnalyzer.FunctionLog, days_data,
                                               CovidAnalyzer.null_inf(np.log(CovidAnalyzer.safe_log(self.data[i]))),
                                               maxfev=100000, absolute_sigma=True, sigma=[0.001 for _ in days_data],
                                               p0=[uniform(0, 0.00005) for _ in range(28)],
                                               bounds=[0, np.log(self.pop_size)])
                data_fit[i], _ = curve_fit(CovidAnalyzer.Function, days_data, self.data[i],
                                           maxfev=100000, absolute_sigma=True, sigma=[0.001 for _ in days_data],
                                           p0=[uniform(0, 0.00005) for _ in range(28)],
                                           bounds=[0, np.log(self.pop_size)])
            self.fitted_data_log = data_fit_log
            self.fitted_data = data_fit
        self.predicted_data, self.pDays = self.GeneratePredictions(Prediction_days)
        if pr:
            print("Completed")

    def GeneratePredictions(self, Prediction_Days=7):
        days = self.data["Dates"].copy()
        for i in range(Prediction_Days):
            days.append(days[len(days)-1] + timedelta(days=1))
        days_float = np.array(CovidAnalyzer.ConvertDates(days))
        PredictedValue = {}
        for i in list(self.fitted_data.keys())[::-1]:
            a = np.round(np.exp(CovidAnalyzer.FunctionLog(days_float, *self.fitted_data_log[i])))
            b = np.round(CovidAnalyzer.Function(days_float, *self.fitted_data[i]))
            z = 0
            w = 0
            for j in range(len(self.data[i])):
                z += 1
                if pow(a[j] - self.data[i][j], 2) > pow(b[j] - self.data[i][j], 2):
                    w += 1
                else:
                    w = 0
                if w > 3:
                    break
            PredictedValue[i] = np.append(a[:z], b[z:])
            if i == 'TotalCases':
                PredictedValue['NewCasesPerDay'] = [PredictedValue[i][j + 1] - PredictedValue[i][j] for j
                                                    in range(len(PredictedValue[i]) - 1)]
                self.clean(PredictedValue['NewCasesPerDay'], 'NewCasesPerDay')
            if i == 'TotalDeath':
                PredictedValue['DeathPerDay'] = [PredictedValue[i][j + 1] - PredictedValue[i][j] for j
                                                 in range(len(PredictedValue[i]) - 1)]
                self.clean(PredictedValue['DeathPerDay'], 'DeathPerDay')
            if i == 'TotalRecovered':
                PredictedValue['RecoveredPerDay'] = [PredictedValue[i][j + 1] - PredictedValue[i][j] for j
                                                     in range(len(PredictedValue[i]) - 1)]
                self.clean(PredictedValue['RecoveredPerDay'], 'RecoveredPerDay')
        return PredictedValue, days

    def clean(self, x, element):
        for i in range(len(self.data[element])):
            if x[i] < 0:
                x[i] = self.data[element][i]

    @staticmethod
    def ConvertDates(dates, mode=False, min_date=None):
        if not mode:
            return [CovidAnalyzer.ConvertDateToTimestamp(dates[0], i) for i in dates]
        elif min_date:
            return [CovidAnalyzer.ConvertTimestampToDate(min_date, i) for i in dates]

    def ShowData(self):
        days = self.data["Dates"]
        trace = []
        for i in list(self.data.keys())[1:]:
            if len(days) == len(self.data[i]):
                trace.append(go.Scatter(x=days, y=self.data[i], mode="lines+markers", name=i))
            elif len(days) > len(self.data[i]):
                trace.append(go.Scatter(x=days[1:], y=self.data[i], mode="lines+markers", name=i))
        for i in list(self.predicted_data.keys()):
            if len(self.pDays) == len(self.predicted_data[i]):
                trace.append(go.Scatter(x=self.pDays, y=self.predicted_data[i],
                                        mode="lines+markers", name=i+"Predicted"))
            elif len(self.pDays) > len(self.predicted_data[i]):
                trace.append(go.Scatter(x=self.pDays[1:], y=self.predicted_data[i],
                                        mode="lines+markers", name=i+"Predicted"))
        update_menus = list([
            dict(active=1,
                 buttons=list([
                     dict(label='Log Scale',
                          method='update',
                          args=[{'visible': [True for _ in range(len(trace))]},
                                {'yaxis': {'type': 'log'}}]),
                     dict(label='Linear Scale',
                          method='update',
                          args=[{'visible': [True for _ in range(len(trace))]},
                                {'yaxis': {'type': 'linear'}}])
                 ]),
                 direction='down',
                 pad={'r': 10, 't': 10},
                 showactive=True,
                 x=0.2,
                 xanchor='center',
                 y=1.1,
                 yanchor='middle'
                 ),
        ])

        data = trace
        layout = dict(updatemenus=update_menus, title=f'Covid19 {self.Tracker.data[1]}')
        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig)

    def make_prediction(self, float_date, date):
        keys = list(self.fitted_data.keys())
        print("-------------------------------------")
        if "TotalCases" in keys:
            Predicted_Cases = CovidAnalyzer.Function(float_date, *self.fitted_data["TotalCases"])
            print(f"Predicted Cases on {date} : {int(round(Predicted_Cases))}")
        if "TotalDeath" in keys:
            Predicted_Deaths = CovidAnalyzer.Function(float_date, *self.fitted_data["TotalDeath"])
            print(f"Predicted Deaths on {date} : {int(round(Predicted_Deaths))}")
        if "TotalRecovered" in keys:
            Predicted_Recovered = CovidAnalyzer.Function(float_date, *self.fitted_data["TotalRecovered"])
            print(f"Predicted Recovered on {date} : {int(round(Predicted_Recovered))}")
        if "TotalActiveCases" in keys:
            Predicted_ActiveCases = CovidAnalyzer.Function(float_date, *self.fitted_data["TotalActiveCases"])
            print(f"Predicted Active Cases on {date} : {int(round(Predicted_ActiveCases))}")
        print("-------------------------------------")

    def Prediction(self, date):
        rDate = datetime.strptime(date, "%d-%m-%y")
        minD = self.data["Dates"][0]
        float_date = CovidAnalyzer.ConvertDateToTimestamp(minD, rDate)
        self.make_prediction(float_date, date)

    @staticmethod
    def getContinuousDate(Min, Max):
        return [Min + timedelta(seconds=i) for i in range(0, int((Max - Min).total_seconds()) + 1, 10000)]

    @staticmethod
    def ConvertDateToTimestamp(Min, CurrentDate):
        return (datetime.timestamp(CurrentDate) - datetime.timestamp(Min)) / 86400.0

    @staticmethod
    def ConvertTimestampToDate(Min, CurrentTimeStamp):
        return datetime.fromtimestamp(CurrentTimeStamp * 86400.0 + datetime.timestamp(Min))

    @staticmethod
    def FunctionLog(x, a, b, c, u, v, m, n, p, q, a1, b1, c1, u1, v1, m1, n1, p1, q1,
                    a2, b2, c2, u2, v2, m2, n2, p2, q2, w):
        return np.log((a * np.exp(b * x + c)) / (u * np.exp(-m * x + p) + v * np.exp(n * x + q)) +
                      (a1 * np.exp(b1 * x + c1)) / (u1 * np.exp(-m1 * x + p1) + v1 * np.exp(n1 * x + q1)) +
                      (a2 * np.exp(b2 * x + c2)) / (u2 * np.exp(-m2 * x + p2) + v2 * np.exp(n2 * x + q2)) + w)

    @staticmethod
    def Function(x, a, b, c, u, v, m, n, p, q, a1, b1, c1, u1, v1, m1, n1, p1, q1,
                 a2, b2, c2, u2, v2, m2, n2, p2, q2, w):
        return (a * np.exp(b * x + c)) / (u * np.exp(-m * x + p) + v * np.exp(n * x + q)) + \
               (a1 * np.exp(b1 * x + c1)) / (u1 * np.exp(-m1 * x + p1) + v1 * np.exp(n1 * x + q1)) + \
               (a2 * np.exp(b2 * x + c2)) / (u2 * np.exp(-m2 * x + p2) + v2 * np.exp(n2 * x + q2)) + w

    @staticmethod
    def null_inf(x):
        y = np.array([i for i in x])
        y[y < 0] = 0
        return y

    @staticmethod
    def safe_log(x):
        y = x.copy()
        for i in range(len(y)):
            if y[i] == 0:
                y[i] = 1
        return y
