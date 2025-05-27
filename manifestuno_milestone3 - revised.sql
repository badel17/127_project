/*
Additional Notes:
    - Ensure you have submitted your final Milestone 2 before proceeding to Milestone 3.
    - Submit one SQL file containing all your table definitions,
    including CREATE statements with appropriate constraints.
    - Include one sample query for each project feature (e.g.,
    a sample query for CRUD of member, org, or fee using dummy data).
    - Document your SQL file (add comments) to describe the purpose of each query.
    Please let me know if you have any questions. Thank you!
*/
DROP DATABASE IF EXISTS `student_org`;
CREATE DATABASE IF NOT EXISTS `student_org`;
GRANT ALL ON student_org.* TO `our`@`localhost`;
USE `student_org`;

CREATE TABLE IF NOT EXISTS `member` (
    `student_num` varchar(10) NOT NULL,
    `first_name` varchar(100),
    `last_name` varchar(100),
    `mem_username` varchar(30),
    `mem_password` varchar(50),
    `gender` char(1),
    `acad_year_enrolled` YEAR,
    `degree_prog` varchar(8),
    CONSTRAINT member_student_num_pk PRIMARY KEY(student_num),
    CONSTRAINT member_mem_username_uk UNIQUE KEY(mem_username)
);


CREATE TABLE IF NOT EXISTS `organization` (
    `org_id` int(6) NOT NULL,
    `org_username` varchar(30),
    `org_password` varchar(50),
    `org_name` varchar(100),
    `year_founded` YEAR,
    `org_type` varchar(50), -- perform checking in front end
    CONSTRAINT organization_org_id_pk PRIMARY KEY(org_id),
    CONSTRAINT organization_org_username_uk UNIQUE KEY(org_username)
);


CREATE TABLE IF NOT EXISTS `organization_event` (
    `org_id` int(6),
    `event_name` varchar(50),
    CONSTRAINT organization_event_org_id_fk FOREIGN KEY(org_id) REFERENCES organization(org_id),
    CONSTRAINT organization_event_org_event_name_pk PRIMARY KEY(event_name)
);


CREATE TABLE IF NOT EXISTS `joins` (
    `student_num` varchar(10) NOT NULL,
    `org_id` int(6) NOT NULL,
    `membership_status` varchar(20),
    `academic_year` YEAR,
    `classification` varchar(50), -- can put check
    `type` varchar(20), -- can put check
    `role` varchar(20), -- can put check
    `semester` varchar(1) CHECK (semester IN ('1', '2', 'M')),
    CONSTRAINT joins_student_num_fk FOREIGN KEY(student_num) REFERENCES member(student_num),
    CONSTRAINT joins_org_id_fk FOREIGN KEY(org_id) REFERENCES organization(org_id),
    CONSTRAINT joins_pks PRIMARY KEY(student_num, org_id, membership_status, academic_year, classification, type, role, semester)
);


CREATE TABLE IF NOT EXISTS `fee` (
    `trans_num` int(10) NOT NULL,
    `amount` int,
    `due_date` DATE,
    `org_id` int(6) NOT NULL,
    CONSTRAINT fee_org_id_fk FOREIGN KEY(org_id) REFERENCES organization(org_id),
    CONSTRAINT fee_trans_num_pk PRIMARY KEY(trans_num)
);


CREATE TABLE IF NOT EXISTS `pays` (
    `student_num` varchar(10) NOT NULL,
    `trans_num` int(10) NOT NULL,
    `payment_status` varchar(10) CHECK (payment_status IN ('PAID', 'NOT PAID')),
    `payment_date` DATE,
    CONSTRAINT pays_student_num_fk FOREIGN KEY(student_num) REFERENCES member(student_num),
    CONSTRAINT pays_trans_num_fk FOREIGN KEY(trans_num) REFERENCES fee(trans_num),
    CONSTRAINT pays_pks PRIMARY KEY(student_num, trans_num, payment_status. payment_date)
);


-- Sample Queries
-- Insert new student
INSERT INTO member(student_num, first_name, last_name, mem_username, mem_password, gender, acad_year_enrolled, degree_prog)
VALUES ('2023-2020', 'Juan', 'Dela Cruz', 'juanOne', 'password', 'M', 2023, 'BSSTAT');


-- Insert new organization
INSERT INTO organization(org_id, org_username, org_password, org_name, year_founded, org_type)
VALUES (101010, '@c$$_uplb', 'qwerty', 'ACSS-UPLB', 2024, 'College');


-- Create a new fee entry for an organization
INSERT INTO fee (trans_num, amount, due_date, org_id)
VALUES (1010, 150, '2025-06-01', 101010);


