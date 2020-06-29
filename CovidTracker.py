from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


class CovidTracker:
    def __init__(self, country=None, pr=False):
        self.link = 'https://www.worldometers.info/coronavirus/'
        self.data = []
        if pr:
            print("connecting")
        self.req = Request(self.link, headers={'User-Agent': 'Mozilla/5.0'})
        self.mainReq = Request(self.link, headers={'User-Agent': 'Mozilla/5.0'})
        self.mainData: BeautifulSoup = BeautifulSoup(urlopen(self.req).read(), features="html.parser")
        self.country = "world"
        if country:
            self.setTrackerLocation(country, pr=False)
        else:
            self.WebData: BeautifulSoup = BeautifulSoup(urlopen(self.req).read(), features="html.parser")
            self.set_data()
        if self.country.casefold() != "world":
            url = self.link + "country/" + country.casefold().replace(" ", "-")
        else:
            url = self.link
        if self.country == "usa":
            self.country = "us"
        if pr:
            print(f"connected to {url}")

    def setTrackerLocation(self, country, pr=True):
        self.country = country.casefold()
        if self.country == "usa":
            self.country = "us"
        if self.country != "world":
            url = self.link + "country/" + self.country.replace(" ", "-")
        else:
            url = self.link
        if pr:
            print("connecting")
        self.req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        self.WebData = BeautifulSoup(urlopen(self.req).read(), features="html.parser")
        self.set_data()
        if pr:
            print(f"connected to {url}")

    def set_data(self):
        if self.country.casefold() in ["world"]:
            element = CovidTracker.find_in_using_text(self.mainData.find_all('tr',
                                                                             attrs={'class': "total_row_world"}),
                                                      self.country.title())
        elif self.country.casefold() in ["north america", "south america", "asia", "africa", "europe", "oceania"]:
            element = CovidTracker.find_in_using_text(
                self.mainData.find_all('tr',
                                       attrs={'class': "total_row_world row_continent"}),
                self.country.title())
        else:
            if self.country == "us":
                element = CovidTracker.find_in_using_text(self.mainData.find_all('tr', attrs={'style': ""}),
                                                          'USA')
            else:
                element = CovidTracker.find_in_using_text(self.mainData.find_all('tr', attrs={'style': ""}),
                                                          self.country.replace(" ", "-"))
        self.data = [i.text for i in element.find_all('td')]
        self.data = self.data[:len(self.data) - 3]

    def getDates(self):
        data = CovidTracker.find_using_text(self.WebData.find_all('script', attrs={'type': 'text/javascript'}),
                                            'Total Cases')
        elements = None
        if data:
            for line in data:
                if "categories: " in line:
                    elements = line
                    break
            value = [i.replace("\"", "") for i in elements.split("[")[1].split("]")[0].split(",")]
            return value
        else:
            return None

    def getRank(self):
        x = self.data[0].replace(",", "")
        if x == "":
            x = '0'
        elif x == "N/A":
            return None
        return eval(x)

    def getInfectedData(self):
        x = self.data[2].replace(",", "")
        if x == "":
            x = '0'
        elif x == "N/A":
            return None
        return eval(x)

    def getTodayInfectedData(self):
        x = self.data[3].replace(",", "")
        if x == "":
            x = '0'
        elif x == "N/A":
            return None
        return eval(x)

    def getDeathData(self):
        x = self.data[4].replace(",", "")
        if x == "":
            x = '0'
        elif x == "N/A":
            return None
        return eval(x)

    def getTodayDeathData(self):
        x = self.data[5].replace(",", "")
        if x == "":
            x = '0'
        elif x == "N/A":
            return None
        return eval(x)

    def getRecoveredData(self):
        x = self.data[6].replace(",", "")
        if x == "":
            x = '0'
        elif x == "N/A":
            return None
        return eval(x)

    def getActiveCasesData(self):
        x = self.data[8].replace(",", "")
        if x == "":
            x = '0'
        elif x == "N/A":
            return None
        return eval(x)

    def getSeriousCritical(self):
        x = self.data[9].replace(",", "")
        if x == "":
            x = '0'
        elif x == "N/A":
            return None
        return eval(x)

    def getTotalCasesPerM(self):
        x = self.data[10].replace(",", "")
        if x == "":
            x = '0'
        elif x == "N/A":
            return None
        return eval(x)

    def getDeathsPerM(self):
        x = self.data[11].replace(",", "")
        if x == "":
            x = '0'
        elif x == "N/A":
            return None
        return eval(x)

    def getTotalTest(self):
        x = self.data[12].replace(",", "")
        if x == "":
            x = '0'
        elif x == "N/A":
            return None
        return eval(x)

    def getTestPerM(self):
        x = self.data[13].replace(",", "")
        if x == "":
            x = '0'
        elif x == "N/A":
            return None
        return eval(x)

    def getTotalPopulation(self):
        x = self.data[14].replace(",", "")
        if x == "":
            x = '0'
        elif x == "N/A":
            return None
        return eval(x)

    def getContinent(self):
        x = self.data[15].replace(",", "")
        if x == "N/A":
            return None
        return x

    def getInfectedDataTable(self):
        data = CovidTracker.find_using_text(self.WebData.find_all('script', attrs={'type': 'text/javascript'}),
                                            'Total Cases')
        if data:
            elements = None
            for line in data:
                if "data: " in line:
                    elements = line
                    break
            value = [CovidTracker.intN(i) for i in elements.split("[")[1].split("]")[0].split(",")]
            return value
        else:
            return None

    def getDeathDataTable(self):
        data = CovidTracker.find_using_text(self.WebData.find_all('script', attrs={'type': 'text/javascript'}),
                                            'Total Coronavirus Deaths')
        if data:
            elements = None
            for line in data:
                if "data: " in line:
                    elements = line
                    break
            value = [CovidTracker.intN(i) for i in elements.split("[")[1].split("]")[0].split(",")]
            return value
        else:
            return None

    def getActiveDataTable(self):
        data = CovidTracker.find_using_text(self.WebData.find_all('script', attrs={'type': 'text/javascript'}),
                                            'Total Coronavirus Currently Infected')
        if data:
            elements = None
            for line in data:
                if "data: " in line:
                    elements = line
                    break
            value = [CovidTracker.intN(i) for i in elements.split("[")[1].split("]")[0].split(",")]
            return value
        else:
            return None

    def getDeathsPerDayTable(self):
        data = self.getDeathDataTable()
        if data:
            new_data = [data[i + 1] - data[i] for i in range(len(data) - 1)]
            return new_data
        else:
            return None

    def getNewCasesPerDayTable(self):
        data = self.getInfectedDataTable()
        if data:
            new_data = [data[i + 1] - data[i] for i in range(len(data) - 1)]
            return new_data
        else:
            return None

    def getRecoveredDataTable(self):
        data1 = self.getInfectedDataTable()
        data2 = self.getActiveDataTable()
        if data1 and data2:
            new_data = [(i - j) for i, j in zip(data1, data2)]
            return new_data
        else:
            return None

    def getRecoveredPerDayTable(self):
        data = self.getRecoveredDataTable()
        if data:
            new_data = [data[i + 1] - data[i] for i in range(len(data) - 1)]
            return new_data
        else:
            return None

    def getRvsD(self):
        data = CovidTracker.find_using_text(self.WebData.find_all('script', attrs={'type': 'text/javascript'}),
                                            'deaths-cured-outcome-small')
        if data:
            elements = []
            for line in data:
                if "data: " in line:
                    elements.append(line)
            value = []
            for i in elements:
                value.append([CovidTracker.floatN(j) for j in i.split("[")[1].split("]")[0].split(",")])
            return value
        else:
            return [None, None]

    def getCurrentData(self, pr=False, country=None):
        if country:
            self.setTrackerLocation(country)
        country = self.country.upper()
        Rank = self.getRank()
        TotalInfected = self.getInfectedData()
        NewCases = self.getTodayInfectedData()
        TotalDeaths = self.getDeathData()
        NewDeath = self.getTodayDeathData()
        TotalRecovered = self.getRecoveredData()
        TotalActiveCases = self.getActiveCasesData()
        SeriousCondition = self.getSeriousCritical()
        TotalCasesPerM = self.getTotalCasesPerM()
        TotalDeathPerM = self.getDeathsPerM()
        TotalTest = self.getTotalTest()
        TestPerM = self.getTestPerM()
        TotalPop = self.getTotalPopulation()
        Continent = self.getContinent()
        if TotalRecovered:
            Outcome = TotalDeaths + TotalRecovered
            pRecovered = TotalRecovered/Outcome
            pDied = TotalDeaths/Outcome
        else:
            Outcome = None
            pRecovered = None
            pDied = None
        if pr:
            print("")
            print("--------------------------------------------------------")
            if country.casefold() not in ["north america", "south america", "asia",
                                          "africa", "europe", "oceania", "world"]:
                print(f"Rank of {country} in world : {CovidTracker.NoneData(Rank)}")
            print(f"Total Cases in {country} : {CovidTracker.NoneData(TotalInfected)}")
            print(f"New Cases as of right now in {country} : {CovidTracker.NoneData(NewCases)}")
            print(f"Total Deaths in {country} : {CovidTracker.NoneData(TotalDeaths)}")
            print(f"New Death as of right now in {country} : {CovidTracker.NoneData(NewDeath)}")
            print(f"Total Recovered in {country} : {CovidTracker.NoneData(TotalRecovered)}")
            print(f"Total Active Cases in {country} : {CovidTracker.NoneData(TotalActiveCases)}")
            print("--------------------------------------------------------")
            print(f"Serious Cases in {country} : {CovidTracker.NoneData(SeriousCondition)}")
            print(f"Cases Per Million in {country} : {CovidTracker.NoneData(TotalCasesPerM)}")
            print(f"Death Per Million in {country} : {CovidTracker.NoneData(TotalDeathPerM)}")
            print(f"Total Test Done in {country} : {CovidTracker.NoneData(TotalTest)}")
            print(f"Test Done Per Million in {country} : {CovidTracker.NoneData(TestPerM)}")
            print(f"Total Population in {country} : {CovidTracker.NoneData(TotalPop)}")
            if country.casefold() not in ["north america", "south america", "asia",
                                          "africa", "europe", "oceania", "world"]:
                print(f"Continent : {CovidTracker.NoneData(Continent)}")
            print("--------------------------------------------------------")
            if Outcome:
                print(f"Total Cases That had an outcome in {country} : {Outcome}")
                print(f"Percentage Recovered in {country} : {round(pRecovered * 100.0, 2)}%")
                print(f"percentage Died in {country} : {round(pDied * 100.0, 2)}%")
            else:
                print(f"Total Cases That had an outcome in {country} : N/A")
                print(f"Percentage Recovered in {country} : N/A")
                print(f"percentage Died in {country} : N/A")
            print("--------------------------------------------------------")
            print("")
        return country, Rank, TotalInfected, NewCases, TotalDeaths, NewDeath, TotalRecovered, TotalActiveCases, \
            Continent, SeriousCondition, TotalCasesPerM, TotalDeathPerM, TotalTest, TestPerM, TotalPop, Outcome, \
            pRecovered, pDied

    def getDataList(self, country=None):
        if country:
            self.setTrackerLocation(country)
        RvsD = self.getRvsD()
        return {"Dates": self.getDates(),
                "TotalCases": self.getInfectedDataTable(),
                "TotalDeath": self.getDeathDataTable(),
                "TotalActiveCases": self.getActiveDataTable(),
                "TotalRecovered": self.getRecoveredDataTable(),
                "NewCasesPerDay": self.getNewCasesPerDayTable(),
                "DeathPerDay": self.getDeathsPerDayTable(),
                "RecoveredPerDay": self.getRecoveredPerDayTable(),
                "RecoveryPercentage": RvsD[1],
                "DeathPercentage": RvsD[0]}

    def data_from(self):
        return self.link

    @staticmethod
    def find_using_text(data, value):
        for scripts in data:
            scripts = str(scripts).split('\n')
            found = False
            for line in scripts:
                if value in line:
                    found = True
                    break
            if found:
                return scripts
        return None

    @staticmethod
    def find_in_using_text(data, value):
        j = 0
        for script in data:
            scripts = str(script).split('\n')
            found = False
            for line in scripts[1:len(scripts) - 1]:
                if value in line:
                    found = True
                    break
            if found:
                return script
            j += 1
        return None

    @staticmethod
    def NoneData(x):
        if x is None:
            return "N/A"
        else:
            return x

    @staticmethod
    def intN(x):
        if x == "null" or x == '"nan"':
            return None
        else:
            return int(x)

    @staticmethod
    def floatN(x):
        if x == "null" or x == '"nan"':
            return None
        else:
            return float(x)


if __name__ == "__main__":
    Tracker = CovidTracker()
    while True:
        user_input = eval(input("1. Display Data for World/Continent/Country \n2. exit \nChoose Option : "))
        if not user_input - 1:
            Country_name = input("enter Country/Continent name or type World : ")
            Tracker.setTrackerLocation(Country_name)
            Tracker.getCurrentData(pr=True)
        else:
            break
