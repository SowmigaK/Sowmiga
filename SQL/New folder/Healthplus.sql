#================================================================================================================================================================
# Database creation
#================================================================================================================================================================
CREATE DATABASE HealthPlus;
USE HealthPLus;

#==================================================================================================================================================================
# Table creation and insertion of values
#==================================================================================================================================================================
CREATE TABLE Clinics(
clinic_id varchar(6) not null,
clinic_name varchar(50) not null,
clinic_type varchar(50) not null,
city varchar(50) not null,
state varchar(50) not null,
established_year int not null,
contact_number varchar(15) not null,

CONSTRAINT pk_clinic_id PRIMARY KEY(clinic_id)

);

INSERT INTO `Clinics` (`clinic_id`, `clinic_name`, `clinic_type`, `city`, `state`, `established_year`, `contact_number`) VALUES
('C001', 'HealthPlus Diagnostic Clinic - Kozhikode', 'Diagnostic', 'Kozhikode', 'Kerala', 2018, 8039233214),
('C002', 'HealthPlus Wellness Clinic - Kozhikode', 'Wellness', 'Kozhikode', 'Kerala', 2020, 8081973699),
('C003', 'HealthPlus Telemedicine Hub Clinic - Hyderabad', 'Telemedicine Hub', 'Hyderabad', 'Telangana', 2017, 8063272951),
('C004', 'HealthPlus Primary Care Clinic - Delhi', 'Primary Care', 'Delhi', 'Delhi', 2022, 8017560480),
('C005', 'HealthPlus Diagnostic Clinic - Pune', 'Diagnostic', 'Pune', 'Maharashtra', 2015, 8058178397),
('C006', 'HealthPlus Wellness Clinic - Coimbatore', 'Wellness', 'Coimbatore', 'Tamil Nadu', 2017, 8023279282),
('C007', 'HealthPlus Telemedicine Hub Clinic - Coimbatore', 'Telemedicine Hub', 'Coimbatore', 'Tamil Nadu', 2013, 8002761612),
('C008', 'HealthPlus Primary Care Clinic - Vijayawada', 'Primary Care', 'Vijayawada', 'Andhra Pradesh', 2021, 8006528630),
('C009', 'HealthPlus Diagnostic Clinic - Hyderabad', 'Diagnostic', 'Hyderabad', 'Telangana', 2019, 8048625702),
('C010', 'HealthPlus Wellness Clinic - Mysuru', 'Wellness', 'Mysuru', 'Karnataka', 2021, 8061112422),
('C011', 'HealthPlus Telemedicine Hub Clinic - Pune', 'Telemedicine Hub', 'Pune', 'Maharashtra', 2014, 8038573415),
('C012', 'HealthPlus Primary Care Clinic - Mangaluru', 'Primary Care', 'Mangaluru', 'Karnataka', 2022, 8018409053),
('C013', 'HealthPlus Diagnostic Clinic - Kozhikode', 'Diagnostic', 'Kozhikode', 'Kerala', 2018, 8056665812),
('C014', 'HealthPlus Wellness Clinic - Coimbatore', 'Wellness', 'Coimbatore', 'Tamil Nadu', 2017, 8067343415),
('C015', 'HealthPlus Telemedicine Hub Clinic - Hyderabad', 'Telemedicine Hub', 'Hyderabad', 'Telangana', 2023, 8036471764),
('C016', 'HealthPlus Primary Care Clinic - Madurai', 'Primary Care', 'Madurai', 'Tamil Nadu', 2020, 8045782464),
('C017', 'HealthPlus Diagnostic Clinic - Pune', 'Diagnostic', 'Pune', 'Maharashtra', 2022, 8092469973),
('C018', 'HealthPlus Wellness Clinic - Kozhikode', 'Wellness', 'Kozhikode', 'Kerala', 2017, 8035054324);


