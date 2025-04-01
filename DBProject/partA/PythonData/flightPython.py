import pandas as pd
import random
from datetime import datetime, timedelta

# Load data files
securityPerson_file = 'C:/Users/linoy/OneDrive/Desktop/SQLpython/SecurityPerson.csv'
flight_file = 'C:/Users/linoy/OneDrive/Desktop/SQLpython/flights.csv'

security_persons = pd.read_csv(securityPerson_file)

# Convert dates to datetime format
security_persons["EmploymentDate"] = pd.to_datetime(security_persons["EmploymentDate"])

def random_date(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    random_days = random.randint(0, (end - start).days)
    random_hours = random.randint(0, 23)
    random_minutes = random.choice([0, 15, 30, 45])  # Ensuring rounded minutes
    return start + timedelta(days=random_days, hours=random_hours, minutes=random_minutes)

flights = []
flight_id = 1

destinations = ["New York", "Paris", "London", "Berlin", "Tokyo"]
sources = ["Tel Aviv", "Madrid", "Rome", "Dubai", "Athens"]

for _ in range(401):
    departure_date = random_date("2020-01-01", "2024-12-31")
    landing_date = departure_date + timedelta(hours=random.randint(2, 12))
    
    valid_persons = security_persons[security_persons["EmploymentDate"] < departure_date]
    
    if not valid_persons.empty:
        chosen_person = valid_persons.sample(n=1).iloc[0]
        flights.append([flight_id, random.choice(destinations), random.choice(sources), 
                        departure_date, landing_date, chosen_person["SecurityPersonID"]])
        flight_id += 1

flights_df = pd.DataFrame(flights, columns=["FlightId", "FlightDestination", "FlightSource", "Departure", "Landing", "SecurityPersonID"])
flights_df.to_csv("flights.csv", index=False)

print("Flight schedule generated successfully!")
