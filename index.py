import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import login
import signup
import os

def index_page():
    root = tk.Tk()
    root.title("Notice Hub - Home")
    root.state('zoomed')
    root.configure(bg="#f8f9fa")

    root.images = {}

    def load_image(path, size=None):
        try:
            img = Image.open(path)
            if size:
                img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            return None

    # Navbar
    navbar = tk.Frame(root, bg="white", height=80, highlightbackground="#e0e0e0", highlightthickness=1)
    navbar.pack(fill="x", side="top")
    navbar.pack_propagate(False)

    # Logo in Navbar
    logo_img = load_image("logo.jpg", (300, 250))
    if logo_img:
        root.images['logo'] = logo_img
        logo_icon = tk.Label(navbar, image=logo_img, bg="white")
        logo_icon.pack(side="left", padx=(10))

    btn_frame = tk.Frame(navbar, bg="white")
    btn_frame.pack(side="right", padx=60)

    def open_login():
        root.destroy()
        login.login_page()

    def open_signup():
        root.destroy()
        signup.signup_page()

    tk.Button(btn_frame, text="Log In", font=("Arial", 11, "bold"), fg="#1877f2", bg="white", bd=0, cursor="hand2", command=open_login, activebackground="#f0f2f5").pack(side="left", padx=20)
    
    # Join Now Button
    join_btn = tk.Button(btn_frame, text="Join Now", font=("Arial", 11, "bold"), fg="white", bg="#1877f2", 
                         padx=25, pady=8, bd=0, cursor="hand2", command=open_signup, activebackground="#145dbf")
    join_btn.pack(side="left")

    # Hero Section
    hero = tk.Frame(root, bg="#1877f2", pady=40)
    hero.pack(fill="x")
    
    hero_content = tk.Frame(hero, bg="#1877f2")
    hero_content.pack()
    
    tk.Label(hero_content, text="Stay Informed. Stay Connected.", font=("Helvetica", 42, "bold"), fg="white", bg="#1877f2").pack()
    tk.Label(hero_content, text="The centralized digital platform for all your organizational announcements.", 
             font=("Arial", 16), fg="#e0e0e0", bg="#1877f2", pady=20).pack()
    
    get_started_btn = tk.Button(hero_content, text="Get Started", font=("Arial", 13, "bold"), bg="white", fg="#1877f2", 
                               padx=40, pady=12, bd=0, cursor="hand2", command=open_signup, activebackground="#f8f9fa")
    get_started_btn.pack(pady=10)

    # Features Section
    features_container = tk.Frame(root, bg="#f8f9fa", pady=60)
    features_container.pack(fill="x")

    def add_feature(title, desc, color):
        f = tk.Frame(features_container, bg="white", padx=10, pady=10, width=250, height=130, highlightbackground="#e0e0e0", highlightthickness=1)
        f.pack(side="left", expand=True, padx=20)
        f.pack_propagate(False)
        
        # Color bar at top for style
        tk.Frame(f, bg=color, height=10).pack(fill="x", pady=(0, 20))
        
        tk.Label(f, text=title, font=("Helvetica", 10, "bold"), fg="#1c1e21", bg="white").pack(pady=(0, 15))
        tk.Label(f, text=desc, font=("Arial", 8), fg="#000000", bg="white",wraplength=200, justify="center").pack()

    add_feature("Smart Admin", "Effortlessly broadcast tagged announcements and track read receipts in real-time.", "#1877f2")
    add_feature("Instant Alerts", "Never miss an update. Categorized views help you find what matters most.", "#6c5ce7")
    add_feature("Feedback Loop", "Two-way communication channels ensure every voice in the organization is heard.", "#00b894")

    # Footer
    footer = tk.Frame(root, bg="white", height=60, highlightbackground="#e0e0e0", highlightthickness=1)
    footer.pack(fill="x", side="bottom")
    tk.Label(footer, text="© 2026 Notice Hub. Empowering communication.", font=("Arial", 9), bg="white", fg="#8d949e").pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    index_page()