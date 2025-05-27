# db.py or top of the file
import mysql.connector

class StudentOrgDBMS:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="jbcrossfire"
        )
        self.cursor = self.connection.cursor()
        self.create_database("student_org_db")
        self.use_database("student_org_db")
        self.create_tables()

    def destroy_database(self, name):
        self.cursor.execute(f"DROP DATABASE IF EXISTS {name}")

    def create_database(self, name):
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {name}")

    def use_database(self, name):
        self.cursor.execute(f"USE {name}")

    def create_tables(self):
        self.cursor.execute("""
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
            )""")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS `organization` (
                `org_id` int(6) NOT NULL,
                `org_username` varchar(30),
                `org_password` varchar(50),
                `org_name` varchar(100),
                `year_founded` YEAR,
                `org_type` varchar(50) CHECK (org_type IN ('University', 'College', 'GS', 'N/A', 'NDMO', 'University-wide')),
                CONSTRAINT organization_org_id_pk PRIMARY KEY(org_id),
                CONSTRAINT organization_org_username_uk UNIQUE KEY(org_username)
            )""")
        self.cursor.execute("""
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
                CONSTRAINT joins_org_id_fk FOREIGN KEY(org_id) REFERENCES organization(org_id)
            )""")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS `organization_event` (
                `org_id` int(6),
                `event_name` varchar(50),
                CONSTRAINT organization_event_org_id_fk FOREIGN KEY(org_id) REFERENCES organization(org_id),
                CONSTRAINT organization_event_org_event_name_uk UNIQUE KEY(event_name)
            )""")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS `fee` (
                `trans_num` int(10) NOT NULL AUTO_INCREMENT,
                `amount` int,
                `due_date` DATE,
                `org_id` int(6) NOT NULL,
                CONSTRAINT fee_org_id_fk FOREIGN KEY(org_id) REFERENCES organization(org_id),
                CONSTRAINT fee_trans_num_pk PRIMARY KEY(trans_num)
            )""")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS `pays` (
                `student_num` varchar(10) NOT NULL,
                `trans_num` int(10) NOT NULL,
                `payment_status` varchar(10) CHECK (payment_status IN ('PAID', 'NOT PAID')),
                `payment_date` DATE,
                CONSTRAINT pays_student_num_fk FOREIGN KEY(student_num) REFERENCES member(student_num),
                CONSTRAINT pays_trans_num_fk FOREIGN KEY(trans_num) REFERENCES fee(trans_num)
            )""")
        
    def checkUsernamePassword(self, username, type):
        if type == "Member":
            self.cursor.execute("SELECT mem_password FROM member WHERE mem_username = %s", (username,))
        elif type == "Organization":
            self.cursor.execute("SELECT org_password FROM organization WHERE org_username = %s", (username,))
        return self.cursor.fetchone()

    def add_student(self, student_num, first_name, last_name, mem_username, mem_password, gender, acad_year_enrolled, degree_prog):
        self.cursor.execute("INSERT INTO member(student_num, first_name, last_name, mem_username, mem_password, gender, acad_year_enrolled, degree_prog) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (student_num, first_name, last_name, mem_username, mem_password, gender, acad_year_enrolled, degree_prog))
        self.connection.commit()

    def get_stud_num(self, username):
        self.cursor.execute("SELECT student_num FROM member WHERE mem_username = %s", (username,))
        return self.cursor.fetchone()
    
    def get_stud_name(self, student_num):
        self.cursor.execute("SELECT first_name, last_name FROM member WHERE student_num = %s", (student_num,))
        results = self.cursor.fetchone()
        if results:
            first_name, last_name = results
            return first_name, last_name
        return None, None
    
    def check_if_have_org(self, student_num):
        self.cursor.execute("SELECT o.org_name FROM organization o JOIN joins j ON o.org_id = j.org_id WHERE j.student_num = %s", (student_num,))
        result = self.cursor.fetchall()
        return result if result else None
    
    def get_org_id(self, org_name):
        self.cursor.execute("SELECT org_id FROM organization WHERE org_name = %s", (org_name,))
        return self.cursor.fetchone()
    
    def get_username(self, student_num):
        self.cursor.execute("SELECT mem_username FROM member WHERE student_num = %s", (student_num,))
        return self.cursor.fetchone()

    def get_all_payments(self, student_num):
        self.cursor.execute("SELECT p.trans_num, p.payment_status, p.payment_date FROM pays p JOIN member m ON p.student_num = m.student_num WHERE m.student_num = %s", (student_num,))
        result = self.cursor.fetchall()
        return result if result else None
    
    def get_org_id_username(self, username):
        self.cursor.execute("SELECT org_id FROM organization WHERE org_username = %s", (username,))
        return self.cursor.fetchone()

    def get_org_name(self, org_id):
        self.cursor.execute("SELECT org_name FROM organization WHERE org_id = %s", (org_id,))
        return self.cursor.fetchone()
    
    def get_org_events(self, org_id):
        self.cursor.execute("SELECT * FROM organization_event WHERE org_id = %s", (org_id,))
        result = self.cursor.fetchall()
        return result if result else None

    ###############################

    def get_students(self):
        self.cursor.execute("SELECT * FROM member")
        return self.cursor.fetchall()

    def add_organization(self, org_id, org_username, org_password, org_name, year_founded, org_type):
        self.cursor.execute("INSERT INTO organization (org_id, org_username, org_password, org_name, year_founded, org_type) VALUES (%s, %s, %s, %s, %s, %s)", (org_id, org_username, org_password, org_name, year_founded, org_type,))
        self.connection.commit()

    def get_organizations(self):
        self.cursor.execute("SELECT * FROM organization")
        return self.cursor.fetchall()
    
    def member_exists(self, student_num):
        self.cursor.execute("SELECT 1 FROM member WHERE student_num = %s", (student_num))
        return self.cursor.fetchone() is not None
    
    def org_exists(self, org_id):
        self.cursor.execute("SELECT 1 FROM organization WHERE org_id = %s", (org_id))
        return self.cursor.fetchone() is not None

    def add_membership(self, student_num, org_id, membership_status, acad_year, classification, joins_type, role, semester):
        self.cursor.execute("INSERT INTO joins (student_num, org_id, membership_status, academic_year, classification, type, role, semester) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (student_num, org_id, membership_status, acad_year, classification, joins_type, role, semester,))
        self.connection.commit()

    def get_memberships(self, org_id):
        self.cursor.execute("SELECT m.student_num, m.first_name, m.last_name, m.degree_prog FROM member m JOIN joins j ON m.student_num = j.student_num JOIN organization o ON j.org_id = o.org_id WHERE o.org_id = %s", (org_id,))
        return self.cursor.fetchall()
    
    def add_event(self, org_id, event_name):
        self.cursor.execute("INSERT INTO organization_event VALUES (%s, %s)", (org_id, event_name))
        self.connection.commit()

    def add_fee(self, trans_num, amount, due_date, org_id):
        self.cursor.execute("INSERT INTO fee VALUES (%s, %s, %s, %s)", (trans_num, amount, due_date, org_id))
        self.connection.commit()

    def add_pays(self, student_num, trans_num, payment_status, payment_date):
        self.cursor.execute("INSERT INTO pays VALUES (%s, %s, %s, %s)", (student_num, trans_num, payment_status, payment_date))
        self.connection.commit()

######
    def get_memorg(self, student_num):
        self.cursor.execute("""
            SELECT org_name FROM organization o 
            JOIN joins j ON o.org_id=j.org_id 
            WHERE student_num = %s
        """, (student_num,))
        return self.cursor.fetchall()
    
    def add_memorg(self, student_num, org_id, membership_status, academic_year, classification, type, role, semester):
        self.cursor.execute("INSERT INTO joins (student_num, org_id, membership_status, academic_year, classification, type, role, semester) VALUES (%s, %s, %s, %s, %s,  %s, %s, %s)", (student_num, org_id, membership_status, academic_year, classification, type, role, semester))
        self.connection.commit()

    def get_member(self, student_num):
        self.cursor.execute("SELECT * FROM member WHERE student_num = %s", (student_num,))
        return self.cursor.fetchall()
    
    def update_member(self, mem_username, mem_password, degree_prog, student_num):
        self.cursor.execute("UPDATE member SET mem_username = %s, mem_password = %s, degree_prog = %s WHERE student_num = %s", (mem_username, mem_password, degree_prog, student_num))
        self.connection.commit()
    
    def get_pending(self, student_num):
        self.cursor.execute("""
        SELECT o.org_name, f.trans_num, f.amount, p.payment_status FROM fee f  JOIN pays p ON f.trans_num = p.trans_num  JOIN organization o ON f.org_id = o.org_id WHERE payment_status = 'NOT PAID' AND p.student_num = %s GROUP BY org_name, f.trans_num, f.amount, p.payment_status
        """, (student_num,))
        return self.cursor.fetchall()
