import tkinter as tk
from PIL import Image, ImageTk  # Import PIL for image handling
import sqlite3
from tkinter import messagebox as ms
import re
import subprocess

# Function to create a custom button with hover effect
def create_button(frame, text, command):
    btn = tk.Button(frame, text=text, command=command, font=("Helvetica", 14), width=20, 
                    bg="#007bff", fg="white", activebackground="#0056b3", bd=0)
    
    # Button hover effects
    btn.bind("<Enter>", lambda e: btn.config(bg="#0056b3"))
    btn.bind("<Leave>", lambda e: btn.config(bg="#007bff"))
    
    return btn

root = tk.Tk()
root.title("Registration")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size to full screen
root.geometry(f"{screen_width}x{screen_height}")

# Load the background image
bg_image = Image.open("bg images/b1.jpg")  
bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)  # Resize the image to fill the window
bg_image_tk = ImageTk.PhotoImage(bg_image)


# Create a Canvas and set the background image
canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_image_tk, anchor="nw")

# Global variables
name = tk.StringVar()
Email = tk.StringVar()
PhoneNo = tk.StringVar()
password = tk.StringVar()
password1 = tk.StringVar()

# Database setup
db = sqlite3.connect('knee.db')
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS KneeReg (name TEXT, Email TEXT, Phoneno TEXT, password TEXT)")
db.commit()

# Password validation
def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%']
    if len(passwd) < 6:
        return 'Password should be at least 6 characters long.'
    if len(passwd) > 20:
        return 'Password should not be more than 20 characters long.'
    if not any(char.isdigit() for char in passwd):
        return 'Password should contain at least one numeral.'
    if not any(char.isupper() for char in passwd):
        return 'Password should contain at least one uppercase letter.'
    if not any(char.islower() for char in passwd):
        return 'Password should contain at least one lowercase letter.'
    if not any(char in SpecialSym for char in passwd):
        return 'Password should contain at least one special symbol ($, @, #, %).'
    return None  # No issues with the password

# Redirect to login page (run login.py)
def open_login_page():
    root.destroy()  # Close the current window
    try:
        subprocess.run(['python', 'login.py'])  # Run the existing login.py script
    except Exception as e:
        ms.showinfo("Error", f"Failed to open login page: {e}")

# Insert data into the database and redirect to login page
def insert():
    fname = name.get().strip()
    email = Email.get().strip()
    mobile = PhoneNo.get().strip()
    pwd = password.get()
    cnpwd = password1.get()
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    # Validation
    if not fname or fname.isdigit():
        ms.showinfo("Message", "Please enter a valid name.")
        return
    if not re.search(regex, email):
        ms.showinfo("Message", "Please enter a valid email.")
        return
    pwd_error = password_check(pwd)
    if pwd_error:
        ms.showinfo("Message", pwd_error)
        return
    if pwd != cnpwd:
        ms.showinfo("Message", "Password and Confirm Password must be the same.")
        return
    if len(mobile) != 10 or not mobile.isdigit():
        ms.showinfo("Message", "Please enter a valid 10-digit mobile number.")
        return
 
    # If all validations pass, insert the data
    with sqlite3.connect('knee.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO KneeReg (name, Email, Phoneno, password) VALUES (?, ?, ?, ?)',
                       (fname, email, mobile, pwd))
        conn.commit()
        ms.showinfo('Success!', 'Account Created Successfully!')
        open_login_page()  # Redirect to login page after success

# Title label
title_label = tk.Label(root, text="Image Forgery Detection ", font=("Times New Roman", 35, "bold"),
                       bg="lightgray", fg="black", width=55, height=1)
title_label.place(x=-100, y=0)

# Load and display the logo
logo_image = Image.open('bg images/logo.webp')  # Change 'logo.png' to your logo filename
logo_image = logo_image.resize((100, 55), Image.LANCZOS)  # Resize logo as needed
logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = tk.Label(root, image=logo_photo, bg='lightgray')
logo_label.place(x=0, y=0)  # Center the logo
       

# Main registration form layout using grid for flexible layout
form_frame = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.GROOVE, padx=20, pady=20)
form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

title = tk.Label(form_frame, text="Registration Form", font=("Helvetica", 22, "bold"), bg="#ffffff", fg="#333333")
title.grid(row=0, columnspan=2, pady=20)

# Name field
label_name = tk.Label(form_frame, text="Name:", font=("Arial", 14), bg="#ffffff", fg="#333333")
label_name.grid(row=1, column=0, sticky=tk.W, pady=(5, 2), padx=10)
entry_name = tk.Entry(form_frame, textvariable=name, font=("Arial", 12), bd=2, width=30, 
                      relief=tk.SUNKEN, bg="#f7f7f7", highlightbackground="#007bff")
entry_name.grid(row=1, column=1, pady=(5, 5))

# Email field
label_email = tk.Label(form_frame, text="Email:", font=("Arial", 14), bg="#ffffff", fg="#333333")
label_email.grid(row=2, column=0, sticky=tk.W, pady=(5, 2), padx=10)
entry_email = tk.Entry(form_frame, textvariable=Email, font=("Arial", 12), bd=2, width=30, 
                       relief=tk.SUNKEN, bg="#f7f7f7", highlightbackground="#007bff")
entry_email.grid(row=2, column=1, pady=(5, 5))

# Password field
label_password = tk.Label(form_frame, text="Password:", font=("Arial", 14), bg="#ffffff", fg="#333333")
label_password.grid(row=3, column=0, sticky=tk.W, pady=(5, 2), padx=10)
entry_password = tk.Entry(form_frame, textvariable=password, font=("Arial", 12), bd=2, width=30, 
                          relief=tk.SUNKEN, bg="#f7f7f7", highlightbackground="#007bff", show="*")
entry_password.grid(row=3, column=1, pady=(5, 5))

# Re-enter Password field
label_password1 = tk.Label(form_frame, text="Re-enter Password:", font=("Arial", 14), bg="#ffffff", fg="#333333")
label_password1.grid(row=4, column=0, sticky=tk.W, pady=(5, 2), padx=10)
entry_password1 = tk.Entry(form_frame, textvariable=password1, font=("Arial", 12), bd=2, width=30, 
                           relief=tk.SUNKEN, bg="#f7f7f7", highlightbackground="#007bff", show="*")
entry_password1.grid(row=4, column=1, pady=(5, 5))

# Phone No field
label_phone = tk.Label(form_frame, text="Phone No:", font=("Arial", 14), bg="#ffffff", fg="#333333")
label_phone.grid(row=5, column=0, sticky=tk.W, pady=(5, 2), padx=10)
entry_phone = tk.Entry(form_frame, textvariable=PhoneNo, font=("Arial", 12), bd=2, width=30, 
                       relief=tk.SUNKEN, bg="#f7f7f7", highlightbackground="#007bff")
entry_phone.grid(row=5, column=1, pady=(5, 5))


# Create Account button
create_button = create_button(form_frame, "Create Account", insert)
create_button.grid(row=6, columnspan=2, pady=(20, 5))

# Already have an account? label
already_label = tk.Label(form_frame, text="Already have an account?", font=("Arial", 12), bg="#ffffff", fg="#333333")
already_label.grid(row=7, column=0, sticky=tk.W, pady=(5, 2), padx=10)

# Log In button
login_button = tk.Button(form_frame, text="Log In", font=("Arial", 12), fg="blue", bg="#ffffff", bd=0, command=open_login_page)
login_button.grid(row=7, column=1, sticky=tk.W, pady=(5, 5))

# Ensure the window remains responsive and updates with the background image
root.pack_propagate(False)
root.update()
# Start the main loop
root.mainloop()
