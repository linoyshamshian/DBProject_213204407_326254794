# DBProject_213204407_326254794


# Security



## Table of Contents 
**[View `drop_tables.sql`](partA/MOCK_DATA (1).csv)** 
[HHH](#DBProject-partA-MOCK_DATA (1).csv)
DBProject/partA/MOCK_DATA (1).csv
- [Phase 1: Design and Build the Database](#phase-1-design-and-build-the-database)  
  - [Introduction](#introduction)  
  - [ERD (Entity-Relationship Diagram)](#erd-entity-relationship-diagram)  
  - [DSD (Data Structure Diagram)](#dsd-data-structure-diagram)  
  - [SQL Scripts](#sql-scripts)  
  - [Data](#data)
  - [Backup](#backup)  
- [Phase 2: Integration](#phase-2-integration)  

## Phase 1: Design and Build the Database  

### Introduction

The **Nursery School Database** is designed to efficiently manage information related to children, parents, nannies, and nursery groups. This system ensures smooth organization and tracking of essential details such as group assignments, caregiver experience, child-parent relationships, and contact information.

#### Purpose of the Database
This database serves as a structured and reliable solution for nursery schools to:  
- **Organize groups** of children based on age, availability, and special needs.  
- **Manage caregiver assignments** by linking experienced nannies to specific groups.  
- **Maintain parent-child relationships**, ensuring smooth communication and accessibility.  
- **Store contact information**, including addresses, phone numbers, and emails.  
- **Track essential details** such as children's birthdates, allergies, and caregiver experience.  

#### Potential Use Cases
- **Nursery School Administrators** can use this database to efficiently allocate children to groups, assign caregivers, and store emergency contacts.  
- **Parents** can track their child's assigned group, caregiver details, and provide important information about allergies or special needs.  
- **Nannies** can view their assigned groups and the children under their care.  
- **Staff and Management** can use the system for record-keeping, scheduling, and communication.  

This structured database helps streamline nursery school operations, improving organization, safety, and communication among all parties involved.

###  ERD (Entity-Relationship Diagram)    
![ERD Diagram](Phase1/ERDAndDSTFiles/ERD.png)  

###  DSD (Data Structure Diagram)   
![DSD Diagram](Phase1/ERDAndDSTFiles/DSD.png)  

###  SQL Scripts  
Provide the following SQL scripts:  
- **Create Tables Script** - The SQL script for creating the database tables is available in the repository:  

📜 **[View `create_tables.sql`](Phase1/scripts/NurserySchoolCreateTable.sql)**  

- **Insert Data Script** - The SQL script for insert data to the database tables is available in the repository:  

📜 **[View `insert_tables.sql`](Phase1/scripts/NurserySchoolInserts.sql)**  
 
- **Drop Tables Script** - The SQL script for droping all tables is available in the repository:  

📜 **[View `drop_tables.sql`](Phase1/scripts/NurserySchoolDropTable.sql)**  

- **Select All Data Script**  - The SQL script for selectAll tables is available in the repository:  

📜 **[View `selectAll_tables.sql`](Phase1/scripts/NurserySchoolSelectAll.sql)**  
  
###  Data  
####  First tool: using [mockaro](https://www.mockaroo.com/) to create csv file
#####  Entering a data to person table
-  person id scope 1-800
📜[View `personMock_data.csv`](Phase1/mockData/Person_MOCK_DATA.csv)
#####  Entering a data to nanny table
-  person id scope 1-400
📜[View `nannyMock_data.csv`](Phase1/mockData/nannyMOCK_DATA.csv)
#####   Entering a data to apotropus table
-  person id scope 401-800
-  Formula of Person ID: `this + 400`
![image](https://github.com/user-attachments/assets/c6ae9a74-aac6-4195-b010-1ad78690e459)

📜 **[View `apotropusMock_data.csv`](Phase1/mockData/apotropusMOCK_DATA.csv)**
![image](https://github.com/user-attachments/assets/08e3b07b-c3ab-44c6-917b-f904926f6901)
![image](https://github.com/user-attachments/assets/6833ecf1-90e6-454d-8396-9dddf415e323)
results for  the command `SELECT COUNT(*) FROM Apotropus;`:
<br>
![image](https://github.com/user-attachments/assets/eaa16659-2fd8-44c0-81cf-c30f62632258)

####  Second tool: using [generatedata](https://generatedata.com/generator). to create csv file 
#####  Entering a data to babyGroup table
-  Group Number  scope 1-400 
📜[View `babyGroupGenerateDat.csv`](Phase1/generateData/babyGroupGenerateData.csv)

![image](https://github.com/user-attachments/assets/9cf296ca-5ccf-46a2-a484-18bd5a5bef4d)

![image](https://github.com/user-attachments/assets/046ee01c-599b-4858-886f-7c9809c60bfa)

![image](https://github.com/user-attachments/assets/b2045ef2-ca93-4829-af5f-843e792afdfd)

results for  the command `SELECT COUNT(*) FROM BabyGroup;`:
<br>
![image](https://github.com/user-attachments/assets/3572a931-0f33-4e31-aced-371117e109db)

#####  Entering a data to baby table
-  Bayby id scope 801-1200
-  Group Number  range 1-400

📜[View `babyGenerateDat.csv`](Phase1/generateData/babyGenerateData.csv)
![image](https://github.com/user-attachments/assets/f9395c30-c300-4f11-9f22-9397bf6e02bf)

![image](https://github.com/user-attachments/assets/a0073b25-4b9c-43ce-a6c1-e0d961ae70d8)
results for  the command `SELECT COUNT(*) FROM Baby;`:
<br>
![image](https://github.com/user-attachments/assets/3572a931-0f33-4e31-aced-371117e109db)


####  Third tool: using python to create csv file

### Backup 
-   backups files are kept with the date and hour of the backup:  

[עבור לתיקיית הגיבויים](Phase1/Backup)



## Phase 2: Integration 
