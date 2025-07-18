import tkinter as tk
from tkinter import messagebox as ms
from PIL import Image, ImageTk
import sqlite3

# Initialize the root window
root = tk.Tk()
root.configure(background='white')
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Forget Password")

# Load background image
bg_image = Image.open('bg images/b3.jpg')
bg_image = bg_image.resize((w, h), Image.LANCZOS)
bg_image_tk = ImageTk.PhotoImage(bg_image)

# Set the background
background_label = tk.Label(root, image=bg_image_tk)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Variables to hold email, password, and confirmation password
email = tk.StringVar()
password = tk.StringVar()
confirmPassword = tk.StringVar()

# Connect to the database and ensure the table exists
db = sqlite3.connect('knee.db')
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS KneeReg (name TEXT,  Email TEXT,  Phoneno TEXT,  password TEXT)")
db.commit()

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


# Create a frame to hold the form and make it semi-transparent
frame = tk.Frame(root, bg="white", padx=40, pady=40, relief=tk.GROOVE, bd=2)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


# Title Label
title_label = tk.Label(frame, text="Reset Your Password", font=("Helvetica", 24, "bold"), bg="white", fg="black")
title_label.grid(row=0, column=0, columnspan=2, pady=20)

# Labels and entry fields for email, password, and confirm password
tk.Label(frame, text='Email', font=('Cambria', 14), bg="white", fg="#333333").grid(row=1, column=0, pady=10, padx=10, sticky='w')
tk.Entry(frame, width=40, textvariable=email, font=("Arial", 12)).grid(row=1, column=1, pady=10, padx=10)

tk.Label(frame, text='New Password', font=('Cambria', 14), bg="white", fg="#333333").grid(row=2, column=0, pady=10, padx=10, sticky='w')
tk.Entry(frame, width=40, textvariable=password, show="*", font=("Arial", 12)).grid(row=2, column=1, pady=10, padx=10)

tk.Label(frame, text='Confirm Password', font=('Cambria', 14), bg="white", fg="#333333").grid(row=3, column=0, pady=10, padx=10, sticky='w')
tk.Entry(frame, width=40, textvariable=confirmPassword, show="*", font=("Arial", 12)).grid(row=3, column=1, pady=10, padx=10)

# Function to change the password
def change_password():
    new_password = password.get().strip()
    confirm_password = confirmPassword.get().strip()

    if not email.get().strip():
        ms.showerror('Error!', "Please enter your email")
        return

    if not new_password or not confirm_password:
        ms.showerror('Error!', "Please fill in both password fields.")
        return

    with sqlite3.connect('knee.db') as db:
        c = db.cursor()

    # Check if the email exists
    find_user = 'SELECT * FROM KneeReg WHERE Email = ?'
    c.execute(find_user, [(email.get())])
    result = c.fetchone()

    if result:
        if new_password == confirm_password:
            # Update the password in the database
            db = sqlite3.connect("knee.db")
            c = db.cursor()
            c.execute("UPDATE KneeReg SET password = ? WHERE Email = ?", (new_password, email.get()))
            db.commit()
            db.close()
            ms.showinfo('Success', 'Password changed successfully')
            root.destroy()  
        else:
            ms.showerror('Error!', "Passwords didn't match")
    else:
        ms.showerror('Error!', "No account found with this email")

# Submit button with hover effect
def on_enter(e):
    submit_btn.config(bg="#0056b3", fg="white")

def on_leave(e):
    submit_btn.config(bg="#007bff", fg="white")

submit_btn = tk.Button(frame, text="Submit", width=20, command=change_password, font=("Arial", 14), bg="#007bff", fg="white", bd=0)
submit_btn.grid(row=4, columnspan=2, pady=20)

# Add hover effects to the button
submit_btn.bind("<Enter>", on_enter)
submit_btn.bind("<Leave>", on_leave)

# Ensure the window remains responsive and updates with the background image
root.pack_propagate(False)
root.update()
# Start the main loop
root.mainloop()
