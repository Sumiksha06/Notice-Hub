import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import database
import validation

def signup_page():
    root = tk.Tk()
    root.title("Notice Hub - Create Account")
    root.state('zoomed')
    root.configure(bg="#f0f2f5")

    # Split Layout Container
    main_container = tk.Frame(root, bg="white")
    main_container.place(relx=0.5, rely=0.5, anchor="center", width=1000, height=650)

    # --- LEFT SIDE: Background Image ---
    left_frame = tk.Canvas(main_container, bg="#181818", bd=0, highlightthickness=0)
    left_frame.place(relx=0, rely=0, relwidth=0.45, relheight=1)

    try:
        bg_img = Image.open("background.jpg")
        bg_img = bg_img.resize((450, 750), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_img)
        left_frame.create_image(0, 0, image=bg_photo, anchor="nw")
        left_frame.image = bg_photo
        left_frame.create_rectangle(0, 0, 450, 750, fill="black", stipple="gray50")
    except Exception as e:
        print(f"Error loading background: {e}")
        left_frame.configure(bg="#1c1c1c")

    left_frame.create_text(225, 300, text="Create your\nAccount", font=("Helvetica", 32, "bold"), fill="white", width=400, justify="center")
    left_frame.create_text(225, 400, text="Join our community to stay updated with the latest notices.", font=("Helvetica", 12), fill="#cccccc", width=350, justify="center")

    # --- RIGHT SIDE: Sign Up Form (with Border) ---
    form_container = tk.Frame(main_container, bg="white", highlightthickness=2, highlightbackground="#101828", padx=40, pady=30)
    form_container.place(relx=0.45, rely=0.5, relwidth=0.55, anchor="w", height=750)

    tk.Label(form_container, text="Sign Up", font=("Helvetica", 24, "bold"), bg="white", fg="#181818").pack(pady=(20, 10))

    # Role Selection
    role_frame = tk.Frame(form_container, bg="white")
    role_frame.pack(fill="x", pady=5)
    tk.Label(role_frame, text="Select Role:", font=("Helvetica", 10, "bold"), bg="white", fg="#555555").pack(side="left", padx=5)
    role_var = tk.StringVar(value="User")
    tk.Radiobutton(role_frame, text="User", variable=role_var, value="User", bg="white", font=("Helvetica", 10)).pack(side="left", padx=10)
    tk.Radiobutton(role_frame, text="Admin", variable=role_var, value="Admin", bg="white", font=("Helvetica", 10)).pack(side="left")

    def create_modern_input(parent, label_text, placeholder, is_password=False):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="x", pady=5)
        tk.Label(frame, text=label_text, font=("Helvetica", 10, "bold"), bg="white", fg="#555555").pack(anchor="w", padx=5)
        
        canvas = tk.Canvas(frame, height=45, bg="white", bd=0, highlightthickness=0)
        canvas.pack(fill="x", pady=5)
        
        def draw_rounded_rect(event=None):
            canvas.delete("bg")
            w = canvas.winfo_width()
            h = canvas.winfo_height()
            r = 8
            canvas.create_arc((0, 0, 2*r, 2*r), start=90, extent=90, fill="#f5f5f5", outline="#dddddd", tags="bg")
            canvas.create_arc((w-2*r, 0, w, 2*r), start=0, extent=90, fill="#f5f5f5", outline="#dddddd", tags="bg")
            canvas.create_arc((0, h-2*r, 2*r, h), start=180, extent=90, fill="#f5f5f5", outline="#dddddd", tags="bg")
            canvas.create_arc((w-2*r, h-2*r, w, h), start=270, extent=90, fill="#f5f5f5", outline="#dddddd", tags="bg")
            canvas.create_rectangle((r, 0, w-r, h), fill="#f5f5f5", outline="#f5f5f5", tags="bg")
            canvas.create_rectangle((0, r, w, h-r), fill="#f5f5f5", outline="#f5f5f5", tags="bg")
            canvas.create_line(r, 0, w-r, 0, fill="#dddddd", tags="bg")
            canvas.create_line(r, h, w-r, h, fill="#dddddd", tags="bg")
            canvas.create_line(0, r, 0, h-r, fill="#dddddd", tags="bg")
            canvas.create_line(w, r, w, h-r, fill="#dddddd", tags="bg")
        
        canvas.bind("<Configure>", draw_rounded_rect)
        
        entry = tk.Entry(canvas, font=("Helvetica", 11), bg="#f5f5f5", bd=0, highlightthickness=0, fg="#667085")
        entry.insert(0, placeholder)
        
        def toggle_password():
            if entry.cget("show") == "" and entry.get() != placeholder:
                entry.config(show="*")
                toggle_btn.config(text="Show")
            elif entry.get() != placeholder:
                entry.config(show="")
                toggle_btn.config(text="Hide")

        if is_password:
            toggle_btn = tk.Button(canvas, text="Show", font=("Helvetica", 8, "bold"), bg="#f5f5f5", fg="#101828", bd=0, cursor="hand2", command=toggle_password, activebackground="#f5f5f5")
            canvas.create_window(canvas.winfo_width()-10 if canvas.winfo_width()>1 else 400, 22, window=toggle_btn, anchor="e", tags="toggle")
            
            def update_toggle_pos(event):
                canvas.coords("toggle", event.width - 10, 22)
            canvas.bind("<Configure>", lambda e: [draw_rounded_rect(e), update_toggle_pos(e)], add="+")

        def on_focus_in(e):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg="#101828")
                if is_password: 
                    entry.config(show="*")
                    toggle_btn.config(text="Show")
        def on_focus_out(e):
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.config(fg="#667085")
                if is_password: 
                    entry.config(show="")
                    toggle_btn.config(text="Show")
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        
        canvas.create_window(10, 22, window=entry, anchor="w", width=360 if is_password else 400)
        return entry

    fname_entry = create_modern_input(form_container, "First Name", "First Name")
    lname_entry = create_modern_input(form_container, "Last Name", "Last Name")
    email_entry = create_modern_input(form_container, "Email", "Enter your email")
    pass_entry = create_modern_input(form_container, "Password", "Password", True)


    def handle_signup():
        role = role_var.get()
        fname = fname_entry.get().strip()
        lname = lname_entry.get().strip()
        email = email_entry.get().strip()
        password = pass_entry.get().strip()

        if not all([fname, lname, email, password]) or fname == "First Name" or lname == "Last Name" or email == "Enter your email" or password == "Password":
            messagebox.showerror("Error", "All fields are required!")
            return

        is_valid_email, email_msg = validation.validate_email(email)
        if not is_valid_email:
            messagebox.showerror("Invalid Email", email_msg)
            return

        success, msg = database.add_user(role, fname, lname, email, password)
        if success:
            messagebox.showinfo("Success", msg)
            root.destroy()
            import login
            login.login_page()
        else:
            messagebox.showerror("Error", msg)

    signup_btn = tk.Button(form_container, text="Sign Up", font=("Helvetica", 12, "bold"), bg="#181818", fg="white", bd=0, cursor="hand2", command=handle_signup, activebackground="#333333", activeforeground="white")
    signup_btn.pack(fill="x", ipady=12, pady=(10, 15))

    tk.Frame(form_container, bg="#eeeeee", height=1).pack(fill="x", pady=15)
    footer_frame = tk.Frame(form_container, bg="white")
    footer_frame.pack()
    tk.Label(footer_frame, text="Already have an account? ", bg="white", font=("Helvetica", 10), fg="#555555").pack(side="left")
    
    def go_to_login():
        root.destroy()
        import login
        login.login_page()

    login_link = tk.Button(footer_frame, text="Log In", font=("Helvetica", 10, "bold"), fg="#181818", bg="white", bd=0, cursor="hand2", command=go_to_login)
    login_link.pack(side="left")

    root.mainloop()

if __name__ == "__main__":
    signup_page()