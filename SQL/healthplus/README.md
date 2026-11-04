# HealthPlus – Healthcare Membership & Clinic Operations Analytics (SQL Project)

## Business Problem

HealthPlus operates a network of healthcare clinics and provides services such as specialist consultations, telemedicine sessions, chronic care programs, health packages, laboratory testing, prescriptions, and corporate memberships.

The database contains information about members, clinics, specialists, consultations, healthcare services, billing, payments, claims, and feedback. However, these records need to be organized and analyzed to understand how effectively the healthcare network manages member activity, clinic operations, service utilization, and revenue collection.

The project uses SQL queries to examine operational and financial information across the HealthPlus database and convert relational data into meaningful business insights.

---

## Business Objective

The objective of this project is to analyze HealthPlus healthcare operations and financial performance using MySQL.

The analysis focuses on:

- Understanding member registration and membership distribution.
- Evaluating clinic and specialist information.
- Analyzing consultation activity, status, and consultation modes.
- Reviewing telemedicine usage and session performance.
- Examining chronic care programs and health package subscriptions.
- Analyzing prescriptions and laboratory testing activity.
- Understanding corporate membership participation.
- Evaluating billing, payment collection, and outstanding collection gaps.
- Reviewing member feedback and consultation ratings.
- Identifying data quality issues and preparing data for analysis.

---

## Business Questions

The project addresses the following business questions:

1. How many members are registered, and how are they distributed by membership type and location?
2. Which clinics and clinic types are represented in the HealthPlus network?
3. How is the specialist workforce distributed across specializations and clinics?
4. What is the consultation activity by date, status, mode, and reason for visit?
5. Which specialists handle the highest consultation workload?
6. How frequently do members use consultation services?
7. How are telemedicine sessions distributed by platform, status, and connection quality?
8. Which health packages are most popular?
9. What is the subscription and expiry pattern of health packages?
10. How are corporate members distributed across companies and industries?
11. Which medicines are prescribed most frequently?
12. Which laboratory tests have the highest costs, and what are their statuses?
13. How much is billed for consultation, laboratory, and medicine services?
14. How much payment has been successfully collected, and what is the collection gap?
15. Which payment modes are used by members?
16. What feedback ratings are received, and how do ratings vary by consultation mode?
17. Which members have no recorded consultations?

---

## Dataset / Source Details

| Item | Description |
|---|---|
| Database Name | HealthPlus |
| Database Platform | MySQL |
| Source File | Healthplus(1).sql |
| Data Type | Relational healthcare and membership data |
| Main Areas | Clinics, members, specialists, consultations, telemedicine, healthcare services, billing, payments, and feedback |
| Tables | 17 |

The SQL source file contains database creation statements, table definitions, data insertion statements, data quality checks, data cleaning operations, and analytical SQL queries.

---

## Dataset Structure

The HealthPlus database contains 17 relational tables.

| Table Name | Description |
|---|---|
| Clinics | Clinic details, clinic type, location, establishment year, and contact information |
| Specialists | Specialist details, specialization, clinic assignment, qualifications, experience, and consultation fee |
| Members | Member demographics, location, membership type, registration date, and contact information |
| Corporates | Corporate company details, industry, location, contract dates, and employee count |
| Corporate_Members | Mapping between corporate organizations and enrolled members |
| Consultation | Member consultations, assigned specialists, clinics, dates, modes, statuses, and reasons for visits |
| Telemedicine_Sessions | Telemedicine session timing, platform, connection quality, and session status |
| Chronic_Care_Programs | Member enrollment in chronic care programs, assigned specialists, conditions, and review dates |
| Health_Packages | Health package names, types, prices, validity, and included tests |
| Package_Subscriptions | Member package subscriptions, subscription dates, expiry dates, and payment status |
| Prescriptions | Medicines prescribed during consultations, dosage, duration, and prescription dates |
| Lab_Tests | Laboratory test details, test dates, results, costs, and statuses |
| Claims | Member claims, claim amounts, dates, statuses, and insurance provider details |
| Staff | Clinic staff details, designations, employment types, salaries, and joining dates |
| Billing | Member bills, service-wise charges, total amount, and bill status |
| Payments | Payment dates, amounts, modes, and payment statuses |
| Feedback | Member ratings, feedback comments, and feedback dates linked to consultations |

---

## SQL Project / Analysis Overview

The project is organized around the following business areas:

### 1. Member & Membership Analysis
- Member registration and demographic information.
- Membership type distribution.
- Member location analysis.
- Corporate membership and enrollment analysis.
- Members with no recorded consultations.

### 2. Clinic & Specialist Analysis
- Clinic details and clinic type distribution.
- Specialist specialization and experience.
- Consultation fees.
- Specialist consultation workload and ranking.

### 3. Consultation Analysis
- Consultation status and consultation mode.
- Consultation activity by specialization.
- Most frequent reasons for visits.
- Member consultation frequency.
- Previous and next consultation dates using window functions.

### 4. Telemedicine Analysis
- Telemedicine session status.
- Platform usage.
- Connection quality.
- Average telemedicine session duration.

### 5. Healthcare Service Analysis
- Chronic care program information and status.
- Health package popularity.
- Package subscription payment status and expiry patterns.
- Most prescribed medicines.
- Specialist prescription workload.
- Laboratory test costs and statuses.

### 6. Financial Analysis
- Total billed amount by service.
- Billing status analysis.
- Payment status and collection.
- Payment mode analysis.
- Successful payment totals.
- Billing and payment collection gap.

