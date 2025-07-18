import tkinter as tk
from PIL import Image, ImageTk

# Root window setup
root = tk.Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()  # Get screen width and height
root.geometry("%dx%d+0+0" % (w, h))
root.title("Image Forgery Detection")

# Load and resize images to fit the screen
img1 = ImageTk.PhotoImage(Image.open("bg images/image5.jpg").resize((w, h), Image.LANCZOS))   # Resize background image
img2 = ImageTk.PhotoImage(Image.open("bg images/image6.png").resize((w, h), Image.LANCZOS))  # Resize for consistency
img3 = ImageTk.PhotoImage(Image.open("bg images/image2.png").resize((w, h), Image.LANCZOS)) # Resize for consistency


# Canvas to hold the rotating background images
canvas = tk.Canvas(root, width=w, height=h)
canvas.place(x=0, y=0, relwidth=1, relheight=1)  # Cover the entire window

# Initial image on the canvas
canvas_image = canvas.create_image(0, 0, anchor=tk.NW, image=img1)

# Image rotation function
x = 1
def rotate_images():
    global x
    if x == 1:
        canvas.itemconfig(canvas_image, image=img1)
    elif x == 2:
        canvas.itemconfig(canvas_image, image=img2)
    elif x == 3:
        canvas.itemconfig(canvas_image, image=img3)

    x += 1
    if x > 3:
        x = 1
    root.after(2000, rotate_images)  # Rotate every 2 seconds

# Start rotating the images
rotate_images()

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


# Button styles with hover effects
def on_enter(e):
    e.widget['background'] = '#5DADE2'  # Lighter shade of the button when hovered
    e.widget['foreground'] = 'white'

def on_leave(e):
    e.widget['background'] = '#1F618D'  # Revert back to the original color
    e.widget['foreground'] = 'white'

button_style = {
    'font': ('Arial', 20, 'bold'),
    'bg': '#1F618D',  # Original button color
    'fg': 'white',
    'activebackground': '#2874A6',
    'activeforeground': '#ECF0F1',
    'relief': tk.RAISED,
    'bd': 8,
    'width': 12
}

# Function to call login.py
def login():
    from subprocess import call
    call(['python', 'login.py'])

# Function to call registration.py
def register():
    from subprocess import call
    call(['python', 'registration.py'])

# Creating Login Button with hover effect
btn_login = tk.Button(root, text="Login", command=login, **button_style)
btn_login.place(relx=0.20, rely=0.8, anchor=tk.CENTER)
btn_login.bind("<Enter>", on_enter)
btn_login.bind("<Leave>", on_leave)

# Creating Register Button with hover effect
btn_register = tk.Button(root, text="Register", command=register, **button_style)
btn_register.place(relx=0.80, rely=0.8, anchor=tk.CENTER)
btn_register.bind("<Enter>", on_enter)
btn_register.bind("<Leave>", on_leave)

# Footer Label for description
footer_label = tk.Label(root, text="Secure your images with our advanced forgery detection system",
                        font=("Arial", 18, "italic"), bg="#34495E", fg="white")
footer_label.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

# Ensure the window remains responsive and updates with the background image
root.pack_propagate(False)
root.update()
# Start the main loop
root.mainloop()
