# MediCare -- Healthcare Operations & Revenue Analytics

## Business Problem

MediCare operates across a hospital network and generates activity
through patient appointments, admissions, treatments, laboratory
services, pharmacy transactions, billing and payments. However,
management needs a consolidated view of **how effectively healthcare
operations are being managed and how delivered services are converted
into collected revenue**.

The key business problem is:

> **How effectively is MediCare managing healthcare operations and
> converting delivered healthcare services into collected revenue across
> its hospital network?**

The analysis focuses on patient activity, hospital and department
workload, doctor activity, healthcare service utilization, billing
performance and payment collection.

### Business Objective

Analyze healthcare operations and financial performance across the
hospital network using SQL, and generate meaningful insights that can
support operational planning and revenue-related decision-making.

### Business Questions

The project is designed to answer the following questions:

1.  **How many patients, appointments and admissions are recorded across
    the hospital network?**
2.  **Which hospitals and departments have higher appointment and
    admission activity?**
3.  **How does doctor workload vary based on appointments and
    treatments?**
4.  **What are the admission patterns and average length of stay?**
5.  **How are treatment, laboratory and pharmacy services being
    utilized?**
6.  **What is the total billed amount and how much payment has been
    collected?**
7.  **What is the gap between billed revenue and collected payments?**
8.  **How can these operational and financial measures support better
    business decisions?**

------------------------------------------------------------------------

## Dataset / Source Details

The project uses the supplied **Healthcare Analytics database dataset**
and SQL insert script to build and populate a relational database in
MySQL.

### Database Structure

The database consists of **15 interconnected tables**, organized into
the following business categories:

  Category                   Tables
  -------------------------- ---------------------------------------
  Hospital Structure         `Hospitals`, `Departments`
  Healthcare Professionals   `Doctors`, `Employees`
  Patient Management         `Patients`
  Hospital Operations        `Appointments`, `Admissions`, `Rooms`
  Healthcare Services        `Treatments`, `Laboratory`
  Pharmacy & Insurance       `Medicines`, `Pharmacy`, `Insurance`
  Financial Management       `Billing`, `Payments`

Primary keys and foreign key relationships connect the tables and
support analysis across hospitals, patients, departments, doctors,
services and financial transactions.

### Database Relationships

The relational structure allows information from different operational
areas to be analyzed together. For example:

-   Patient records can be connected with appointments and admissions.
-   Hospitals can be analyzed through their departments, doctors and
    operational activity.
-   Admissions can be examined alongside room and department
    information.
-   Treatment, laboratory and pharmacy records support healthcare
    service analysis.
-   Billing and payment records support financial and collection
    analysis.

------------------------------------------------------------------------

## SQL Project / Analysis Overview

The project uses MySQL queries to analyze healthcare operations and
revenue performance across the connected database tables.

The analysis is organized around the following business areas:

### 1. Hospital Performance Analysis

-   Compare appointment and admission activity across hospitals.
-   Analyze hospital-level operational activity.
-   Examine hospital-wise billing activity.

**Business use:** - Understand differences in activity across
hospitals. - Identify hospitals with higher patient and admission
workloads. - Compare operational activity with billing performance.

### 2. Patient & Appointment Analysis

-   Analyze patient distribution and registration patterns.
-   Identify common appointment reasons.
-   Examine appointment status and monthly trends.
-   Review patient activity across available healthcare services.

**Business use:** - Understand patient activity and appointment
patterns. - Identify changes in appointment demand. - Support
patient-service planning.

### 3. Department & Doctor Workload

-   Analyze department-level appointment and admission workload.
-   Compare doctor activity based on appointments and treatments.
-   Evaluate doctor workload and performance rankings.

**Business use:** - Understand workload distribution across
departments. - Compare doctor activity using available operational
records. - Support workload monitoring and resource planning.

### 4. Admission & Resource Utilization

-   Analyze admission types and admission status.
-   Calculate average length of stay using valid admission and discharge
    dates.
-   Examine room availability, room types and room status.
-   Identify hospitals and departments with higher admission activity.

