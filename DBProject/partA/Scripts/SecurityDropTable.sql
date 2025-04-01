-- First, drop linking tables (many-to-many relationships)
DROP TABLE IF EXISTS Incident_Has_SecurityPerson;
DROP TABLE IF EXISTS Assigment;

-- Next, drop dependent entities (tables with foreign keys)
DROP TABLE IF EXISTS flight;
DROP TABLE IF EXISTS SecurityPerson;
DROP TABLE IF EXISTS Incident;
DROP TABLE IF EXISTS Shifts;

-- Finally, drop primary entities (independent tables)
DROP TABLE IF EXISTS Area;