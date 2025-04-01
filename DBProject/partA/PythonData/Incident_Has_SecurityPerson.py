# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 17:07:51 2025

@author: linoy
"""

import pandas as pd
import random

from datetime import datetime, timedelta

# Input file paths
securityPerson_file = 'C:/Users/linoy/OneDrive/Desktop/SQLpython/SecurityPerson.csv'
incident_file = 'C:/Users/linoy/OneDrive/Desktop/SQLpython/incident.csv'
flight_file = 'C:/Users/linoy/OneDrive/Desktop/SQLpython/flights.csv'

# Load CSV files
security_persons = pd.read_csv(securityPerson_file)
incidents = pd.read_csv(incident_file)
flights = pd.read_csv(flight_file)

# Convert date columns to datetime format
security_persons["EmploymentDate"] = pd.to_datetime(security_persons["EmploymentDate"])
incidents["IncidentDate"] = pd.to_datetime(incidents["IncidentDate"])
flights["Departure"] = pd.to_datetime(flights["Departure"])
flights["Landing"] = pd.to_datetime(flights["Landing"])

# List to hold the assignments
assignments = []
assignment_id = 1

for _ in range(400):
    # Select a random incident
    incident = incidents.sample(n=1).iloc[0]
    
    # Select a random security person
    person = security_persons.sample(n=1).iloc[0]
    
    # Ensure the incident date is after the security person's employment date
    while incident["IncidentDate"] < person["EmploymentDate"]:
        incident = incidents.sample(n=1).iloc[0]
    
    # Check if the security person is assigned to a flight during the incident
    overlapping_flights = flights[
        (flights["SecurityPersonID"] == person["SecurityPersonID"]) & 
        ((flights["Departure"] <= incident["IncidentDate"]) & (flights["Landing"] >= incident["IncidentDate"]))
    ]
    
    # If the person is assigned to a flight at the time of the incident, skip this person
    if not overlapping_flights.empty:
        continue  # Skip to the next iteration if the person is unavailable
    
    # Create a random duration for handling the incident (between 1 and 12 hours)
    duration = timedelta(hours=random.randint(1, 12))
    
    # Create the assignment with the duration of the incident handling time
    assignments.append([person["SecurityPersonID"], incident["IncidentID"], duration])
    assignment_id += 1

# Convert the list of assignments to a DataFrame and save as CSV
assignments_df = pd.DataFrame(assignments, columns=["SecurityPersonID", "IncidentID", "Duration"])
assignments_df.to_csv("C:/Users/linoy/OneDrive/Desktop/SQLpython/Incident_Has_SecurityPerson.csv", index=False)

print("Assignment file generated successfully!")
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 17:07:51 2025

@author: linoy
"""

import pandas as pd
import random
from datetime import timedelta

# Input file paths
securityPerson_file = 'C:/Users/linoy/OneDrive/Desktop/SQLpython/SecurityPerson.csv'
incident_file = 'C:/Users/linoy/OneDrive/Desktop/SQLpython/incident.csv'
flight_file = 'C:/Users/linoy/OneDrive/Desktop/SQLpython/flights.csv'

# Load CSV files
security_persons = pd.read_csv(securityPerson_file)
incidents = pd.read_csv(incident_file)
flights = pd.read_csv(flight_file)

# Convert date columns to datetime format
security_persons["EmploymentDate"] = pd.to_datetime(security_persons["EmploymentDate"])
incidents["IncidentDate"] = pd.to_datetime(incidents["IncidentDate"])
flights["Departure"] = pd.to_datetime(flights["Departure"])
flights["Landing"] = pd.to_datetime(flights["Landing"])

# List to hold the assignments
assignments = []
assignment_id = 1

for _ in range(400):
    print(_)
    # Select a random incident
    incident = incidents.sample(n=1).iloc[0]
    
    # Select a random security person
    person = security_persons.sample(n=1).iloc[0]
    
    # Ensure the incident date is after the security person's employment date
    while incident["IncidentDate"] < person["EmploymentDate"]:
        incident = incidents.sample(n=1).iloc[0]
    
    # Check if the security person is assigned to a flight during the incident
    overlapping_flights = flights[
        (flights["SecurityPersonID"] == person["SecurityPersonID"]) & 
        ((flights["Departure"] <= incident["IncidentDate"]) & (flights["Landing"] >= incident["IncidentDate"]))
    ]
    
    # If the person is assigned to a flight at the time of the incident, skip this person
    if not overlapping_flights.empty:
        continue  # Skip to the next iteration if the person is unavailable
    
    # Create a random duration for handling the incident (between 1 and 12 hours)
    duration = timedelta(hours=random.randint(1, 12), minutes=random.choice([0, 15, 30, 45]))  # Ensure rounded minutes
    
    # Convert duration to a time object (hours:minutes:seconds format)
    duration_time = (datetime.min + duration).time()

    # Create the assignment with the duration of the incident handling time
    assignments.append([person["SecurityPersonID"], incident["IncidentID"], duration_time])
    assignment_id += 1

# Convert the list of assignments to a DataFrame and save as CSV
assignments_df = pd.DataFrame(assignments, columns=["SecurityPersonID", "IncidentID", "Duration"])
assignments_df.to_csv("C:/Users/linoy/OneDrive/Desktop/SQLpython/Incident_Has_SecurityPerson.csv", index=False)

print("Assignment file generated successfully!")