### 7. Member Feedback Analysis
- Feedback rating distribution.
- Average feedback rating by consultation mode.
- Member feedback records linked to consultations.

---

## Tools / SQL Techniques Used

| Tool / Concept | Application |
|---|---|
| MySQL | Relational database creation and analysis |
| SQL DDL | Creating the database and tables |
| Primary Keys | Uniquely identifying records |
| Foreign Keys | Establishing relationships between tables |
| INSERT | Loading records into database tables |
| SELECT | Retrieving data for analysis |
| WHERE | Filtering records based on conditions |
| ORDER BY | Sorting query results |
| GROUP BY | Grouping records for analysis |
| HAVING | Filtering grouped results |
| Aggregate Functions | COUNT, SUM, AVG, MIN, and MAX |
| Joins | Combining related records across tables |
| Subqueries | Performing nested data analysis |
| Common Table Expressions (CTEs) | Structuring multi-step analytical queries |
| CASE | Categorizing records based on conditions |
| Date Functions | Analyzing dates and calculating durations |
| Window Functions | ROW_NUMBER, RANK, LAG, and LEAD |
| Data Cleaning | Standardizing values and handling missing information |

---

## Data Cleaning / Preparation

Data quality checks and preparation steps are included in the SQL script before the analytical queries.

The preparation process covers:

- Checking primary key uniqueness in important tables.
- Profiling missing values in Consultation, Members, Payments, and Claims.
- Reviewing inconsistent casing in consultation statuses.
- Checking consultation modes, payment modes, and membership types.
- Reviewing specialist consultation fees and experience values.
- Checking financial totals in Billing.
- Validating feedback rating ranges.
- Standardizing casing and whitespace in consultation data.
- Handling missing values in Payments and Claims.
- Cleaning member contact information and demographic fields.
- Standardizing diagnostic and chronic care program statuses.

### Data Quality Observations

The SQL script includes profiling comments that identify the following issues before or during preparation:

- 75 missing email values in Members.
- 283 missing payment mode values in Payments.
- 330 missing consultation ID values in Claims.
- 72 missing insurance provider values in Claims.
- Mixed casing in Consultation status values, including `Completed`, `completed`, and `COMPLETED`.

These are source-script profiling observations. The final impact of cleaning should be confirmed by running the validation queries after the preparation steps.

---

## KPIs / Features Explained

| KPI / Feature | Description |
|---|---|
| Total Members | Number of registered members |
| Membership Distribution | Members grouped by membership type |
| Clinic Distribution | Clinic count and distribution by clinic type or location |
| Specialist Count | Number of specialists and their specialization distribution |
| Total Consultations | Number of recorded consultations |
| Consultation Status | Distribution of consultation statuses |
| Consultation Mode | Distribution of consultation modes |
| Specialist Workload | Consultation count handled by each specialist |
| Telemedicine Sessions | Number and status of telemedicine sessions |
| Average Session Duration | Average duration of telemedicine sessions |
| Package Subscriptions | Number of subscriptions by health package |
| Subscription Payment Status | Payment status of package subscriptions |
| Corporate Enrollment | Member participation by corporate organization and industry |
| Prescription Activity | Prescriptions grouped by medicine or specialist |
| Laboratory Test Activity | Number and status of laboratory tests |
| Laboratory Test Cost | Cost analysis of laboratory tests |
| Total Billed Amount | Total amount recorded in Billing |
| Payment Collection | Successful payment amount recorded in Payments |
| Collection Gap | Difference between billed amount and successful payments |
| Feedback Rating | Distribution and average of member ratings |
| Consultation Frequency | Consultation activity by member |

---

## Dashboard / Reporting Features

The provided SQL file contains SQL-based analysis queries rather than a dashboard file.

The query outputs can be used to prepare reports or visualizations covering:

- Member and membership analysis.
- Clinic and specialist performance.
- Consultation and telemedicine activity.
- Health package and corporate enrollment.
- Prescription and laboratory service utilization.
- Billing and payment collection.
- Member feedback and ratings.

---

## Key Insights / Business Interpretation

The SQL analysis is designed to help interpret:

- How members use consultation and other healthcare services.
- Which specializations and specialists have higher consultation activity.
- How telemedicine services are being used.
- Which health packages attract more subscriptions.
- How corporate membership contributes to member enrollment.
- Which medicines and laboratory services are frequently used.
- How billed amounts compare with successfully collected payments.
- Whether feedback ratings differ across consultation modes.
- Which members have no recorded consultation activity.

Actual numerical findings and rankings should be added only after executing the queries against the database and validating their outputs. The SQL source file alone does not establish the final results of every analysis.

---

## Recommendations / Conclusion

Based on the outputs produced by the SQL analysis, HealthPlus management can use the findings to:

- Review member engagement and membership distribution.
- Monitor clinic and specialist consultation workloads.
- Evaluate telemedicine usage and session quality.
- Track health package subscriptions and expiry patterns.
- Review corporate enrollment and participation.
- Monitor laboratory and prescription service activity.
- Compare billed amounts with successful payment collections.
- Investigate outstanding collection gaps.
- Review member feedback to understand service experience.
- Improve data quality through regular validation and standardization.

The project demonstrates how MySQL can be used to organize and analyze connected healthcare and membership data. It applies relational database concepts, data preparation techniques, joins, aggregations, CTEs, and window functions to support operational and financial analysis.
