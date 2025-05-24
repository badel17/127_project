import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from db import StudentOrgDBMS  # Import your DB class

class StudentOrgApp:
    def __init__(self, root):
        self.db = StudentOrgDBMS()
        self.root = root
        self.root.title("Student Organization Management")

        tab_control = ttk.Notebook(root)

        self.tab_members = ttk.Frame(tab_control)
        self.tab_orgs = ttk.Frame(tab_control)
        #self.tab_memberships = ttk.Frame(tab_control) # JOINS relationship of member to organization
        self.tab_org_events = ttk.Frame(tab_control)
        self.tab_fees = ttk.Frame(tab_control)
        self.tab_pays = ttk.Frame(tab_control)
        self.tab_reports = ttk.Frame(tab_control)

        tab_control.add(self.tab_members, text="Students")
        tab_control.add(self.tab_orgs, text="Organizations")
        #tab_control.add(self.tab_memberships, text="Memberships")
        tab_control.add(self.tab_org_events, text="Events")
        tab_control.add(self.tab_fees, text="Fees")
        tab_control.add(self.tab_pays, text="Payments")
        tab_control.add(self.tab_reports, text="Reports")
        tab_control.pack(expand=1, fill='both')

        self.build_orgs_tab()
        self.build_members_tab()
        #self.build_memberships_tab()
        self.build_events_tab()
        self.build_fees_tab()
        self.build_pays_tab()

    def build_members_tab(self):
        tk.Label(self.tab_members, text="Student Number:").grid(row=0, column=0)
        self.mem_student_num = tk.Entry(self.tab_members)
        self.mem_student_num.grid(row=0, column=1)

        tk.Label(self.tab_members, text="First Name:").grid(row=1, column=0)
        self.mem_first_name = tk.Entry(self.tab_members)
        self.mem_first_name.grid(row=1, column=1)

        tk.Label(self.tab_members, text="Last Name:").grid(row=2, column=0)
        self.mem_last_name = tk.Entry(self.tab_members)
        self.mem_last_name.grid(row=2, column=1)

        tk.Label(self.tab_members, text="Username:").grid(row=3, column=0)
        self.mem_username = tk.Entry(self.tab_members)
        self.mem_username.grid(row=3, column=1)

        tk.Label(self.tab_members, text="Password:").grid(row=4, column=0)
        self.mem_password = tk.Entry(self.tab_members, show="*")
        self.mem_password.grid(row=4, column=1)

        # Make it a dropdown options
        tk.Label(self.tab_members, text="Gender:").grid(row=5, column=0)
        self.mem_gender = tk.Entry(self.tab_members)
        self.mem_gender.grid(row=5, column=1)
        
        # tk.Label(self.tab_members, text="Gender:").grid(row=4, column=0)

        # self.gender_var = tk.StringVar()
        # self.gender_var.set("Select")  # default value shown

        # # Create dropdown menu
        # gender_options = ["M", "F", "Other"]  # customize as needed
        # self.mem_gender = tk.OptionMenu(self.tab_members, self.gender_var, *gender_options)
        # self.mem_gender.grid(row=4, column=1)

        tk.Label(self.tab_members, text="Academic Year:").grid(row=6, column=0)
        self.mem_acad_year = tk.Entry(self.tab_members)
        self.mem_acad_year.grid(row=6, column=1)

        tk.Label(self.tab_members, text="Degree Program:").grid(row=7, column=0)
        self.mem_deg_prog = tk.Entry(self.tab_members)
        self.mem_deg_prog.grid(row=7, column=1)

        tk.Label(self.tab_members, text="Organization ID:").grid(row=0, column=3)
        self.joins_org_id = tk.Entry(self.tab_members)
        self.joins_org_id.grid(row=0, column=4)

        tk.Label(self.tab_members, text="Status:").grid(row=2, column=3)
        self.joins_status = tk.Entry(self.tab_members)
        self.joins_status.grid(row=2, column=4)

        tk.Label(self.tab_members, text="Classification:").grid(row=3, column=3)
        self.joins_classification = tk.Entry(self.tab_members)
        self.joins_classification.grid(row=3, column=4)

        tk.Label(self.tab_members, text="Membership Type:").grid(row=4, column=3)
        self.joins_type = tk.Entry(self.tab_members)
        self.joins_type.grid(row=4, column=4)

        tk.Label(self.tab_members, text="Role:").grid(row=5, column=3)
        self.joins_role = tk.Entry(self.tab_members)
        self.joins_role.grid(row=5, column=4)

        tk.Label(self.tab_members, text="Semester:").grid(row=6, column=3)
        self.joins_semester = tk.Entry(self.tab_members)
        self.joins_semester.grid(row=6, column=4)

        tk.Button(self.tab_members, text="Add Student", command=self.handle_add_membership).grid(row=7, column=3, columnspan=2)

        self.student_list = tk.Text(self.tab_members, height=10, width=100)
        self.student_list.grid(row=8, column=0, columnspan=5)
        self.refresh_members()

    def handle_add_membership(self):
        self.add_member() # Add a student to the database
        self.add_membership()


    def add_member(self):
        student_num = self.mem_student_num.get()
        first_name = self.mem_first_name.get()
        last_name = self.mem_last_name.get()
        mem_username = self.mem_username.get()
        mem_password = self.mem_password.get()
        gender = self.mem_gender.get()
        acad_year_enrolled = self.mem_acad_year.get()
        degree_prog = self.mem_deg_prog.get()
        self.db.add_student(student_num, first_name, last_name, mem_username, mem_password, gender, acad_year_enrolled, degree_prog)
        self.refresh_members()

    def refresh_members(self):     # Refreshes and displays all students 
        self.student_list.delete('1.0', tk.END) # start from line 1, go until end
        for student in self.db.get_students():  # fetch all the students by quering select * from member
            self.student_list.insert(tk.END, f"{student}\n")

    def build_orgs_tab(self):
        tk.Label(self.tab_orgs, text="Name:").grid(row=0, column=0)
        self.org_name = tk.Entry(self.tab_orgs)
        self.org_name.grid(row=0, column=1)

        tk.Label(self.tab_orgs, text="Organization ID:").grid(row=1, column=0)
        self.org_id = tk.Entry(self.tab_orgs)
        self.org_id.grid(row=1, column=1)

        tk.Label(self.tab_orgs, text="Username:").grid(row=2, column=0)
        self.org_username = tk.Entry(self.tab_orgs)
        self.org_username.grid(row=2, column=1)

        tk.Label(self.tab_orgs, text="Password:").grid(row=3, column=0)
        self.org_password = tk.Entry(self.tab_orgs)
        self.org_password.grid(row=3, column=1)

        tk.Label(self.tab_orgs, text="Year founded:").grid(row=4, column=0)
        self.org_year_founded = tk.Entry(self.tab_orgs)
        self.org_year_founded.grid(row=4, column=1)

        tk.Label(self.tab_orgs, text="Organization Type:").grid(row=5, column=0)
        self.org_type = tk.Entry(self.tab_orgs)
        self.org_type.grid(row=5, column=1)

        tk.Button(self.tab_orgs, text="Add Organization", command=self.add_organization).grid(row=6, column=0, columnspan=2)

        self.org_list = tk.Text(self.tab_orgs, height=10, width=50)
        self.org_list.grid(row=7, column=0, columnspan=2)
        self.refresh_organizations()

    def add_organization(self):
        org_name = self.org_name.get()
        org_username = self.org_username.get()
        org_password = self.org_password.get()
        org_id = self.org_id.get()
        year_founded = self.org_year_founded.get()
        org_type = self.org_type.get()
        self.db.add_organization(org_id, org_username, org_password, org_name, year_founded, org_type)
        self.refresh_organizations()

    def refresh_organizations(self):
        self.org_list.delete('1.0', tk.END)
        for org in self.db.get_organizations():
            self.org_list.insert(tk.END, f"{org}\n")

    def build_memberships_tab(self):
        tk.Label(self.tab_memberships, text="Student Number:").grid(row=0, column=0)
        self.joins_mem_st_num = tk.Entry(self.tab_memberships)
        self.joins_mem_st_num.grid(row=0, column=1)

        tk.Label(self.tab_memberships, text="Organization ID:").grid(row=1, column=0)
        self.joins_org_id = tk.Entry(self.tab_memberships)
        self.joins_org_id.grid(row=1, column=1)

        tk.Label(self.tab_memberships, text="Status:").grid(row=2, column=0)
        self.joins_status = tk.Entry(self.tab_memberships)
        self.joins_status.grid(row=2, column=1)

        tk.Label(self.tab_memberships, text="Academic Year:").grid(row=3, column=0)
        self.joins_acad_year = tk.Entry(self.tab_memberships)
        self.joins_acad_year.grid(row=3, column=1)

        tk.Label(self.tab_memberships, text="Classification:").grid(row=4, column=0)
        self.joins_classification = tk.Entry(self.tab_memberships)
        self.joins_classification.grid(row=4, column=1)

        tk.Label(self.tab_memberships, text="Membership Type:").grid(row=5, column=0)
        self.joins_type = tk.Entry(self.tab_memberships)
        self.joins_type.grid(row=5, column=1)

        tk.Label(self.tab_memberships, text="Role:").grid(row=6, column=0)
        self.joins_role = tk.Entry(self.tab_memberships)
        self.joins_role.grid(row=6, column=1)

        tk.Label(self.tab_memberships, text="Semester:").grid(row=7, column=0)
        self.joins_semester = tk.Entry(self.tab_memberships)
        self.joins_semester.grid(row=7, column=1)

        tk.Button(self.tab_memberships, text="Add Membership", command=self.add_membership).grid(row=8, column=0, columnspan=2)

        self.mem_list = tk.Text(self.tab_memberships, height=10, width=60)
        self.mem_list.grid(row=9, column=0, columnspan=2)
        self.refresh_memberships()

    def add_membership(self):
        try:
            student_num = self.mem_student_num.get()
            org_id = self.joins_org_id.get()
            membership_status = self.joins_status.get()
            academic_year = self.joins_acad_year.get()
            classification = self.joins_classification.get()
            joins_type = self.joins_type.get()
            role = self.joins_role.get()
            semester = self.joins_semester.get()

            # Check if the organization exists in the database
            if not self.db.org_exists(org_id):
                messagebox.showerror("Organization not found!")
                return
            
            self.db.add_membership(student_num, org_id, membership_status, academic_year, classification, joins_type, role, semester)
            self.refresh_memberships()
        except ValueError:
            messagebox.showerror("Invalid Input")

    def refresh_memberships(self):
        self.mem_list.delete('1.0', tk.END)
        for mem in self.db.get_memberships():
            self.mem_list.insert(tk.END, f"Membership #{mem[0]}: {mem[1]} in {mem[2]}\n")

    def build_events_tab(self):
        tk.Label(self.tab_org_events, text="Organization ID: ").grid(row=0, column=0)
        self.events_org_id = tk.Entry(self.tab_org_events)
        self.events_org_id.grid(row=0, column=1)

        tk.Label(self.tab_org_events, text="Event Name: ").grid(row=2, column=0)
        self.events_name = tk.Entry(self.tab_org_events)
        self.events_name.grid(row=2, column=1)

        tk.Button(self.tab_org_events, text="Add Event", command=self.add_event).grid(row=3, column=0, columnspan=2)

    def add_event(self):
        org_id = self.events_org_id.get()
        event_name = self.events_name.get()

        self.db.add_event(org_id, event_name)

    # Add refresh tab function for add_event

    def build_fees_tab(self):
        tk.Label(self.tab_fees, text="Transaction Number:").grid(row=0, column=0)
        self.fees_trans_num = tk.Entry(self.tab_fees)
        self.fees_trans_num.grid(row=0, column=1)

        tk.Label(self.tab_fees, text="Amount:").grid(row=1, column=0)
        self.fees_amount = tk.Entry(self.tab_fees)
        self.fees_amount.grid(row=1, column=1)

        tk.Label(self.tab_fees, text="Due Date:").grid(row=2, column=0)
        self.fees_due = DateEntry(self.tab_fees, date_pattern='yyyy-mm-dd')
        self.fees_due.grid(row=2, column=1)

        tk.Label(self.tab_fees, text="Organization ID:").grid(row=3, column=0)
        self.fees_org_id = tk.Entry(self.tab_fees)
        self.fees_org_id.grid(row=3, column=1)

        tk.Button(self.tab_fees, text="Add Fee", command=self.add_fee).grid(row=4, column=0, columnspan=2)

    def add_fee(self):
        trans_num = self.fees_trans_num.get()
        amount = self.fees_amount.get()
        due = self.fees_due.get()
        org_id = self.fees_org_id.get()

        self.db.add_fee(trans_num, amount, due, org_id)

    def build_pays_tab(self):
        tk.Label(self.tab_pays, text="Student Number:").grid(row=0, column=0)
        self.pays_stud_num = tk.Entry(self.tab_pays)
        self.pays_stud_num.grid(row=0, column=1)

        tk.Label(self.tab_pays, text="Transaction Number:").grid(row=1, column=0)
        self.pays_trans_num = tk.Entry(self.tab_pays)
        self.pays_trans_num.grid(row=1, column=1)

        tk.Label(self.tab_pays, text="Status:").grid(row=2, column=0)
        self.pays_status = DateEntry(self.tab_pays, date_pattern='yyyy-mm-dd')
        self.pays_status.grid(row=2, column=1)

        tk.Label(self.tab_pays, text="Date paid:").grid(row=3, column=0)
        self.pays_date = tk.Entry(self.tab_pays)
        self.pays_date.grid(row=3, column=1)

        tk.Button(self.tab_pays, text="Add Payment", command=self.add_payment).grid(row=4, column=0, columnspan=2)

    def add_payment(self):
        student_num = self.pays_stud_num.get()
        trans_num = self.pays_trans_num.get()
        status = self.pays_status.get()
        date = self.pays_date.get()

        self.db.add_pays(student_num, trans_num, status, date)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentOrgApp(root)
    root.mainloop()
