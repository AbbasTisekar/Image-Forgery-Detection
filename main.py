import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from ela import convert_to_ela_image
from prediction import predict_result

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Image Forgery Detection")
        self.geometry("1600x900")
        self.resizable(True, True)
        self.configure(bg="#2c3e50")

        # Title background frame (to keep both logo and text in one line)
        self.title_frame = tk.Frame(self, bg="lightgray", width=1600, height=60)
        self.title_frame.place(x=0, y=0)
        
        # Logo inside title bar
        logo_img = Image.open("bg images/logo.webp").resize((100, 55), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_img)
        self.logo_label = tk.Label(self.title_frame, image=self.logo_photo, bg='lightgray')
        self.logo_label.place(x=0, y=0)
        
        # Title text label next to logo
        self.title_label = tk.Label(self.title_frame, text="Image Forgery Detection", font=("Times New Roman", 35, "bold"),
                                    fg="black", bg="lightgray")
        self.title_label.place(x=450, y=0)


       # ===== Original Image Section =====
        self.original_image_label = tk.Label(self, text="Original Image", font=("Arial", 16, "bold"),
                                             fg="white", bg="#2c3e50")
        self.original_image_label.place(x=200, y=80)
        
        self.original_image_canvas = tk.Label(self, bg="#34495e", width=300, height=200)
        self.original_image_canvas.place(x=200, y=120, width=300, height=200)
        
        # ===== ELA Image Section =====
        self.ela_image_label = tk.Label(self, text="ELA Image", font=("Arial", 16, "bold"),
                                        fg="white", bg="#2c3e50")
        self.ela_image_label.place(x=200, y=420)
        
        self.ela_image_canvas = tk.Label(self, bg="#34495e", width=300, height=200)
        self.ela_image_canvas.place(x=200, y=460, width=300, height=200)
        
        # ===== Browse Button =====
        self.browse_button = tk.Button(self, text="Browse Image", command=self.open_image,
                                       font=("Arial", 16), bg="#2980b9", fg="white", relief="flat", bd=2)
        self.browse_button.place(x=250, y=350, width=200, height=40)

        # ===== Prediction Result Label =====
        self.result_label = tk.Label(self, text="Prediction Result", font=("Arial", 22, "bold"),
                                     fg="white", bg="#2c3e50")
        self.result_label.place(x=850, y=300)

        self.result_text = tk.Label(self, text="Prediction: None\nConfidence: 0%",
                                    font=("Arial", 20, "bold"), fg="#2ecc71", bg="#2c3e50")
        self.result_text.place(x=850, y=400)

        # ===== Test Button =====
        self.test_button = tk.Button(self, text="Test", command=self.display_result,
                                     font=("Arial", 20), bg="#3498db", fg="white", relief="flat", bd=2)
        self.test_button.place(x=800, y=500, width=200, height=50)

        # ===== Quit Button =====
        self.quit_button = tk.Button(self, text="Quit", command=self.close_main_window,
                                     font=("Arial", 20), bg="#e74c3c", fg="white", relief="flat", bd=2)
        self.quit_button.place(x=1050, y=500, width=200, height=50)

    def open_image(self):
        fname = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp;*.avif")])

        if fname:
            self.fname = fname
            print(f"Selected image path: {self.fname}")  # Debug

            # Display Original Image
            original_img = Image.open(fname).resize((384, 256))
            original_img = ImageTk.PhotoImage(original_img)
            self.original_image_canvas.configure(image=original_img)
            self.original_image_canvas.image = original_img

            # Generate and display ELA image
            convert_to_ela_image(fname, 90)
            ela_img = Image.open("ela_image.png").resize((384, 256))
            ela_img = ImageTk.PhotoImage(ela_img)
            self.ela_image_canvas.configure(image=ela_img)
            self.ela_image_canvas.image = ela_img

    def display_result(self):
        if hasattr(self, 'fname'):
            prediction, confidence = predict_result(self.fname)
            self.result_text.configure(text=f"Prediction: {prediction}\nConfidence: {confidence}%")
        else:
            messagebox.showerror("Error", "No image selected. Please browse an image first.")

    def close_main_window(self):
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.quit()

def main():
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
