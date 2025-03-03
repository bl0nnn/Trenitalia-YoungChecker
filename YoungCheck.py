import requests
import json
from datetime import datetime, timedelta
import readline
import calendar

GREEN = "\033[32m"
RED =  "\033[31m"
NO_COLOR = "\033[0m"


def check_young(result):
    trainInfos = []
    for i in range(len(result['solutions'])):

        if not result['solutions'][i]['grids']:
            continue

        for j in range(len(result['solutions'][i]['grids'][0]["services"][0]['offers'])):
            
                if result['solutions'][i]['grids'][0]['services'][0]["offers"][j]["offerId"] == 1825 and result['solutions'][i]['grids'][0]['services'][0]["offers"][j]["availableAmount"] > 0:

                    trainInfos.append(result['solutions'][i]["solution"]["departureTime"])
                    trainInfos.append(result['solutions'][i]['grids'][0]["summaries"][0]["trainInfo"]["description"])
                    trainInfos.append(result['solutions'][i]['grids'][0]["summaries"][0]["description"])
                    trainInfos.append(result['solutions'][i]['grids'][0]['services'][0]["offers"][j]["price"]["amount"])
                    return trainInfos
                     
    return False
         

def get_train_solutions(departure_id, arrival_id, departure_time, adults=1, children=0, 
                         frecce_only=True, regional_only=False, no_changes=True, 
                         order="DEPARTURE_DATE", limit=10, offset=0, best_fare=False):
    
    
    url = "https://www.lefrecce.it/Channels.Website.BFF.WEB/website/ticket/solutions"

#per eventuali chiarimenti sui parametri del payload consultare la documentazioni API trenitalia di SimoDax  
    payload = {
        "departureLocationId": departure_id,
        "arrivalLocationId": arrival_id,
        "departureTime": departure_time,
        "adults": adults,
        "children": children,
        "criteria": {
            "frecceOnly": frecce_only,
            "regionalOnly": regional_only,
            "noChanges": no_changes,
            "order": order,
            "limit": limit,
            "offset": offset
        },
        "advancedSearchRequest": {
            "bestFare": best_fare,
        }
    }
    
    headers = {
        "Content-Type": "application/json",
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"error code: {response.status_code}"}
    
#tutti i codici stazione sono ricavabili dalle richieste che si effettuano a trenitalia. Non ho trovato una fonte specifica da cui reperirli
stations = {
    "Milano": "830001700",
    "Firenze": "830006421",
    "Bologna": "830005043",
    "ReggioE": "830005254",
    "Torino": "830000219",
    "Napoli": "830009218",
    "Roma": "830008409",
    "ReggioC": "830011781",
    "Salerno": "830009818",
    "Venezia": "830002593",
    "Potenza": "830011420"
}

stations_names = list(stations.keys())

ascii_art = """
@@@ @@@   @@@@@@   @@@  @@@  @@@  @@@   @@@@@@@@      @@@@@@@  @@@  @@@  @@@@@@@@   @@@@@@@  @@@  @@@  @@@@@@@@  @@@@@@@   
@@@ @@@  @@@@@@@@  @@@  @@@  @@@@ @@@  @@@@@@@@@     @@@@@@@@  @@@  @@@  @@@@@@@@  @@@@@@@@  @@@  @@@  @@@@@@@@  @@@@@@@@  
@@! !@@  @@!  @@@  @@!  @@@  @@!@!@@@  !@@           !@@       @@!  @@@  @@!       !@@       @@!  !@@  @@!       @@!  @@@  
!@! @!!  !@!  @!@  !@!  @!@  !@!!@!@!  !@!           !@!       !@!  @!@  !@!       !@!       !@!  @!!  !@!       !@!  @!@  
 !@!@!   @!@  !@!  @!@  !@!  @!@ !!@!  !@! @!@!@     !@!       @!@!@!@!  @!!!:!    !@!       @!@@!@!   @!!!:!    @!@!!@!   
  @!!!   !@!  !!!  !@!  !!!  !@!  !!!  !!! !!@!!     !!!       !!!@!!!!  !!!!!:    !!!       !!@!!!    !!!!!:    !!@!@!    
  !!:    !!:  !!!  !!:  !!!  !!:  !!!  :!!   !!:     :!!       !!:  !!!  !!:       :!!       !!: :!!   !!:       !!: :!!   
  :!:    :!:  !:!  :!:  !:!  :!:  !:!  :!:   !::     :!:       :!:  !:!  :!:       :!:       :!:  !:!  :!:       :!:  !:!  
   ::    ::::: ::  ::::: ::   ::   ::   ::: ::::      ::: :::  ::   :::   :: ::::   ::: :::   ::  :::   :: ::::  ::   :::  
   :      : :  :    : :  :   ::    :    :: :: :       :: :: :   :   : :  : :: ::    :: :: :   :   :::  : :: ::    :   : :   
"""

