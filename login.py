import tkinter as tk
import sqlite3
from tkinter import messagebox as ms
from PIL import Image, ImageTk
from tkinter import font

root = tk.Tk()
root.configure(background='white')

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Login")

# Load and set the background image
image2 = Image.open('bg images/b2.jpg')
image2 = image2.resize((w, h), Image.LANCZOS)
background_image = ImageTk.PhotoImage(image2)
background_label = tk.Label(root, image=background_image)
background_label.image = background_image
background_label.place(x=0, y=0)

# Set up global variables
Email = tk.StringVar()
password = tk.StringVar()

# Function to handle the login process
def login():
    with sqlite3.connect('knee.db') as db:
        c = db.cursor()

        find_entry = 'SELECT * FROM KneeReg WHERE Email = ? AND password = ?'
        c.execute(find_entry, [(Email.get()), (password.get())])
        result = c.fetchall()

        if result:
            ms.showinfo("Message", "Login successfully")
            from subprocess import call
            call(['python', 'main.py'])
        else:
            ms.showerror('Oops!', 'Username or password did not match.')

# Function to handle forgot password
def forgot():
    from subprocess import call
    call(['python', 'forgot password.py'])

def main():
    from subprocess import call
    call(['python', 'main.py'])

# Function to open the registration page
def reg():
    from subprocess import call
    call(['python', 'registration.py'])

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


# Create a frame for the login section
login_frame = tk.Frame(root, bg="white", bd=2, relief=tk.GROOVE, padx=20, pady=20)
login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Title Label
title_label = tk.Label(login_frame, text="Login Here", font=("Helvetica", 24, "bold"), bg="white", fg="black")
title_label.grid(row=0, column=0, columnspan=2, pady=20)

# Login Labels and Fields
label_font = font.Font(family='Cambria', size=14)
entry_font = font.Font(family='Arial', size=12)

a12 = tk.Label(login_frame, text='Enter Email', bg='white', font=label_font)
a12.grid(row=1, column=0, sticky='w', pady=10)
b11 = tk.Entry(login_frame, textvariable=Email, font=entry_font, width=30)
b11.grid(row=1, column=1, pady=10, padx=10)

a13 = tk.Label(login_frame, text='Enter Password', bg='white', font=label_font)
a13.grid(row=2, column=0, sticky='w', pady=10)
b12 = tk.Entry(login_frame, show='*', textvariable=password, font=entry_font, width=30)
b12.grid(row=2, column=1, pady=10, padx=10)


button_font = font.Font(family='Arial', size=11, weight='bold')

# forgot button
forgot_button = tk.Button(login_frame, text="Forgot Password?", fg='black', bg='white', bd=0, font=button_font, command=forgot)
forgot_button.grid(row=3, column=1, sticky='e', pady=10)

# Login button
login_button = tk.Button(login_frame, text="Login", font=button_font, command=login, width=20, bg='#007bff', fg='white', activebackground="#0056b3")
login_button.grid(row=4, column=1, pady=20)


# Signup Section
signup_label = tk.Label(login_frame, text="Not a member?", bg='white', font=label_font)
signup_label.grid(row=5, column=0, sticky='w', pady=20)

signup_button = tk.Button(login_frame, text="Sign Up", fg='blue', bg='white', bd=0, font=button_font, command=reg)
signup_button.grid(row=5, column=1, sticky='w')

#guest login
login_button1 = tk.Button(login_frame, text="Login as Guest", fg='blue', bg='white', bd=0,  font=button_font, command=main, width=15)
login_button1.grid(row=5, column=1, sticky='e', pady=40)

# Adding hover effects to buttons
def on_hover(button, color_on_hover, color_on_leave):
    button.bind("<Enter>", lambda e: button.config(bg=color_on_hover))
    button.bind("<Leave>", lambda e: button.config(bg=color_on_leave))

on_hover(login_button, '#0056b3', '#007bff')

# Ensure the window remains responsive and updates with the background image
root.pack_propagate(False)
root.update()
# Start the main loop
root.mainloop()