-- Insert payment details of organization member
INSERT INTO pays VALUES ('2023-2020', 1010, 'NOT PAID', '2025-01-01');


-- Insert event of organization
INSERT INTO organization_event VALUES (101010, 'Tutorials');


-- Insert details of member in the organization
INSERT INTO joins VALUES ('2023-2020', 101010, 'ACTIVE', 2023, 'Resident', 'Records', 'Secretary', '2')


-- Read all members
SELECT * FROM member;


-- Read all organizations
SELECT * FROM organization;


-- Read all members of a specific organization and their roles
SELECT o.org_name, m.first_name, m.last_name, j.role
FROM organization o
JOIN joins j ON o.org_id = j.org_id
JOIN member m ON j.student_num = m.student_num
WHERE o.org_id = 101010;


-- Read all fees for a specific organization
SELECT * FROM fee WHERE org_id = 101010;


-- Read all events of a specific organization
SELECT o.org_name, e.event_name
FROM organization o
JOIN organization_event e ON o.org_id = e.org_id
WHERE o.org_id = 101010;


-- Update a member's degree program
UPDATE member
SET degree_prog = 'BSCS'
WHERE student_num = '2023-2020';


-- Update a member's membership status for a specific organization
UPDATE joins
SET membership_status = 'INACTIVE'
WHERE student_num = '2023-2020' AND org_id = 101010;


-- Update organization name
UPDATE organization
SET org_name = 'ASM-UPLB'
WHERE org_id = 101010;


-- Update fee amount
UPDATE fee
SET amount = 200
WHERE trans_num = 1010;


-- Delete a member (only if not referenced by foreign keys)
DELETE FROM member
WHERE student_num = '2023-2020';


-- Delete a member (from table that references it)
DELETE FROM joins
WHERE student_num = '2023-2020';


-- Delete an organization (only if not referenced)
DELETE FROM organization
WHERE org_id = 101010;


-- Delete a fee transaction
DELETE FROM fee
WHERE trans_num = 1010;


--#REPORTS TO GENERATE


INSERT INTO member(student_num, first_name, last_name, mem_username, mem_password, gender, acad_year_enrolled, degree_prog) VALUES ('2022-12345', 'Mary Grace', 'Piattos', 'mgp123', 'million', '1', 2022, 'BSCMSC');


INSERT INTO organization(org_id, org_username, org_password, org_name, year_founded, org_type) VALUES (101011, '@sd30_uplb', '12345', 'SD30-UPLB', 2000, 'University');


INSERT INTO fee (trans_num, amount, due_date, org_id)
VALUES (1011, 500, '2024-10-01', 101011);


INSERT INTO pays VALUES ('2022-12345', 1011,  'PAID', '2024-06-01');
INSERT INTO organization_event VALUES (101011, 'Orientation');


INSERT INTO joins VALUES ('2022-12345', 101011, 'INACTIVE', 2023, 'Resident', 'Finance', 'Member', '1')


--#1 View all members of the organization by role, status, gender, degree program, batch (year of membership), and committee. (Note: we assume one committee membership only per organization per semester)


SELECT o.org_id, o.org_name, m.student_num, m.first_name, m.last_name, m.gender, m.degree_prog, j.membership_status, j.academic_year, j.role, j.type
FROM joins j
JOIN organization o ON j.org_id=o.org_id
JOIN member m ON j.student_num=m.student_num
ORDER BY o.org_name, m.gender, m.degree_prog, j.academic_year,  j.role, j.membership_status, j.type;


--#2 View members for a given organization with unpaid membership fees or dues for a given semester and academic year.


SELECT m.student_num, m.first_name, m.last_name, m.acad_year_enrolled, j.semester, f.amount, f.due_date, p.payment_status, p.payment_date
FROM pays p 
JOIN member m ON p.student_num=m.student_num
JOIN fee f ON p.trans_num=f.trans_num
JOIN joins j ON p.student_num=j.student_num AND f.org_id=j.org_id
WHERE j.org_id=101010 AND j.semester = '2' AND j.academic_year=2023 AND p.payment_status='NOT PAID';


--#3 View a member’s unpaid membership fees or dues for all their organizations (Member’s POV).


SELECT o.org_name, f.trans_num, f.amount, f.due_date, p.payment_status, j.org_id
FROM pays p
JOIN fee f ON p.trans_num=f.trans_num
JOIN joins j ON p.student_num=j.student_num AND f.org_id=j.org_id
JOIN organization o ON j.org_id=o.org_id
WHERE p.student_num='2023-2020' AND p.payment_status='NOT PAID';


--#4 View all executive committee members of a given organization for a given academic year.


