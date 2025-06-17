# DBProject_213204407_326254794


# Security Management Database

## Table of Contents 

- [Phase 1: Design and Build the Database](#phase-1-design-and-build-the-database)  
  - [Introduction](#introduction)  
  - [ERD (Entity-Relationship Diagram)](#erd-entity-relationship-diagram)  
  - [DSD (Data Structure Diagram)](#dsd-data-structure-diagram)  
  - [SQL Scripts](#sql-scripts)  
  - [Data](#data)
    - [First tool: using Mockaroo](#first-tool-using-mockaro-to-create-csv-file) 
    - [Second tool: using Generatedata](#second-tool-using-generatedata-to-create-csv-file)  
    - [Third tool: using Python](#third-tool-using-python-to-create-csv-file) 
  - [Backup_1](#backup_1)  
- [Phase 2: Queries](#phase-2-queries)
   - [Queries](#queries)
  - [Commit and Rollback](#commit-and-rollback)
  - [Checks](#checks)
  - [Backup_2](#backup_2)
- [Phase 3: Integration](#phase-3-integration)
  - [ה-DSD של האגף השני](#ה-DSD-של-האגף-השני)
  - [ה-ERD של האגף השני](#ה-ERD-של-האגף-השני)
  - [ה-ERD המשולב](#ה-ERD-המשולב)
  - [ה-DSD המשולב](#ה-DSD-המשולב)
  - [שינויים בבסיס הנתונים](#שינויים-בבסיס-הנתונים)
  - [מבטים](#מבטים)
  - [גיבוי 3](#גיבוי-3)
- [Phase 4: Programming](#phase-4-programming)
  - [Functions](#functions)
  - [Procedures](#procedures)
  - [Triggers](#triggers)
  - [Main](#main)
  - [Backup_4](#backup_4)

 

- [שלב ה' - יצירת ממשק גרפי לעבודה מול בסיס הנתונים](#שלב-ה---יצירת-ממשק-גרפי-לעבודה-מול-בסיס-הנתונים)
- [הקדמה](#הקדמה)
- [כלים וטכנולוגיות בהם השתמשנו](#כלים-וטכנולוגיות-בהם-השתמשנו)
- [מסכי המערכת](#מסכי-המערכת)
- [פירוט הקבצים במערכת](#פירוט-הקבצים-במערכת)
- [תמונות מסך](#תמונות-מסך)




## Phase 1: Design and Build the Database  
### Introduction
The **Security Management Database** is designed to efficiently manage security personnel, secure areas, shifts, and incident records. This system ensures smooth operations by tracking security assignments, required security levels, and emergency incidents while maintaining a high level of organization and accessibility.

#### **Purpose of the Database**
This database serves as a structured and reliable solution for security organizations to:  
- **Manage security personnel** by tracking their experience, employment details, and security levels.  
- **Monitor secure areas** by maintaining information about locations and the required security levels.  
- **Assign security officers to shifts** based on availability and clearance levels.  
- **Track and record incidents** for reporting and operational improvements.  
- **Ensure compliance** with security regulations and maintain a history of security personnel activities.  

#### **Potential Use Cases**
- **Security Administrators** can use the database to schedule shifts, allocate personnel to secure areas, and track incidents.  
- **Security Personnel** can check their assigned shifts, work locations, and report incidents.  
- **Management & Investigators** can analyze security breaches, review personnel history, and generate reports on security performance.  
- **Emergency Response Teams** can quickly access real-time data to handle security incidents efficiently.  

This structured database helps streamline security operations, improving organization, compliance, and response times.
###  ERD (Entity-Relationship Diagram)    
![ERD Diagram](DBProject/partA/ERDAndDSDFiles/erd.png)  

###  DSD (Data Structure Diagram)   
![DSD Diagram](DBProject/partA/ERDAndDSDFiles/dsd.png)  

###  SQL Scripts  
Provide the following SQL scripts:  
- **Create Tables Script** - The SQL script for creating the database tables is available in the repository:  

     📌 **[View `create_tables.sql`](DBProject/partA/Scripts/SecurityCreateTable.sql)**  

- **Insert Data Script** - The SQL script for insert data to the database tables is available in the repository:  

    📌 **[View `insert_tables.sql`](DBProject/partA/Scripts/SecurityInserts.sql)**  
 
- **Drop Tables Script** - The SQL script for droping all tables is available in the repository:  

    📌 **[View `drop_tables.sql`](DBProject/partA/Scripts/SecurityDropTable.sql)**  

- **Select All Data Script**  - The SQL script for selectAll tables is available in the repository:  

    📌 **[View `selectAll_tables.sql`](DBProject/partA/Scripts/SecuritySelectAll.sql)**  
  
###  Data  
####  First tool: using [mockaro](https://www.mockaroo.com/) to create csv file
#####  Entering a data to securityPerson table
📌[View `securityPerson_data.csv`](DBProject/partA/MockData/SecurityPerson.csv)
- formula of securityPersonID: \d{9}
- formula of ContactInfo : concat("05", random(10000000, 99999999))
![image](DBProject/partA/MockData/mock_1.png)
![image](DBProject/partA/MockData/mock_2.png)
![image](DBProject/partA/MockData/mock_3.png)
results for  the command `SELECT COUNT(*) FROM securityPerson;`:
![image](DBProject/partA/MockData/mock_4.png)

####  Second tool: using [generatedata](https://generatedata.com/generator). to create csv file 
#####  Entering a data to shift table
![image](DBProject/partA/GenerateData/gen_1.png)
![image](DBProject/partA/GenerateData/gen_2.png)
<br><br>


results for  the command `SELECT COUNT(*) FROM shift;`:
<br>
![image](DBProject/partA/GenerateData/gen_3.png)


####  Third tool: using python to create csv file

- Area Data:*
  <br>
   📌 [View `area_data_code`](DBProject/partA/PythonData/area_data_python.py)
  <br>
   📌 [View `area_data.csv`](DBProject/partA/PythonData/area.csv)
- Assigment Data:
  <br>
    📌 [View `assigment_data_code`](DBProject/partA/PythonData/assignmentPython.py)
  <br>
    📌 [View `assigment_data.csv`](DBProject/partA/PythonData/assignment.csv)
- IncidentHasSecurityPerson Data:
    <br>
   📌 [View `incidentHasSecurityPerson_code`](DBProject/partA/PythonData/Incident_Has_SecurityPerson.py)
  <br>
   📌 [View `incidentHasSecurityPerson.csv`](DBProject/partA/PythonData/Incident_Has_SecurityPerson.csv)
 - Flights Data:
    <br>
   📌 [View `flights_code`](DBProject/partA/PythonData/flightPython.py)
   <br>
   📌 [View `flights_data.csv`](DBProject/partA/PythonData/flights.csv)
   
  



### Backup_1
-   backups files are kept with the date and hour of the backup:  

[go to backups](DBProject/partA/Backup)



## Phase 2: Queries 

### [Queries](#queries)
📌[View Queries Code](DBProject/partB/Queries/Queries)

- Query 1: שאילתה למציאת כל המשמרות שבהן עובדים מאבטחים ברמה ביטחונית מסוימת
  
![image](DBProject/partB/Queries/Query_1.png)

- Query 2:  שאילתה למציאת כל הטיסות בהן מאבטחים אחראים על טיסות, ומידע על המאבטח
  
![image](DBProject/partB/Queries/Query_2.png)

- Query 3: השאילתה הזו מחזירה את המידע על מאבטחים שעבדו באזורים עם רמת ביטחון גבוהה 
                                                         כולל שם המאבטח, שם האזור, ומספר האירועים שהמאבטח היה מעורב בהם באותו האזור

![image](DBProject/partB/Queries/Query_3.png)

- Query 4: השאילתה הזו מחפשת את כל המאבטחים שעבדו באזורים שבהם התרחשו יותר מ-3 אירועים,
                                                  סופרת את מספר האירועים לכל מאבטח בכל אזור, ומחזירה את שם המאבטח, שם האזור ומספר האירועים

![image](DBProject/partB/Queries/Query_4.png)

- Query 5: השאילתה סופרת את מספר המשמרות שביצע כל מאבטח בטווח התאריכים ומחזירה את המידע ממוין לפי מספר המשמרות
  
![image](DBProject/partB/Queries/Query_5.png)

- Query 6: השאילתה סופרת את מספר האירועים בכל חודש ושנה
  
![image](DBProject/partB/Queries/Query_6.png)

- Query 7: השאילתה מחזירה את שמות המאבטחים שהיו מעורבים באירועים מסוג מסוים
  
![image](DBProject/partB/Queries/Query_7.png)

- Query 8: השאילתה סופרת את מספר הטיסות שכל איש אבטחה איבטח
  
![image](DBProject/partB/Queries/Query_8.png)

**delete and update queries**

📌[View Delete And Update Queries Code](DBProject/partB/Queries/DeleteAndUpdateQueris)

🔹Delete Queries:
  
  - Query 1: מחיקת אנשי אבטחה שלא שובצו לשום משמרת, לא היו בטיסות, ולא השתתפו באירועים
    
   ![image](DBProject/partB/Queries/delete_1.png)

  - Query 2: מחיקת טיסות שבהן שובץ איש אבטחה עם רמת אבטחה נמוכה מ־2
    
   ![image](DBProject/partB/Queries/delete_2.png)

  - Query 3: מחיקת כל השיבוצים של מאבטחים שהוצבו באותו אזור ביותר ממשמרת אחת
    
    ![image](DBProject/partB/Queries/delete_3.png)

🔹Update Queries:

 - Query 1: העלאת דרגת אבטחה למאבטחים שטיפלו באירועים באזורים ברמת אבטחה גבוהה מ־4 וקטנה מ-5

   ![image](DBProject/partB/Queries/update_1.png)
   
 - Query 2: עדכון אזורים: הוספת "אזור חם" לשם של אזורים שבהם התרחשו יותר מ־3 אירועים

   ![image](DBProject/partB/Queries/update_2.png)

 - Query 3: עדכון אנשי אבטחה: הוספת ותק לשם של מאבטחים שעובדים יותר מ־5 שנים

    ![image](DBProject/partB/Queries/update_3.png)


   


    
   ![image](DBProject/partB/Queries/delete_1.png)

### [Commit and Rollback](#commit-and-rollback)

📌[View Commit and Rollback Code](DBProject/partB/Commit_Rollback/Commit_Rollback)

📌 Commit is a command used to finalize or save all the changes made during a transaction to the database.

- Commit 1: We added a new employee to the Security Person table and it was indeed saved.
![image](DBProject/partB/Commit_Rollback/Commit_1.png)

- Commit 2: We updated the security level of a specific employee in the Security Person table and it was updated.
![image](DBProject/partB/Commit_Rollback/Commit_2.png)

📌 Rollback is a command used to undo or cancel all changes made during a transaction if something goes wrong.

- RallBack 1: We deleted one area from the Area table and then rolled back and it was not deleted.
![image](DBProject/partB/Commit_Rollback/RollBack_1.png)

- RallBack 2: We updated an area name in the Area table and then rolled back and it was not updated.
![image](DBProject/partB/Commit_Rollback/RollBack_2.png)


### [Checks](#checks)

📌 The CHECK command in SQL is used to define constraints on values in a table's columns. It ensures that the data
    entered into the table meets specific conditions or rules.

📌[View Checks Code](DBProject/partB/Checks/Checks)

- Check 1: We checked that the security level in Area table is in the range between 1 and 5.
![image](DBProject/partB/Checks/Checks_1.png)

- Check 2: We checked the validity of the cell phone number in the Security Person table:
   it must start with the digits 05 and must have 10 digits.
![image](DBProject/partB/Checks/Checks_2.png)

- Check 3: We checked that the takeoff time in Flight table is less than the landing time.
![image](DBProject/partB/Checks/Checks_3.png)


### [Backup_2](#backup_2)

-   backups files are kept with the date and hour of the backup:  

[go to backups](DBProject/partB/Backup)

## Phase 3: Integration

### Introduction

בשלב זה ביצענו אינטגרציה בין המערכת שפיתחנו לבין מערכת נוספת של קבוצה אחרת. המטרה הייתה לשלב את בסיסי הנתונים בצורה לוגית ופיזית לכדי בסיס נתונים משותף, תוך כדי שמירה על תקינות הנתונים והקשרים.

### Process Overview

### **ה-DSD של האגף השני**

קיבלנו קובץ גיבוי של בסיס נתונים מקבוצה אחרת ומתוכו הפקנו את תרשים מבנה הנתונים.
   ![image]( DBProject/partC/ERDandDSDfiles/dsdFlight.png)
  

### **ה-ERD של האגף השני**

   מתוך ה-DSD שיחזרנו את תרשים ה-ERD באמצעות הינדוס לאחור.
 ![image]( DBProject/partC/ERDandDSDfiles/erdFlight.png)
### **ה-ERD המשולב**

   עיצבנו תרשים ERD משולב המשלב את שני הארגונים בצורה לוגית, לאחר שקיבלנו החלטות עיצוביות כיצד לבצע את השילוב.
    בין היתר ביצענו את השינויים הבאים:
   - איחדנו שתי טבלאות `Flight` שהופיעו אצל כל קבוצה, תוך שמירה על שדות רלוונטיים מכל אחת וביטול כפילויות.
   - הפכנו את הישות `SecurityPerson` ליורשת של `Person`, על מנת למנוע כפילויות ולנצל את המבנה הכללי של בני אדם במערכת.
   - איחדנו מספר קשרים מסוג רבים־לרבים שהיו מחוברים לישויות השונות היורשות מ־`Person`, כך שייצרו קשר אחד כללי עם `Person`.
   - הוספנו עמודת "תחילת עבודה" (EmploymentDate) בישות `Person` כדי לייצג את תאריך ההתחלה של מאבטחים, והסרנו את אותה עמודה מ־`SecurityPerson`.
   
   את שלבי האיחוד והשינויים נציג בהמשך בפירוט בעת הצגת קובץ `Integrate.sql`.

 ![image]( DBProject/partC/ERDandDSDfiles/combinedErd.png)
### **ה-DSD המשולב** 

   ייצרנו תרשים מבנה נתונים (DSD) מתוך המערכת החדשה לאחר השינויים, הכולל את כל הישויות והקשרים המעודכנים.
    ![image]( DBProject/partC/ERDandDSDfiles/combinedDsd.png)
    בנוסף, יצרנו את ה-ERD המשותף מתוך התוכנה.
      ![image]( DBProject/partC/ERDandDSDfiles/combinedDsdFromPostgres.png)

### **שינויים בבסיס הנתונים**  
   לא יצרנו מחדש את הטבלאות – השתמשנו בטבלאות הקיימות והשתמשנו בפקודות `ALTER TABLE`, `UPDATE`, ו-`DROP COLUMN` כדי להתאים את המבנה ל־ERD החדש.  
   

חילקנו את העבודה לכמה קבצים לפי שלבים ברורים, כאשר השלב הראשון היה להמיר את העמודה `passportNumber` בטבלת Person למפתח הראשי החדש `PersonID` מסוג `SERIAL`.  

הסבר על התהליך של המרת העמודה:
-  הסרנו את כל הקשרים הזרים (foreign keys) שהתבססו על `passportNumber` בטבלאות המקושרות ל- `Person`.
-  הסרנו את המפתח הראשי הישן מטבלת `Person`, ועדכנו את העמודה `Birthday` עם ערכים אקראיים (בהתאם לגיל ריאלי לתחילת עבודה) ושינינו את שמה ל-EmploymentDate. בנוסף, שינינו שמות וגדלים של עמודות בהתאם לעיצוב החדש (`Name_` ל־`FullName`, ו־`Mail` ל־VARCHAR(50)).  
-  הוספנו עמודת `PersonID` מסוג `SERIAL` כ־Primary Key חדש בטבלת `Person`.
-  עדכנו כל אחת מטבלאות הירושה (`Passenger`, `Pilot`, `FlightAttendant`) כך שישתמשו ב־`PersonID` במקום `passportNumber`, כולל הוספת קשרים זרים חדשים והגדרה של `PersonID` כמפתח ראשי.
-  עדכנו את כל הטבלאות המקושרות הנוספות (כמו `Has`, `ServedBy`, `FlownBy`, `Recive`, `Give`, ועוד) כך שישתמשו ב־`PersonID` במקום `passportNumber`, תוך שמירה על תקינות של קשרים זרים.
-  מחקנו את העמודה `passportNumber` מטבלת `Person`, כך שלא תהיה כפילות.
-  קבענו שערך `EmploymentDate` יהיה `NULL` עבור נוסעים (שלא נחשבים עובדים בארגון), ועדכנו אותו בהתאם. בנוסף, הסרנו עמודות מיותרות כמו `numberPhone` מהטבלה `FlightAttendant`.

📌 [View `part1`](DBProject/partC/IntegrateSql/part1_Integrate_from_person.txt)

לאחר שסיימנו להמיר את Person ולהתאים את כל הטבלאות לתמוך ב-PersonID כמפתח הראשי, בשלב הבא התמקדנו בהורשת SecurityPerson מ-Person כדי לאחד את המידע ולשפר את מבנה בסיס הנתונים.

הסבר על התהליך של הורשת SecurityPerson מ-Person:
- מוסיפים לעמודת SecurityPerson את העמודה PersonID כדי לקשר ל-Person.
- מכניסים רשומות חדשות לטבלת Person מהנתונים הקיימים ב-SecurityPerson.
- מעדכנים את העמודה PersonID ב-SecurityPerson לפי ההתאמה בין השמות והאימיילים בטבלת Person.
- מוסיפים עמודת PersonID לטבלאות התלויות (כמו Assigment, flight1 ו-Incident_Has_SecurityPerson) ומעדכנים את הערכים לפי SecurityPerson.
- מסירים את המפתחות הזרים הישנים שמצביעים על SecurityPersonID בטבלאות התלויות.
- מורידים את המפתח הראשי הישן בטבלת SecurityPerson (SecurityPersonID) כדי לאפשר PersonID להיות המפתח הראשי החדש.
- מגדירים את PersonID כמפתח ראשי חדש בטבלת SecurityPerson, ומוסיפים מפתח זר שמפנה לטבלת Person.
- מוסיפים מפתחות זרים חדשים בטבלאות התלויות, שמצביעות על PersonID במקום SecurityPersonID.
- מוחקים את עמודות SecurityPersonID הישנות מטבלאות התלויות.
- מוחקים עמודות מיותרות בטבלת SecurityPerson — כולל FullName, EmploymentDate ו-SecurityPersonID — כי הן כבר בטבלת Person.
 
 📌 [View `part2`](DBProject/partC/IntegrateSql/part2_Implement_inheritance)

חלק מההתאמות למבנה החדש, איחדנו את הטבלאות הרבות המקשרות בין עובדים שונים לטיסה לטבלה בשם PersonInFlight, כדי לנהל בצורה גמישה וברורה יותר את כל התפקידים של אנשים בטיסה.
-מוסיפים לטבלה Has עמודת Role שמייצגת את תפקיד האדם בטיסה, עם ערך ברירת מחדל 'Passenger'.
- משנים את עמודת AirplaneClass בטבלה Has כך שתוכל לקבל ערך NULL, כלומר תהיה אופציונלית.
- מסירים את המפתח הזר הישן שמגביל את PersonID בטבלה Has רק לנוסעים.
- מוסיפים מפתח זר חדש לטבלה Has שמאפשר ל-PersonID להפנות לכל סוג של אדם (נוסע, טייס, דייל וכו') מטבלת Person.
- מעתיקים רשומות של דיילים (FlightAttendants) מטבלת ServedBy לטבלה Has, ומגדירים את התפקיד כ-'FlightAttendant'.
- מעתיקים רשומות של טייסים (Pilots) מטבלת FlownBy לטבלה Has, ומגדירים את התפקיד כ-'Pilot'.
- מוחקים את הטבלאות הישנות ServedBy ו-FlownBy שהפכו מיותרות.
- משנים את שם הטבלה Has ל-PersonInFlight כדי לשפר את הבהירות והקריאות של הטבלה.

 📌 [View `part3`](DBProject/partC/IntegrateSql/part3_MergingThreeConnectors)
 
כעת אנחנו רוצות לאחד את טבלאות flight
- הוספת עמודת FlightId לטבלת OUR_FLIGHT – הוספנו עמודה חדשה שתשמש כמפתח ראשי ייחודי מסוג INTEGER.
- קביעת ערך התחלתי לעמודת FlightId בהתבסס על טבלת Flight1 – מצאנו את המספר הגבוה ביותר של FlightId בטבלה Flight1 כדי לקבוע את הערך הבא שיוקצה.
- יצירת סדרת מספרים (sequence) עבור FlightId – יצרנו סדרה שמתחילה מהמספר שנמצא בשלב הקודם, כדי לייצר ערכי מפתח חדשים.
- עדכון כל הרשומות בטבלת OUR_FLIGHT לקבלת ערך FlightId מתוך הסדרה – מילאנו את הערכים החדשים בעמודה.
- הוספת עמודת FlightID לטבלאות Relationship ו־PersonInFlight – כדי לקשר אותן לטבלת הטיסות החדשה.
- עדכון עמודת FlightID בטבלאות Relationship ו־PersonInFlight לפי טבלת OUR_FLIGHT – העברת הקשר בין טבלאות בהתבסס על הטבלה הראשית.
- מחיקת המפתחות הזרים הישנים שנקשרו לעמודת FlightNumber – כדי לפנות מקום למפתחות החדשים.
- מחיקת עמודת FlightNumber מטבלאות Relationship ו־PersonInFlight – העמודה הישן הוסרה כי היא לא רלוונטית יותר.
- הגדרת FlightId כמפתח הראשי החדש של טבלת OUR_FLIGHT – במקום FlightNumber שהיה קודם.
- הוספת מפתחות זרים חדשים בטבלאות Relationship ו־PersonInFlight שמפנים ל־FlightId בטבלת OUR_FLIGHT – כדי לשמור על תקינות הקשרים.
- הוספת עמודות FlightSource ו־FlightDestination לטבלת OUR_FLIGHT – להרחבת מידע על מקור ויעד הטיסה.
- מחיקת עמודות **מיותרות** מטבלת OUR_FLIGHT – כמו FlightNumber, Origin_DestinationType ו־City.
- עדכון עמודת FlightSource עם ערכים מתוך העמודה country – העברת מידע מהעמודה הישנה לעמודה החדשה.
- מחיקת עמודת country מטבלת OUR_FLIGHT – לאחר העברת הנתונים.
- הוספת עמודת personId לטבלת OUR_FLIGHT לצורך קשר זר – לקשר לטבלת securityPerson.
- הגדרת קשר זר בין personId בטבלת OUR_FLIGHT לטבלת securityPerson – לשמירת קשר תקין בין טבלאות.
- הוספת יעד טיסה אקראי (FlightDestination) מתוך רשימה מוגדרת, כאשר היעד שונה ממקור הטיסה – לצורך השלמת הנתונים.
- אפשרנו שעמודת AirlineID בטבלת OUR_FLIGHT תהיה אופציונלית (NULL) – הסרנו את ההגבלה על ערך חובה.
- הכנסת נתונים מטבלת Flight1 לטבלת OUR_FLIGHT – העתקה של הטיסות הקיימות עם השדות הרלוונטיים.
- עדכון רשומות בטבלת OUR_FLIGHT שבהן AirlineID הוא NULL, עם ערכים אקראיים מטבלת AirLine – למילוי שדות חסרים.
- הכנסת רשומות של אנשים בטיסות (SecurityPerson) לטבלה PersonInFlight עם תפקידים מתאימים – הוספת נתונים על תפקידים שונים בטיסה.
- מחיקת עמודת PersonID מטבלת OUR_FLIGHT – לאחר שהמידע הועבר והקשרים עודכנו.
- מחיקת טבלת Flight1 – טבלה זו הפכה מיותרת לאחר העברת כל הנתונים.
- שינוי שם טבלת OUR_FLIGHT ל־FLIGHT – לשם קצר וברור יותר.

 📌 [View `part4`](DBProject/partC/IntegrateSql/part4_mergingFlightTables)
 
### **מבטים**  
   **מבט 1: IncidentDetails**

   מבט על מסד הנתונים המקורי.

🔹 תיאור המבט:

מבט זה מאגד מידע על תקריות (Incidents), כולל סוג התקרית, תיאורה, תאריך התרחשותה, שם האזור בו קרתה, שם איש האבטחה שהיה נוכח ומשך המעורבות שלו בתקרית.

 ![image](DBProject/partC/Views/Images/view_security.png)
 שאילתות על המבט:

🔸 שאילתה 1: שליפת כל התקריות מסוג Vandalism (ונדליזם).

 ![image](DBProject/partC/Views/Images/query_security_1.png)

 🔸 שאילתה 2: שליפת כל התקריות שהתרחשו לאחר 1 בינואר 2024.

 ![image](DBProject/partC/Views/Images/query_security_2.png)
 **מבט 2: PassengerFlightInfo**

מבט על מסד הנתונים שקיבלנו מזוג אחר בקבוצה

🔹 תיאור המבט:

מבט זה מרכז מידע על נוסעים, כולל שמם המלא, מחלקת הטיסה שלהם, מספר הטיסה, יעד ההמראה והנחיתה, וזמן ההמראה.

 ![image](DBProject/partC/Views/Images/view_flight.png)
 
 🔸 שאילתה 1: שליפת שמות של נוסעים שטסים במחלקה ראשונה.

 ![image](DBProject/partC/Views/Images/query_flight_1.png)
 
 🔸 שאילתה 2: שליפת כל הטיסות שהיעד שלהן הוא תל אביב.

 ![image](DBProject/partC/Views/Images/query_flight_2.png)
 
 📌 [View the views](DBProject/partC/Views/Code/views)

### **גיבוי 3**  
   ייצאנו קובץ גיבוי חדש בשם `backup3` המכיל את בסיס הנתונים לאחר האינטגרציה.

   [go to backup](DBProject/partC/Backup)

## Phase 4: Programming
### [Functions](#functions)
🔸 פונקציה 1: הפונקציה מחשבת את ממוצע שנות הניסיון של הטייסים בחברת תעופה מסוימת ומעדכנת את טבלת השירותים הפעילים עם משוב בהתאם לרמת הניסיון.

🔸 פונקציה 2: הפונקציה מחזירה מצביע לטייסים המשויכים לטיסה מסוימת, כולל פרטים כמו מזהה אדם, שם מלא, שנות ניסיון ומזהה חברת התעופה שלהם.


📌 [View the functions](DBProject/partD/Codes/functions)

### [Procedures](#procedures)

🔸 פרוצדורה 1: הפרוצדורה מוסיפה דייל טיסה חדש עם שפה מדוברת, או אם הדייל כבר קיים – מוסיפה לו שפה חדשה, תוך בדיקות למניעת כפילויות וודא שהאדם קיים בטבלת `person` לפני הוספתו כדייל.


🔸 פרוצדורה 2: הפרוצדורה מוחקת אירוע מסוים יחד עם כל הקצאות האבטחה הקשורות אליו, לאחר בדיקה שהאירוע קיים במערכת.

📌 [View the procedures](DBProject/partD/Codes/procedures)

### [Triggers](#triggers)

🔸 טריגר 1: הטריגר `trg_flightattendant_insert` מופעל לאחר הוספה של שורה חדשה בטבלת `flightattendant`, ורושם את פרטי הדייל שנוסף בטבלת הלוג `flightattendant_insert_log`, תוך הצגת הודעה עם פרטי ההוספה.

כדי לראות את הטבלה שנוצרה רשמנו כך:

![image](DBProject/partD/Images/trigger2_run.png)


🔸 טריגר 2: הטריגר מופעל לאחר שנמחקת רשומה מטבלת incident, ומפעיל את הפונקציה trg_incident_delete_notice, אשר מציגה הודעת NOTICE עם מספר האירוע (incidentid) שנמחק.
את התוצאה ניתן לראות בתמונה של ההרצה של התכנית השנייה שנמצאת בהמשך.

📌 [View the triggers](DBProject/partD/Codes/triggers)

### [Main](#main)

🔸תכנית 1: הפונקציה main_function_1 מבצעת שני שלבים עיקריים:


  - מחשבת את ממוצע שנות הנסיון של טייסים בחברת התעופה ומעדכנת בהתאם את טבלת השירותים, ומחזירה הודעה עם הממוצע.

  - מנסה להוסיף דייל טיסה עם שפה חדשה, ומחזירה הודעה על הצלחה או כישלון בתהליך ההוספה.


    קוד התכנית:

    ![image](DBProject/partD/Images/main1_part1.png)
    ![image](DBProject/partD/Images/main1_part2.png)

    

  כדי להריץ את הפונקציה השתמשנו בקטע הקוד הבא:
  

![image](DBProject/partD/Images/main1_SuccessAdd.png)

כפי שניתן לראות, הדייל נוסף בהצלחה עם השפה החדשה והממוצע חושב בהצלחה.

בהמשך ניסינו להוסיף את אותו הדייל עם אותה השפה שוב, מה שגרם לשגיאה מאחר שזה אינו תקין. התוצאה שהתקבלה מוצגת כאן:


![image](DBProject/partD/Images/main1_failAdd.png)

🔸תכנית 2: הפונקציה main_function_2  מבצעת שני שלבים עיקריים:

  - מוחקת אירוע אבטחה מסוים ואת כל ההקצאות הקשורות אליו באמצעות קריאה לפרוצדורה delete_incident_and_security_assignments.
  
  - מביאה את רשימת הטייסים המשויכים לטיסה מסוימת בעזרת הפונקציה get_pilots_for_flight, ומציגה הודעה עם פרטי כל טייס שנמצא.
 
    קוד התכנית:
![image](DBProject/partD/Images/main2.png)



  כדי להריץ את הפונקציה השתמשנו בקטע הקוד הבא:

      
![image](DBProject/partD/Images/main2_sucessDeleteAndTriger.png)

כפי שניתן לראות, האירוע נמחק בהצלחה ופרטי הטייס הודפסו.

בהמשך ניסינו למחוק אירוע שלא קיים, מה שגרם לשגיאה מאחר שזה אינו תקין. התוצאה שהתקבלה מוצגת כאן:

![image](DBProject/partD/Images/main2_failDelete.png)

📌 [View the main](DBProject/partD/Codes/main)

### Backup_4
[go to backup](DBProject/partD/Backup)
# שלב ה' - יצירת ממשק גרפי לעבודה מול בסיס הנתונים

## הקדמה 
בשלב זה פותח ממשק גרפי (GUI) המאפשר עבודה נוחה מול בסיס הנתונים *FinalIntegrated*.  
הממשק פותח בשפת *Python* תוך שימוש בספריית **tkinter** ליצירת המסכים ובספריית **psycopg2** לצורך התחברות לבסיס הנתונים מסוג *PostgreSQL*.

## כלים וטכנולוגיות בהם השתמשנו
* שפת תכנות: **Python**
* ספריית GUI: **tkinter**
* חיבור לבסיס נתונים: **psycopg2**
* בסיס נתונים: **PostgreSQL**
* ניהול גרסאות: **Git**
  



## מסכי המערכת

* מסך כניסה – ממנו ניתן לגשת לכל שאר המסכים
* מסכי CRUD – הוספה, עדכון, מחיקה ושליפה עבור שלוש טבלאות לפחות (כולל טבלה מקשרת)
* מסך שאילתות ופרוצדורות – מאפשר הרצת 2 שאילתות ו-2 פרוצדורות/פונקציות
* מסך ראשי – ניווט לכל חלקי המערכת
* מסך עזרה/אודות – מידע על האפליקציה

---

## פירוט הקבצים במערכת
<h3 align="right">📄 connectToPostgres</h3>

קובץ זה אחראי על יצירת חיבור למסד הנתונים PostgreSQL של הפרויקט.

**מה עושה הקוד?**  
הקובץ מכיל את הפונקציה `get_connection()` שמבצעת ניסיון התחברות לבסיס הנתונים באמצעות ספריית **psycopg2**.  
הפונקציה מחזירה אובייקט חיבור פעיל אם ההתחברות הצליחה, או None במקרה של שגיאה.


**היכן נמצא הקוד?**  
[לצפייה בקוד המלא לחץ כאן](DBProject/partE/connectToPostgres.py)



<h3 align="right">📄 menu.py</h3>


קובץ זה מהווה את המסך הראשי של המערכת ודרכו מתבצע הניווט לכל חלקי האפליקציה.

**מה עושה הקובץ?**  
הקובץ יוצר חלון ראשי גרפי באמצעות ספריית **customtkinter**, מתחבר למסד הנתונים, ומציג כפתורים לכניסה למסכי הטבלאות (CRUD) ולמסך השאילתות והפרוצדורות.  
המשתמש בוחר לאן לנווט – לכל טבלה או למסך השאילתות – וכל כפתור פותח את המסך המתאים.

**היכן נמצא הקוד?**  
[לצפייה בקוד המלא לחץ כאן](DBProject/partE/menu.py)
<h3 align="right">📄 data.py</h3>

קובץ זה אחראי על הצגת מסך טבלה דינמי עבור כל אחת מהטבלאות במערכת, כולל אפשרויות להוספה, עדכון, מחיקה ושליפה של נתונים (CRUD).

**מה עושה הקובץ?**  
הקובץ יוצר חלון גרפי המציג את תוכן הטבלה שנבחרה מתוך בסיס הנתונים, מאפשר ניווט בין עמודים (Paging), ומציג כפתורי עריכה ומחיקה לכל שורה, וכן כפתור להוספת רשומה חדשה.  
המסך נטען באופן דינמי בהתאם לשם הטבלה וה-Primary Key, ומאפשר שליטה מלאה על הנתונים בטבלה בצורה נוחה וידידותית.

**היכן נמצא הקוד?**  
[לצפייה בקוד המלא לחץ כאן](DBProject/partE/data.py)

<h3 align="right">📄 update_form.py</h3>

קובץ זה אחראי על הצגת טופס עדכון (Update) לרשומה קיימת בטבלה שנבחרה.

**מה עושה הקובץ?**  
הקובץ יוצר חלון גרפי (באמצעות customtkinter) שמציג טופס עם כל שדות הרשומה, מאפשר למשתמש לעדכן ערכים בכל שדה (למעט המפתח הראשי), ומבצע עדכון בפועל במסד הנתונים בלחיצת כפתור.  
הקובץ כולל טיפול בשדות ריקים, הצגת הודעות שגיאה במידת הצורך, ורענון הטבלה לאחר עדכון מוצלח.

**היכן נמצא הקוד?**  
[לצפייה בקוד המלא לחץ כאן](DBProject/partE/update_form.py)

<h3 align="right">📄 delete_record.py</h3>

קובץ זה אחראי על מחיקת רשומה מהטבלה שנבחרה, כולל מחיקה רקורסיבית של כל הרשומות התלויות בה בטבלאות אחרות (באמצעות קשרי foreign key).

**מה עושה הקובץ?**  
הקובץ מזהה את כל הטבלאות והעמודות שמפנות לרשומה הנמחקת (באמצעות foreign key), ומוחק תחילה את כל הרשומות התלויות בהן, ורק לאחר מכן מוחק את הרשומה הראשית.  
המחיקה מתבצעת בצורה בטוחה, כולל טיפול בשגיאות, הצגת סיכום מחיקות למשתמש, וביצוע פעולת commit/rollback בהתאם לצורך.

**היכן נמצא הקוד?**  
[לצפייה בקוד המלא לחץ כאן](DBProject/partE/delete_record.py)
<h3 align="right">📄 insert_form.py</h3>

קובץ זה אחראי על הצגת טופס הוספה דינמי לרשומה חדשה בטבלה שנבחרה.

**מה עושה הקובץ?**  
הקובץ יוצר חלון גרפי (באמצעות customtkinter) שמציג טופס מותאם אישית לכל טבלה, בהתאם למבנה העמודות שלה, כולל טיפול בשדות חובה, סוגי נתונים שונים, ושדות מפתח ראשי (כולל תמיכה ב־auto increment).  
המשתמש מזין ערכים, והקובץ מבצע ולידציה, בונה שאילתת INSERT מתאימה, ומוסיף את הרשומה החדשה למסד הנתונים.  
לאחר ההוספה, הטבלה מתרעננת אוטומטית והמשתמש מקבל הודעת הצלחה או שגיאה בהתאם.

**היכן נמצא הקוד?**  
[לצפייה בקוד המלא לחץ כאן](DBProject/partE/insert_form.py)
<h3 align="right">📄 insert_person_form.py</h3>

קובץ זה אחראי על הצגת טופס הוספה דינמי לרשומה חדשה בטבלת Person, כולל בחירת תפקיד (נוסע, דייל, טייס, איש ביטחון) והוספת הנתונים הרלוונטיים לטבלאות המשנה.

**מה עושה הקובץ?**  
הקובץ יוצר חלון גרפי (באמצעות customtkinter) שמציג טופס מותאם אישית לכל עמודות טבלת Person, כולל שדות חובה, סוגי נתונים שונים, ושדות מפתח ראשי (כולל תמיכה ב־auto increment).  
בנוסף, המשתמש בוחר את תפקיד האדם (role) וממלא שדות נוספים בהתאם לתפקיד שנבחר.  
הקובץ מבצע ולידציה לנתונים, מוסיף את הרשומה לטבלת Person, ולאחר מכן מוסיף את הנתונים לטבלת התפקיד המתאימה (passenger, pilot, flightattendant, securityperson).  
לאחר ההוספה, הטבלה מתרעננת אוטומטית והמשתמש מקבל הודעת הצלחה או שגיאה בהתאם.

**היכן נמצא הקוד?**  
[לצפייה בקוד המלא לחץ כאן](DBProject/partE/insert_person_form.py)


<h3 align="right">📄 open_queries_procedures_screen.py</h3>

קובץ זה אחראי על הצגת מסך ייעודי להרצת שאילתות, פרוצדורות ופונקציות מול מסד הנתונים, והצגת התוצאות בצורה גרפית ונוחה.

**מה עושה הקובץ?**  
הקובץ יוצר חלון גרפי (באמצעות customtkinter) עם כפתורים להרצת שאילתות SQL, פרוצדורות, ופונקציות שנכתבו בשלבים הקודמים של הפרויקט.  
כל כפתור מפעיל פעולה מתאימה:  
- שאילתות מורצות ומוצגות בטבלה דינמית.
- פרוצדורות ופונקציות מבוצעות מול המסד, כולל קבלת קלט מהמשתמש והצגת תוצאות/הודעות הצלחה או שגיאה.
הקובץ כולל גם תיבת תוצאות עם גלילה, הסברים על כל פעולה, וטיפול מלא בשגיאות.

**היכן נמצא הקוד?**  
[לצפייה בקוד המלא לחץ כאן](DBProject/partE/open_queries_procedures_screen.py)

<h3 align="right">📄 entrancePage.py</h3>

קובץ זה מייצג את מסך הכניסה (Login) של המערכת, כחלק מדרישות הפרויקט.

**מה עושה הקובץ?**  
הקובץ יוצר חלון גרפי (באמצעות customtkinter) עם שדות להזנת שם משתמש וסיסמה, וכפתור התחברות.  
בפועל, לא מתבצעת בדיקת הרשאות אמיתית מול מסד הנתונים, אלא בדיקה בסיסית (hardcoded) – שם משתמש וסיסמה ("admin" / "1234").  
בכניסה מוצלחת, המסך הראשי של המערכת נפתח.

**הערה:**  
טכנית, איננו מריצות את הקובץ הזה בפועל, מכיוון שאין צורך אמיתי במסך כניסה במערכת שלנו.  
הוספנו אותו כדי לעמוד בדרישת הפרויקט למסך כניסה בלבד.

**היכן נמצא הקוד?**  
[לצפייה בקוד המלא לחץ כאן](DBProject/partE/entrancePage.py)

---

## תמונות מסך

* תמונות מסך לדוגמה נמצאות בתיקיית images
## תמונות מסך

### מסך עמוד התפריט

<img src="DBProject/partE/Images/menu.png" alt="מסך עמוד התפריט" width="300" />

### מסך טבלת בן אדם (Person)
![מסך טבלת בן אדם](Images/add_person.png)

### מסך הוספת שורה לאדם תוך בחירה בסוג האדם
![מסך הוספת שורה לאדם](Images/add_person_example.png)

### דוגמה להרצה של הוספת אדם (הצלחה)
![דוגמה להוספת אדם - הצלחה](Images/add_person_success.png)

### מסך עריכה של בן אדם
![מסך עריכה של בן אדם](Images/update_person.png)

### דוגמה למסך עריכה (לפני השמירה)
![דוגמה למסך עריכה](Images/update_person_example.png)

### דוגמה למסך מחיקה (מחיקת אדם)
![דוגמה למסך מחיקה](Images/delete_person.png)

### מסך שאילתות, פרוצדורות ופונקציות
![מסך שאילתות, פרוצדורות ופונקציות](Images/queries_procedures.png)

### דוגמה להרצת שאילתה
![דוגמה להרצת שאילתה](Images/query_example.png)

### דוגמה להרצת פרוצדורה
![דוגמה להרצת פרוצדורה](Images/procedure_example.png)

### דוגמה להרצת פונקציה
![דוגמה להרצת פונקציה](Images/function_example.png)

[לצפייה בתקיית התמונות לחץ כאן](DBProject/partE/Images
)

---



