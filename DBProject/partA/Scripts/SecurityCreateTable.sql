CREATE TABLE if not exists Area
(
  AreaID INT NOT NULL,
  AreaName VARCHAR(35) NOT NULL,
  Description VARCHAR NOT NULL,
  SecurityLevelRequired INT NOT NULL,
  PRIMARY KEY (AreaID)
);

CREATE TYPE shift_type_enum AS ENUM ('Morning', 'Evening', 'Night');

CREATE TABLE IF NOT EXISTS Shifts (
  ShiftID SERIAL PRIMARY KEY,
  ShiftType shift_type_enum NOT NULL,
  ShiftStart TIMESTAMP NOT NULL,
  ShiftEnd TIMESTAMP NOT NULL
);

CREATE TABLE if not exists Incident
(
  IncidentID INT NOT NULL,
  IncidentType VARCHAR NOT NULL,
  IncidentDate DATE NOT NULL,
  IncidentDescription VARCHAR NOT NULL,
  AreaID INT NOT NULL,
  PRIMARY KEY (IncidentID),
  FOREIGN KEY (AreaID) REFERENCES Area(AreaID)
);

CREATE TABLE if not exists SecurityPerson
(
  ContactInfo VARCHAR NOT NULL,
  SecurityLevel INT NOT NULL,
  EmploymentDate DATE NOT NULL,
  FullName VARCHAR(40) NOT NULL,
  SecurityPersonID VARCHAR(9) NOT NULL,
  PRIMARY KEY (SecurityPersonID)
);


CREATE TABLE if not exists Flight
(
  FlightId INT NOT NULL,
  FlightDestination VARCHAR(20) NOT NULL,
  FlightSource VARCHAR(20) NOT NULL,
  Departure DATE NOT NULL,
  Landing DATE NOT NULL,
  SecurityPersonID VARCHAR(9) NOT NULL,
  PRIMARY KEY (flightId),
  FOREIGN KEY (SecurityPersonID) REFERENCES SecurityPerson(SecurityPersonID)
);


CREATE TABLE if not exists Assigment
(
  AssigmentID NUMERIC NOT NULL,
  AssignmentDate DATE NOT NULL,
  SecurityPersonID VARCHAR(9) NOT NULL,
  AreaID INT NOT NULL,
  ShiftID INT NOT NULL,
  PRIMARY KEY (AssigmentID),
  FOREIGN KEY (SecurityPersonID) REFERENCES SecurityPerson(SecurityPersonID),
  FOREIGN KEY (AreaID) REFERENCES Area(AreaID),
  FOREIGN KEY (ShiftID) REFERENCES Shifts(ShiftID)
);

CREATE TABLE if not exists Incident_Has_SecurityPerson
(
  AsiigmentStatus INT NOT NULL,
  SecurityPersonID VARCHAR(9) NOT NULL,
  IncidentID INT NOT NULL,
  PRIMARY KEY (SecurityPersonID, IncidentID),
  FOREIGN KEY (SecurityPersonID) REFERENCES SecurityPerson(SecurityPersonID),
  FOREIGN KEY (IncidentID) REFERENCES Incident(IncidentID)
);


 