SELECT m.student_num, m.first_name, m.last_name, m.acad_year_enrolled, j.org_id, j.role
FROM joins j
JOIN member m ON j.student_num=m.student_num
WHERE j.org_id=101010 AND m.acad_year_enrolled=2023 AND j.role IN ('President', 'Vice President', 'Secretary', 'Treasurer', 'Auditor');


--#5 View all Presidents (or any other role) of a given organization for every academic year in reverse chronological order (current to past)


SELECT j.student_num, m.first_name, m.last_name, j.role, j.academic_year, j.semester
FROM joins j
JOIN member m ON j.student_num = m.student_num
WHERE j.org_id = 101010 AND j.role = "President"
ORDER BY j.academic_year DESC;


--#6 View all late payments made by all members of a given organization for a given semester and academic year


SELECT p.student_num, m.first_name, m.last_name, p.trans_num, p.payment_date, f.due_date
FROM pays p
JOIN fee f ON p.trans_num = f.trans_num
JOIN member m ON p.student_num = m.student_num
JOIN joins j ON p.student_num = j.student_num AND f.org_id = j.org_id
WHERE f.org_id = 101010 AND p.payment_status = 'PAID' AND p.payment_date > f.due_date AND j.academic_year = 2025 AND j.semester = '1';


--#7 View the percentage of active vs inactive members of a given organization for the last n semesters

SELECT 
    type,
    COUNT(DISTINCT student_num) AS member_count,
    ROUND(
        COUNT(DISTINCT student_num) * 100.0 /
        (SELECT COUNT(DISTINCT student_num)
         FROM joins
         WHERE org_id = 101010 
         ORDER BY academic_year DESC, semester DESC
         LIMIT '1'),
    2) AS percentage
FROM joins
WHERE org_id = ?
ORDER BY academic_year DESC, semester DESC
LIMIT '1'
GROUP BY type;


--#8 View all alumni members of a given organization as of a given date


SELECT DISTINCT m.student_num, m.first_name, m.last_name, m.acad_year_enrolled
FROM member m
JOIN joins j ON m.student_num = j.student_num
WHERE j.org_id = 101010 AND (j.academic_year < YEAR(2025) OR (j.academic_year = YEAR(2025) AND j.semester < '2')) AND j.type = 'Inactive';


--#9 View the total amount of unpaid and paid fees or dues of a given organization as of a given date


SELECT p.payment_status, SUM(f.amount) AS total_amount
FROM pays p
JOIN fee f ON p.trans_num = f.trans_num
WHERE f.org_id = 101010 AND p.payment_date <= 101010
GROUP BY p.payment_status;


--#10 View all the member/s with the highest debt of a given organization for a given semester


SELECT p.student_num, m.first_name, m.last_name, SUM(f.amount) AS total_debt
FROM pays p
JOIN fee f ON p.trans_num = f.trans_num
JOIN member m ON p.student_num = m.student_num
JOIN joins j ON p.student_num = j.student_num AND f.org_id = j.org_id
WHERE f.org_id = 101010  AND j.academic_year = 2025 AND j.semester = '2' AND p.payment_status = 'NOT PAID'
GROUP BY p.student_num
HAVING total_debt = (SELECT MAX(total_debt)FROM (SELECT p.student_num, SUM(f.amount) AS total_debt
        FROM pays p
        JOIN fee f ON p.trans_num = f.trans_num
        JOIN joins j ON p.student_num = j.student_num AND f.org_id = j.org_id
        WHERE f.org_id = 101010
          AND j.academic_year = 2025
          AND j.semester = '2'
          AND p.payment_status = 'NOT PAID'
        GROUP BY p.student_num
    ) AS debts
);

--Show list of organizations joined by the student(member)
SELECT org_name FROM organization o JOIN joins j ON o.org_id=j.org_id WHERE student_num = %s;

--Can join orgs
INSERT INTO joins (student_num, org_id, membership_status, academic_year, classification, type, role, semester) 
VALUES (%s, %s, %s, %s, %s,  %s, %s, %s);

--Can show current profile
SELECT * FROM member WHERE student_num = %s;

--Update current profile of student/member
UPDATE member SET mem_username = %s,mem_password = %s,  degree_prog = %s WHERE student_num = %s;

--Show pending fees from different organization
SELECT o.org_name, f.trans_num, f.amount, p.payment_status 
    FROM fee f  
    JOIN pays p ON f.trans_num = p.trans_num 
    JOIN organization o ON f.org_id = o.org_id 
    WHERE payment_status = 'NOT PAID' AND p.student_num = %s 
    GROUP BY org_name, f.trans_num, f.amount, p.payment_status;



