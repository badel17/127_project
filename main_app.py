import customtkinter as ctk
import mysql.connector
from tkinter import messagebox
from db import StudentOrgDBMS

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db = StudentOrgDBMS()

        self.title("App Navigation")
        self.geometry("900x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.current_frame = None
        self.show_frame(SelectScreen)

    def show_frame(self, frame_class):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame_class(self)
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
            messagebox.showinfo("Successfully log in!", "Ayos")
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

class EnterAsAdmin(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.db = StudentOrgDBMS()

        ctk.CTkLabel(self, text="Admin Dashboard", font=ctk.CTkFont(size=20)).pack(pady=20)
        ctk.CTkButton(self, text="Go Back", command=lambda: master.show_frame(SelectScreen)).pack(pady=10)


if __name__ == "__main__":
    app = App() 
    app.mainloop()