print(ascii_art)

while True:

    departure_station = input("Stazione di partenza (Milano, Firenze, Bologna, ReggioE, Torino, Napoli, Roma, ReggioC, Salerno, Venezia, Potenza): ")

    if departure_station not in stations_names:
        print("Stazione non trovata!")
    else:
        departure_id = stations[departure_station]
        while True:
            arrival_station = input("Stazione di destinazione: ")

            if arrival_station not in stations_names:
                print("Stazione non trovata!")
            else:
                arrival_id = stations[arrival_station]
                break
        break   
print("loading results...")

iso_date = datetime.now().isoformat()
date = datetime.fromisoformat(iso_date)
date = date.replace(minute=0, second=0, microsecond=0)

allSolutions = []
days = 170

for i in range(days):     #In teoria puoi comprare un biglietto fino a 180 giorni prima e dunque fare un calendario di 180 giorni ma consiglio di lasciare uno scarto di qualche giorno per evitare errori strani lol
    while date.hour <= 20:
        departure_time = str(date.isoformat())
        result = get_train_solutions(departure_id, arrival_id, departure_time)
        if check_young(result) != False:
            allSolutions.append(check_young(result))
        date += timedelta(hours=3)

    date = date.replace(hour=5, minute=0, second=0, microsecond=0)
    date += timedelta(days=1)

YoungSolutions = []

for list in allSolutions:
    if list not in YoungSolutions:
        YoungSolutions.append(list)

solutions = []
for solution in YoungSolutions:
    departure_date = str(solution[0]).split("T")[0]
    train_number = solution[1]
    dep_dest = solution[2]
    price = solution[3]

    solution = {
        "Partenza": departure_date,
        "Numero_treno": train_number,
        "Da-A": dep_dest,
        "Prezzo": price
    }
    
    solutions.append(solution)

temp = {
    "soluzioni": solutions
}

solutionsFinal = json.dumps(temp, indent=4)
print(solutionsFinal)
solutionsFinal = json.loads(solutionsFinal)


month_young = int(str(solutionsFinal["soluzioni"][- 1]["Partenza"]).split("-")[1])
date2 = str(datetime.now())
yy = int(date2.split("-")[0])
mm = int(date2.split("-")[1])
until = (month_young - mm) + 1


for i in range(until):
    print(f"\n{calendar.month_name[mm]} {yy}\n")
    print("|  LUN  |  MAR  |  MERC |  GIO  |  VEN  |  SAB  |  DOM  |")
    print("|-------|-------|-------|-------|-------|-------|-------|")

    month_days = calendar.monthcalendar(yy, mm)
    counter = 0
    for week in month_days:
        line_1 = "|"
        line_2 = "|"

        for day in week:
            
            if day == 0:
                line_1 += "       |"
                line_2 += "       |"

            else:
                counter += 1
                present = False

                for solution in range(len(solutionsFinal["soluzioni"])):
                    day_month_young = str(solutionsFinal["soluzioni"][solution]["Partenza"]).split("-")[-2:]
                
                    day_month_young_int = []
                    for string in day_month_young:
                        day_month_young_int.append(int(string))

                    if day_month_young_int[0] == mm and day_month_young_int[1] == counter:
                        present = True
                        break

                if present:
                    line_1 += f"  {GREEN}{day:2}{NO_COLOR}   |"
                else:
                    line_1 += f"  {RED}{day:2}{NO_COLOR}   |"

                line_2 += "       |"

        print(line_1)
        print(line_2)
        print("|-------|-------|-------|-------|-------|-------|-------|")

    mm += 1
    if mm > 12: 
        mm = 1
        yy += 1