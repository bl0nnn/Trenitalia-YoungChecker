import requests
import json
from datetime import datetime, timedelta
import readline
import calendar

GREEN = "\033[32m"
RED =  "\033[31m"
WHITE = "\033[37m"

def check_young(result):
    solutionInfos = []
    for i in range(len(result['solutions'])):

        if not result['solutions'][i]['grids']:
            continue

        for j in range(len(result['solutions'][i]['grids'][0]["services"][0]['offers'])):

                if result['solutions'][i]['grids'][0]['services'][0]["offers"][j]["offerId"] == 1825 and result['solutions'][i]['grids'][0]['services'][0]["offers"][j]["availableAmount"] > 0:
                    trainInfos = []
                    trainInfos.append(result['solutions'][i]["solution"]["departureTime"])
                    trainInfos.append(result['solutions'][i]['grids'][0]["summaries"][0]["trainInfo"]["description"])
                    trainInfos.append(result['solutions'][i]['grids'][0]["summaries"][0]["description"])
                    trainInfos.append(result['solutions'][i]['grids'][0]['services'][0]["offers"][j]["price"]["amount"])
                    trainInfos.append(result['solutions'][i]['grids'][0]['services'][0]["offers"][j]["availableAmount"])
                    solutionInfos.append(trainInfos)
    return solutionInfos
         

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
    elif response.status_code == 400:
        pass
    else:
        return {"errore": f"codice errore: {response.status_code}"}
    
#tutti i codici stazione sono ricavabili dalle richieste che si effettuano a trenitalia. Non ho trovato una fonte specifica da cui reperirli
stations = {
    "milano": "830001700",
    "firenze": "830006421",
    "bologna": "830005043",
    "reggioe": "830005254",
    "torino": "830000219",
    "napoli": "830009218",
    "roma": "830008409",
    "reggioc": "830011781",
    "salerno": "830009818",
    "venezia": "830002593",
    "potenza": "830011420"
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
days = 0
while True:

    inputD = input("Stazione di partenza (Milano, Firenze, Bologna, ReggioE, Torino, Napoli, Roma, ReggioC, Salerno, Venezia, Potenza): ")
    departure_station = inputD.lower()
    if departure_station not in stations_names:
        print("Stazione non trovata!")
    else:
        departure_id = stations[departure_station]
        while True:
            inputA = input("Stazione di destinazione: ")
            arrival_station = inputA.lower()

            if arrival_station not in stations_names:
                print("Stazione non trovata!")
            else:
                arrival_id = stations[arrival_station]
                while True:
                    daysInput = int(input("Per quanti giorni in avanti vuoi vedere? max 170. (Ricorda che più il numero di giorni è alto e più il tempo di esecuzione aumenterà): "))
                    if daysInput <= 0 or daysInput > 170:
                        print("Inserire un numero di giorni valido!")
                    else: 
                        days = daysInput
                        break
                break
        break
       
print("loading results...")

iso_date = datetime.now().isoformat()
date = datetime.fromisoformat(iso_date)
date = date.replace(minute=0, second=0, microsecond=0)

allSolutions = []

for i in range(days):     #In teoria puoi comprare un biglietto fino a 180 giorni prima e dunque fare un calendario di 180 giorni ma consiglio di lasciare uno scarto di qualche giorno per evitare errori strani lol
    date += timedelta(days=1)
    date = date.replace(hour=5, minute=0, second=0, microsecond=0)
    
    while date.hour <= 23:

        departure_time = str(date.isoformat())
        result = get_train_solutions(departure_id, arrival_id, departure_time)

        if result == None:
            break

        lastdate = result["solutions"][-1]["solution"]["departureTime"]
        lastHour = int(datetime.fromisoformat(lastdate[:19]).hour)  
        lastday = int(datetime.fromisoformat(lastdate[:19]).day)  

        res = check_young(result)
        
        if res != []:
            allSolutions.append(res)
        
        
        if len(result["solutions"]) == 10 and lastday == date.day:
            lastdate = result["solutions"][-1]["solution"]["departureTime"]
            lastHour = int(datetime.fromisoformat(lastdate[:19]).hour)
            shift = lastHour - date.hour
            date += timedelta(hours = shift)
        else:
            break

#fare un check su ora per non eseguire tutte le chiamate e shiftare il delta ore di conseguenza
YoungSolutions = []

for solutions in allSolutions:
    for solution in solutions:
        if solution not in YoungSolutions:
            YoungSolutions.append(solution)

solutions = []
for solution in YoungSolutions:
    departure_date = str(solution[0]).split("T")[0]
    train_number = solution[1]
    dep_dest = solution[2]
    price = solution[3]
    num_avaiable = solution[4]

    solution = {
        "Partenza": departure_date,
        "Numero_treno": train_number,
        "Da-A": dep_dest,
        "Prezzo": price,
        "Biglietti_young_disponibili": num_avaiable 
    }
    
    solutions.append(solution)

temp = {
    "soluzioni": solutions
}

if temp["soluzioni"] == []:
    print("\n")
    print("Nessuna soluzione torvata per nei prossimi " + str(days) + " giorn!")
    print("Prova ad aumentare il numero di giorni di osservazione :). In generale trenitalia concede l'acquisto di biglietti con offerta young se c'è un anticipo nell'acquisto di almeno 10/15 giorni")
    print("\n")
    sys.exit()

solutionsFinal = json.dumps(temp, indent=4)
print(solutionsFinal)


solutionsFinal = json.loads(solutionsFinal)
month_young = int(str(solutionsFinal["soluzioni"][- 1]["Partenza"]).split("-")[1])

date2 = str(datetime.now())
yy = int(date2.split("-")[0])
mm = int(date2.split("-")[1])
dd = dd = int(date2.split("-")[2].split(" ")[0])

until = (month_young - mm) + 1

counterTotal = 0
for i in range(until):
    print("\n")
    print(f"\n                      {calendar.month_name[mm]} {yy}\n")
    print("|  LUN  |  MAR  |  MERC |  GIO  |  VEN  |  SAB  |  DOM  |")
    print("|-------|-------|-------|-------|-------|-------|-------|")

    month_days = calendar.monthcalendar(yy, mm)
    counterMonth = 0
    for week in month_days:
        line_1 = "|"
        line_2 = "|"

        for day in week:
            
            if day == 0:
                line_1 += "       |"
                line_2 += "       |"

            else:
                counterTotal += 1
                counterMonth += 1
                present = False

                for solution in range(len(solutionsFinal["soluzioni"])):
                    day_month_young = str(solutionsFinal["soluzioni"][solution]["Partenza"]).split("-")[-2:]
                    day_month_young_int = []
                    for string in day_month_young:
                        day_month_young_int.append(int(string))

                    if day_month_young_int[0] == mm and day_month_young_int[1] == counterMonth:
                        present = True
                        break

                if present:
                    line_1 += f"  {GREEN}{day:2}{WHITE}   |"
                    
                elif present == False and counterTotal - dd <= days:
                    line_1 += f"  {RED}{day:2}{WHITE}   |"  
                else:
                    line_1 += f"  {WHITE}{day:2}{WHITE}   |"

                line_2 += "       |"
                

        print(line_1)
        print(line_2)
        print("|-------|-------|-------|-------|-------|-------|-------|")

    mm += 1
    if mm > 12: 
        mm = 1
        yy += 1