**Business use:** - Understand admission patterns. - Monitor room
utilization and availability. - Support hospital resource planning.

### 5. Healthcare Service Analysis

-   Analyze treatment volume and treatment costs.
-   Examine laboratory test volume, cost and status.
-   Identify medicines with higher pharmacy activity and revenue.
-   Analyze medicine categories and stock levels.

**Business use:** - Understand the utilization of healthcare services. -
Compare activity and costs across service types. - Monitor pharmacy
sales and medicine stock information.

### 6. Billing & Payment Analysis

-   Calculate total billed revenue.
-   Analyze bill status and billing components.
-   Examine payment methods and payment status.
-   Compare billed amounts with collected payments.
-   Identify outstanding amounts and collection gaps.

**Business use:** - Evaluate billing performance. - Monitor payment
collection. - Identify differences between billed amounts and collected
payments. - Support revenue monitoring and collection follow-up.

------------------------------------------------------------------------

## Tools / SQL Techniques Used

The project is developed using **MySQL** and the following SQL concepts
and techniques:

-   MySQL database creation
-   Table creation and modification
-   Primary key and foreign key constraints
-   `NOT NULL` and `UNIQUE` constraints
-   Data insertion and updates
-   `SELECT`, `WHERE`, `ORDER BY` and `LIMIT`
-   Aggregate functions: `COUNT()`, `SUM()`, `AVG()`, `MIN()` and
    `MAX()`
-   `GROUP BY` and `HAVING`
-   `INNER JOIN`, `LEFT JOIN` and `RIGHT JOIN`
-   Subqueries and nested queries
-   Correlated analysis where applicable
-   Window functions: `ROW_NUMBER()`, `RANK()`, `LAG()` and `LEAD()`
-   Date-based analysis
-   Multi-table relational analysis

------------------------------------------------------------------------

## Data Preparation / Analytical Considerations

Before drawing business conclusions, the data and table relationships
need to be checked to ensure that the analysis is reliable.

### Data Validation and Analysis Considerations

1.  **Data quality**
    -   Investigate missing values and potential data-quality issues
        before using records in analysis.
2.  **Primary and foreign key relationships**
    -   Check the relationships between connected tables to support
        accurate joins.
3.  **Admission date validation**
    -   Calculate length of stay only when valid admission and discharge
        dates are available.
4.  **Billing and payment relationships**
    -   Billing and payment tables may contain one-to-many
        relationships.
    -   Aggregate related records separately where necessary to avoid
        duplicate counting.
5.  **Revenue and collection distinction**
    -   Treat billed revenue and collected payment amounts as separate
        financial measures.
6.  **Dataset-based analysis**
    -   Limit calculations and conclusions to the fields and
        relationships available in the supplied dataset.

These considerations help reduce inaccurate totals and support more
reliable SQL analysis.

------------------------------------------------------------------------

## KPIs / Features Explained

The project focuses on the following operational and financial KPIs.

### Operational KPIs

  -----------------------------------------------------------------------
  KPI                                 Purpose
  ----------------------------------- -----------------------------------
  Total Patients                      Measures the number of patient
                                      records.

  Total Appointments                  Measures appointment activity.

  Total Admissions                    Measures hospital admission
                                      activity.

  Average Length of Stay              Measures the average duration of
                                      eligible admissions using valid
                                      dates.

  Total Treatments                    Measures treatment activity.

  Total Laboratory Tests              Measures laboratory service
                                      activity.

  Hospital Activity                   Supports comparison of operational
                                      activity across hospitals.

  Department Workload                 Supports comparison of activity
                                      across departments.

  Doctor Workload                     Supports comparison of doctor
                                      activity using available records.
  -----------------------------------------------------------------------

