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
    
    # Assign a random assignment status (e.g., 0 for inactive, 1 for active)
    assignment_status = random.choice([0, 1])  # For example: 0 = inactive, 1 = active
    
    # Create the assignment
    assignments.append([assignment_status, person["SecurityPersonID"], incident["IncidentID"]])
    assignment_id += 1

# Convert the list of assignments to a DataFrame and save as CSV
assignments_df = pd.DataFrame(assignments, columns=["AssigmentStatus", "SecurityPersonID", "IncidentID"])
assignments_df.to_csv("C:/Users/linoy/OneDrive/Desktop/SQLpython/Incident_Has_SecurityPerson.csv", index=False)

print("Assignment file generated successfully!")
