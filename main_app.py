import customtkinter as ctk
import mysql.connector
from tkinter import messagebox
from db import StudentOrgDBMS

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db = StudentOrgDBMS()

        self.title("Student Organization")
        self.geometry("900x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.resizable(False, False)

        self.current_frame = None
        self.show_frame(SelectScreen)

    def show_frame(self, frame_class, *args):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame_class(self, *args)
        self.current_frame.pack(expand=True, fill="both")


class SelectScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Welcome!", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=30)
        ctk.CTkLabel(self, text="Please choose whether you are a member or admin.",
                     font=ctk.CTkFont(size=18)).pack(pady=30)

        ctk.CTkButton(self, text="Member", command=lambda: master.show_frame(EnterAsMember)).pack(pady=10)
        ctk.CTkButton(self, text="Administrator", command=lambda: master.show_frame(EnterAsAdmin)).pack(pady=10)


class EnterAsMember(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.db = StudentOrgDBMS()

        ctk.CTkLabel(self, text="Member Dashboard", font=ctk.CTkFont(size=20)).pack(pady=20)
        ctk.CTkButton(self, text="Go Back", command=lambda: master.show_frame(SelectScreen)).pack(pady=10)

        self._form_one()

    def _form_one(self):
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        ctk.CTkButton(self, text='Sign In', command=self.sign_in).pack(pady=10)
        
        ctk.CTkLabel(self, text="Have no account yet?", font=ctk.CTkFont(size=10)).pack(pady=2)
        ctk.CTkButton(self, text="Sign Up", command=lambda: self.master.show_frame(AddMember)).pack(pady=2)
    
    def _get_credentials(self):
        return self.username_entry.get().strip(), self.password_entry.get().strip()

    def sign_in(self):
        username, password = self._get_credentials()
        # Check if username and password empty, return error message
        if not username or not password:
            messagebox.showerror("Error", "Please fill up the form.")
            return
        
        checkpassword = self.db.checkUsernamePassword(username)

        if checkpassword and checkpassword[0] == password:
            #messagebox.showinfo("Successfully log in!", "Ayos")
            self.master.show_frame(MemberScreen, username)
        else:
            messagebox.showerror("Failed", "Invalid username or password.")

class AddMember(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.db = StudentOrgDBMS()

        ctk.CTkLabel(self, text="Please fill up the form", font=ctk.CTkFont(size=20)).pack(pady=20)

        self._form_two()
        ctk.CTkButton(self, text="Submit", command=self.handle_addMembership).pack(pady=10)

    def _form_two(self):
        self.stud_num_entry = ctk.CTkEntry(self, placeholder_text="Student Number")
        self.stud_num_entry.pack(pady=10)

        self.fname_entry = ctk.CTkEntry(self, placeholder_text="First Name")
        self.fname_entry.pack(pady=10)

        self.lname_entry = ctk.CTkEntry(self, placeholder_text="Last Name")
        self.lname_entry.pack(pady=10)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        self.gender_entry = ctk.CTkOptionMenu(self, values=["M", "F", "X"])
        self.gender_entry.pack(pady=10)

        self.acad_yr_entry = ctk.CTkEntry(self, placeholder_text="Academic Year Enrolled")
        self.acad_yr_entry.pack(pady=10)

        self.deg_prog_entry = ctk.CTkEntry(self, placeholder_text="Degree Program (ex: BSSTAT, BSCS)")
        self.deg_prog_entry.pack(pady=10)

    def handle_addMembership(self):
        self.addMember()
        self.master.show_frame(MemberScreen, self.username_entry.get().strip())

    def addMember(self):
        student_num = self.stud_num_entry.get().strip()
        first_name = self.fname_entry.get().strip()
        last_name = self.lname_entry.get().strip()
        mem_username = self.username_entry.get().strip()
        mem_password = self.password_entry.get().strip()
        gender = self.gender_entry.get()
        acad_year_enrolled = self.acad_yr_entry.get().strip()
        degree_prog = self.deg_prog_entry.get().strip()
        self.db.add_student(student_num, first_name, last_name, mem_username, mem_password, gender, acad_year_enrolled, degree_prog)

class MemberScreen(ctk.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username

        self.db = StudentOrgDBMS()

        # Access the information of the student
        student_num = self.db.get_stud_num(self.username)
        first_name, last_name = self.db.get_stud_name(student_num[0])

        ctk.CTkLabel(self, text=f"Hello, {first_name}!", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        ctk.CTkButton(self, text="Sign out", command=lambda: master.show_frame(SelectScreen)).pack(pady=10)

        tab_view = ctk.CTkTabview(self, width=900, height=600)
        tab_view.pack(pady=10)

        tab_view.add("Home")
        tab_view.add("Organizations")
        tab_view.add("Payments")
        tab_view.add("Profile")

        home_tab = tab_view.tab("Home")
        org_tab = tab_view.tab("Organizations")
        pay_tab = tab_view.tab("Payments")
        profile_tab = tab_view.tab("Profile")

        self.build_home(home_tab)
        self.build_profile_tab(profile_tab, first_name, last_name)
        self.build_org_tab(org_tab, student_num[0])

    def build_home(self, parent):
        ctk.CTkLabel(parent, text="Welcome to the database!", font=ctk.CTkFont(size=14, weight="normal")).pack(pady=10)

    def build_org_tab(self, parent, student_num):
        orgs = self.db.check_if_have_org(student_num)

        if orgs:
            scroll_frame = ctk.CTkScrollableFrame(parent, width=300, height=200)
            scroll_frame.pack(pady=10)

            for org in orgs:
                ctk.CTkLabel(scroll_frame, text=org[0]).pack(anchor="w", padx=10, pady=5)
        else:
            ctk.CTkLabel(parent, text="You have not yet joined any org", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)

        ctk.CTkButton(parent, text="Join Org", command=lambda: self.master.show_frame(JoinOrg, student_num)).pack(pady=10)

    def build_profile_tab(self, parent, first_name, last_name):
        ctk.CTkLabel(parent, text=f"{first_name} {last_name}", font=ctk.CTkFont(size=14, weight="normal")).pack(pady=10)

class JoinOrg(ctk.CTkFrame):
    def __init__(self, master, student_num):
        super().__init__(master)
        self.student_num = student_num

        self.db = StudentOrgDBMS()

        self.username = self.db.get_username(student_num)[0]

        ctk.CTkButton(self, text="Back", command=lambda: master.show_frame(MemberScreen, self.username)).pack(pady=10) # Go back

        self.formthree()
        ctk.CTkButton(self, text="Join", command=self.handle_joining).pack(pady=10)

    def formthree(self):
        self.join_org_name = ctk.CTkEntry(self, placeholder_text="Organization Name")
        self.join_org_name.pack(pady=10)

        #self.org_id = self.db.get_org_id(self.join_org_name.get().strip())

        self.join_acad_year = ctk.CTkEntry(self, placeholder_text="Academic Year")
        self.join_acad_year.pack(pady=10)

        self.join_sem = ctk.CTkOptionMenu(self, values=["1", "2", "M"])
        self.join_sem.pack(pady=10)

        # When a student joins, membership status is default to active,classification is default to 'resident', type is NULL, role is NULL
       #print(self.org_id)

    def handle_joining(self):
        org_name = self.join_org_name.get().strip()
        org_id_tuple = self.db.get_org_id(org_name)

        if not org_id_tuple:
            messagebox.showerror("Failed", "Invalid organization")
            return

        self.org_id = org_id_tuple[0]

        self.joinMember()
        self.master.show_frame(MemberScreen, self.username) # Go back

    def joinMember(self):
        academic_year = self.join_acad_year.get().strip()
        semester = self.join_sem.get()

        self.db.add_membership(self.student_num, self.org_id, "Active", academic_year, "Resident", None, None, semester)


#####################################################################

class EnterAsAdmin(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.db = StudentOrgDBMS()

        ctk.CTkLabel(self, text="Admin Dashboard", font=ctk.CTkFont(size=20)).pack(pady=20)
        ctk.CTkButton(self, text="Go Back", command=lambda: master.show_frame(SelectScreen)).pack(pady=10)


if __name__ == "__main__":
    app = App() 
    app.mainloop()