### Financial KPIs

  -----------------------------------------------------------------------
  KPI                                 Purpose
  ----------------------------------- -----------------------------------
  Total Treatment Cost                Measures the recorded cost of
                                      treatments.

  Total Pharmacy Sales                Measures sales recorded in pharmacy
                                      transactions.

  Total Billed Amount                 Measures the amount recorded
                                      through billing.

  Total Payment Collected             Measures payments recorded as
                                      collected, based on payment data
                                      and status.

  Collection Gap                      Measures the difference between
                                      billed amounts and collected
                                      payments, using correctly matched
                                      and aggregated records.

  Collection Rate (%)                 Measures collected payments as a
                                      percentage of the corresponding
                                      billed amount.
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## Key Insights / Business Interpretation

The SQL analysis is intended to generate evidence-based insights across
hospital operations and financial performance.

The following areas are important when interpreting the query results:

### 1. Hospital and Department Activity

Compare patient appointments and admissions across hospitals and
departments to understand where operational activity is concentrated.

### 2. Patient and Appointment Patterns

Review patient activity, appointment reasons, appointment statuses and
monthly trends to understand service demand.

### 3. Doctor Workload

Compare doctor appointment and treatment activity to understand workload
distribution using the available records.

### 4. Admission and Room Utilization

Examine admission types, admission status, length of stay and room
status to understand resource utilization.

### 5. Healthcare Service Utilization

Review treatment, laboratory and pharmacy activity to understand the
usage and recorded costs or revenue of different services.

### 6. Billing and Payment Collection

Compare billed amounts with collected payments to identify outstanding
amounts and collection gaps. This comparison should account for the
relationships between billing and payment records to avoid duplicate
totals.

**Note:** Specific numerical findings and rankings should be added only
after running and validating the SQL queries against the supplied
database. No numerical results are assumed in this README.

------------------------------------------------------------------------

## Recommendations / Conclusion

### Recommendations

Based on the results obtained from the SQL analysis, MediCare management
can use the findings to:

-   Monitor patient appointments and admissions across hospitals.
-   Review department and doctor workload to understand operational
    distribution.
-   Examine admission patterns and room availability to support resource
    planning.
-   Monitor treatment and laboratory service activity.
-   Review pharmacy activity, medicine categories and stock levels.
-   Compare billed amounts with collected payments to monitor collection
    performance.
-   Investigate outstanding amounts and collection gaps using correctly
    matched billing and payment records.
-   Use monthly and hospital-wise analysis to identify operational
    patterns and areas requiring attention.

### Conclusion

The MediCare project uses a relational MySQL database to examine
healthcare operations and financial performance across a hospital
network.

By connecting patient, hospital, department, doctor, admission,
healthcare service, billing and payment information, the project
provides a structured approach to understanding operational activity and
revenue collection.

The analysis brings together **healthcare operations and financial
performance**, helping identify what can be monitored across hospitals
and where further investigation may be required.

The project focuses on SQL-based business analysis and decision support.
It does not cover medical diagnosis, clinical decision-making or
predictive healthcare modeling.

------------------------------------------------------------------------

## Project Outcome

This project demonstrates practical skills in:

-   Relational database creation and management
-   MySQL and SQL querying
-   Data insertion and table relationships
-   Primary key and foreign key constraints
-   Data validation considerations
-   Aggregate and grouped analysis
-   Multi-table joins
-   Subqueries
-   Window functions
-   Healthcare operations analysis
-   Patient and appointment analysis
-   Hospital, department and doctor workload analysis
-   Admission and resource utilization analysis
-   Healthcare service analysis
-   Billing and payment collection analysis
-   Business KPI identification
-   Business insight interpretation

The final project is a **MediCare Healthcare Operations & Revenue
Analytics SQL Project** designed to transform interconnected healthcare
records into structured operational and financial analysis.

------------------------------------------------------------------------

## Project Scope

This project focuses on healthcare operations and revenue analytics
using SQL. It does not cover medical diagnosis, clinical decision-making
or predictive healthcare modeling.

------------------------------------------------------------------------

## Author

**Sowmiga K**

**Project:** MediCare -- Healthcare Operations & Revenue Analytics

**Technology:** MySQL \| SQL \| MySQL Workbench \| Git & GitHub
