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

1. **DSD של האגף השני**
   קיבלנו קובץ גיבוי של בסיס נתונים מקבוצה אחרת ומתוכו הפקנו את תרשים מבנה הנתונים.
   ![image]( DBProject/partC/ERDandDSDfiles/dsdFlight.png)
  

2. **ERD של האגף השני**  
   מתוך ה-DSD שיחזרנו את תרשים ה-ERD באמצעות הינדוס לאחור.
 ![image]( DBProject/partC/ERDandDSDfiles/erdFlight.png)
4. **ERD משולב**
   עיצבנו תרשים ERD משולב המשלב את שני הארגונים בצורה לוגית, לאחר שקיבלנו החלטות עיצוביות כיצד לבצע את השילוב.
    בין היתר ביצענו את השינויים הבאים:
   - איחדנו שתי טבלאות `Flight` שהופיעו אצל כל קבוצה, תוך שמירה על שדות רלוונטיים מכל אחת וביטול כפילויות.
   - הפכנו את הישות `SecurityPerson` ליורשת של `Person`, על מנת למנוע כפילויות ולנצל את המבנה הכללי של בני אדם במערכת.
   - איחדנו מספר קשרים מסוג רבים־לרבים שהיו מחוברים לישויות השונות היורשות מ־`Person`, כך שייצרו קשר אחד כללי עם `Person`.
   - הוספנו עמודת "תחילת עבודה" (EmploymentDate) בישות `Person` כדי לייצג את תאריך ההתחלה של מאבטחים, והסרנו את אותה עמודה מ־`SecurityPerson`.
   
   את שלבי האיחוד והשינויים נציג בהמשך בפירוט בעת הצגת קובץ `Integrate.sql`.

 ![image]( DBProject/partC/ERDandDSDfiles/combinedErd.png)
5. **DSD משולב**  
   ייצרנו תרשים מבנה נתונים (DSD) מתוך המערכת החדשה לאחר השינויים, הכולל את כל הישויות והקשרים המעודכנים.
    ![image]( DBProject/partC/ERDandDSDfiles/combinedDsd.png)
    בנוסף, יצרנו את ה-ERD המשותף מתוך התוכנה.
      ![image]( DBProject/partC/ERDandDSDfiles/combinedDsdFromPostgres.png)

6. **שינויים בבסיס הנתונים (Integrate.sql)**  
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
 
חלק מההתאמות למבנה החדש, איחדנו את הטבלאות הרבות המקשרות בין עובדים שונים לטיסה לטבלה בשם PersonInFlight, כדי לנהל בצורה גמישה וברורה יותר את כל התפקידים של אנשים בטיסה.
-מוסיפים לטבלה Has עמודת Role שמייצגת את תפקיד האדם בטיסה, עם ערך ברירת מחדל 'Passenger'.
- משנים את עמודת AirplaneClass בטבלה Has כך שתוכל לקבל ערך NULL, כלומר תהיה אופציונלית.
- מסירים את המפתח הזר הישן שמגביל את PersonID בטבלה Has רק לנוסעים.
- מוסיפים מפתח זר חדש לטבלה Has שמאפשר ל-PersonID להפנות לכל סוג של אדם (נוסע, טייס, דייל וכו') מטבלת Person.
- מעתיקים רשומות של דיילים (FlightAttendants) מטבלת ServedBy לטבלה Has, ומגדירים את התפקיד כ-'FlightAttendant'.
- מעתיקים רשומות של טייסים (Pilots) מטבלת FlownBy לטבלה Has, ומגדירים את התפקיד כ-'Pilot'.
- מוחקים את הטבלאות הישנות ServedBy ו-FlownBy שהפכו מיותרות.
- משנים את שם הטבלה Has ל-PersonInFlight כדי לשפר את הבהירות והקריאות של הטבלה.

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

7. **קובץ Views.sql**  
   יצירת מבטים (views) בהתאם לדרישות החדשות ולצרכים של שילוב הנתונים.

8. **קובץ גיבוי מעודכן**  
   ייצאנו קובץ גיבוי חדש בשם `backup3` המכיל את בסיס הנתונים לאחר האינטגרציה.

9. **דוח שלב ג**  
   קובץ דוח עם הסברים, החלטות ותמונות של כל התרשימים.






