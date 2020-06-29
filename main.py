from CovidTracker import CovidTracker
from CovidAnalyzer import CovidAnalyzer

desc1 = """Covid Analyzer:
1. Set tracker location
2. Show Today's Data for Countries, Continents, World
3. Analyze Data for Countries and World
4. Exit
"""
desc2 = """Covid Analyzer:
1. Change tracker location and Analyze
2. Show Graphs
3. Cases Prediction
4. Back
5. Exit
"""
option_enter = "Enter your option : "
Enter_Country = "Enter the Country, Continent name or type World : "
enter_date = "Enter the date(dd-mm-yy) : "
wait_enter = "Press Space then Enter to continue"

Tracker = CovidTracker(pr=True, country="world")
Analyzer = CovidAnalyzer(Tracker)

while True:
    print("--------------------------------------------------------")
    print(desc1)
    option = eval(input(option_enter))
    if option == 1:
        country = input(Enter_Country)
        Analyzer.set_location(country, pr=True)
    elif option == 2:
        Tracker.getCurrentData(pr=True)
        _ = input(wait_enter)
    elif option == 3:
        Analyzer.Analyze_data(pr=True)
        while True:
            print("--------------------------------------------------------")
            print(desc2)
            option = eval(input(option_enter))
            if option == 1:
                country = input(Enter_Country)
                Analyzer.set_location(country)
                Analyzer.Analyze_data(pr=True)
            elif option == 2:
                Analyzer.ShowData()
            if option == 3:
                date = input(enter_date)
                Analyzer.Prediction(date)
                _ = input(wait_enter)
            elif option == 4:
                break
            elif option == 5:
                exit()
            else:
                print("Wrong Option")
    elif option == 4:
        break
    else:
        print("Wrong Option")
