# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import random
from datetime import datetime
securityPerson_file = 'C:/Users/linoy/OneDrive/Desktop/SQLpython/SecurityPerson.csv'
area_file = 'C:/Users/linoy/OneDrive/Desktop/SQLpython/area.csv'
shift_file = 'C:/Users/linoy/OneDrive/Desktop/SQLpython/shifts_data.csv'
flight_file = 'C:/Users/linoy/OneDrive/Desktop/SQLpython/flights.csv'

# Load CSV files
security_persons = pd.read_csv(securityPerson_file)
areas = pd.read_csv(area_file)
shifts = pd.read_csv(shift_file)
flights = pd.read_csv(flight_file)
# Convert dates to datetime format
security_persons["EmploymentDate"] = pd.to_datetime(security_persons["EmploymentDate"])
shifts["ShiftStart"] = pd.to_datetime(shifts["ShiftStart"], format="%d/%m/%Y %H:%M")
shifts["ShiftEnd"] = pd.to_datetime(shifts["ShiftEnd"], format="%d/%m/%Y %H:%M")

flights["departure"] = pd.to_datetime(flights["departure"])
flights["landing"] = pd.to_datetime(flights["landing"])


assignments = []
assignment_id = 1

for _ in range(400):
    # Select a random shift
    shift = shifts.sample(n=1).iloc[0]
    
    # Select a random area
    area = areas.sample(n=1).iloc[0]
    required_security_level = area["SecurityLevelRequired"]
    
    # Filter available security personnel
    eligible_persons = security_persons[
        (security_persons["SecurityLevel"] >= required_security_level) &
        (security_persons["EmploymentDate"] < shift["ShiftStart"])
    ]
    
    # Ensure the selected person is not assigned to a flight at the same time
    available_persons = []
    for _, person in eligible_persons.iterrows():
        overlapping_flights = flights[
            (flights["SecurityPersonID"] == person["SecurityPersonID"]) &
            ((flights["departure"] <= shift["ShiftEnd"]) & (flights["landing"] >= shift["ShiftStart"]))
        ]
        if overlapping_flights.empty:
            available_persons.append(person)
    
    if available_persons:
        chosen_person = random.choice(available_persons)  # Randomly select a valid security person
        assignments.append([assignment_id, chosen_person["SecurityPersonID"], area["AreaID"], shift["ShiftID"]])
        assignment_id += 1

# Convert to DataFrame and save to CSV
assignments_df = pd.DataFrame(assignments, columns=["AssigmentID", "SecurityPersonID", "AreaID", "ShiftID"])
assignments_df.to_csv("assignment.csv", index=False)

print("Assignment file generated successfully!")
