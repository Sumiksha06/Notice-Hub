import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import database
import validation

def login_page():
    root = tk.Tk()
    root.title("Notice Hub - Login")
    root.state('zoomed')
    root.configure(bg="#f0f2f5")

    # Main Center Panel with Border
    # We use a container frame to hold the form and provide a border
    main_container = tk.Frame(root, bg="white", highlightthickness=2, highlightbackground="#101828", padx=60, pady=40)
    main_container.place(relx=0.5, rely=0.5, anchor="center", width=550, height=650)
    
    # Header section
    tk.Label(main_container, text="Welcome Back!", font=("Helvetica", 32, "bold"), bg="white", fg="#101828").pack(anchor="w", pady=(20, 5))
    tk.Label(main_container, text="Please enter your details.", font=("Helvetica", 12), bg="white", fg="#475467").pack(anchor="w", pady=(0, 40))

    def create_modern_input(parent, label_text, placeholder, is_password=False):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="x", pady=10)
        
        tk.Label(frame, text=label_text, font=("Helvetica", 11, "bold"), bg="white", fg="#344054").pack(anchor="w", pady=(0, 8))
        
        canvas = tk.Canvas(frame, height=50, bg="white", bd=0, highlightthickness=0)
        canvas.pack(fill="x")
        
        def draw_rounded_rect(event=None):
            canvas.delete("bg")
            w = canvas.winfo_width()
            h = canvas.winfo_height()
            r = 10
            canvas.create_arc((0, 0, 2*r, 2*r), start=90, extent=90, fill="white", outline="#d0d5dd", tags="bg")
            canvas.create_arc((w-2*r, 0, w, 2*r), start=0, extent=90, fill="white", outline="#d0d5dd", tags="bg")
            canvas.create_arc((0, h-2*r, 2*r, h), start=180, extent=90, fill="white", outline="#d0d5dd", tags="bg")
            canvas.create_arc((w-2*r, h-2*r, w, h), start=270, extent=90, fill="white", outline="#d0d5dd", tags="bg")
            canvas.create_rectangle((r, 0, w-r, h), fill="white", outline="white", tags="bg")
            canvas.create_rectangle((0, r, w, h-r), fill="white", outline="white", tags="bg")
            canvas.create_line(r, 0, w-r, 0, fill="#d0d5dd", tags="bg")
            canvas.create_line(r, h, w-r, h, fill="#d0d5dd", tags="bg")
            canvas.create_line(0, r, 0, h-r, fill="#d0d5dd", tags="bg")
            canvas.create_line(w, r, w, h-r, fill="#d0d5dd", tags="bg")
        
        canvas.bind("<Configure>", draw_rounded_rect)
        
        entry = tk.Entry(canvas, font=("Helvetica", 12), bg="white", bd=0, highlightthickness=0, fg="#667085")
        entry.insert(0, placeholder)
        
        def toggle_password():
            if entry.cget("show") == "" and entry.get() != placeholder:
                entry.config(show="*")
                toggle_btn.config(text="Show")
            elif entry.get() != placeholder:
                entry.config(show="")
                toggle_btn.config(text="Hide")

        if is_password:
            toggle_btn = tk.Button(canvas, text="Show", font=("Helvetica", 9, "bold"), bg="white", fg="#101828", bd=0, cursor="hand2", command=toggle_password, activebackground="white")
            canvas.create_window(canvas.winfo_width()-10 if canvas.winfo_width()>1 else 400, 25, window=toggle_btn, anchor="e", tags="toggle")
            
            def update_toggle_pos(event):
                canvas.coords("toggle", event.width - 10, 25)
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
        
        canvas.create_window(15, 25, window=entry, anchor="w", width=340 if is_password else 380)
        return entry

    email_entry = create_modern_input(main_container, "Email", "Enter your email")
    pass_entry = create_modern_input(main_container, "Password", "Password", True)


    def handle_login():
        email = email_entry.get().strip()
        password = pass_entry.get().strip()

        if email == "Enter your email" or password == "Password":
            messagebox.showwarning("Incomplete", "Please enter your email and password.")
            return

        is_valid_email, email_msg = validation.validate_email(email)
        if not is_valid_email:
            messagebox.showerror("Invalid Email", email_msg)
            return

        user = database.login_user(email, password)
        if user:
            role = user[1]
            fname = user[2]
            user_data = {"id": user[0], "role": role, "name": f"{fname} {user[3]}", "email": user[4]}
            messagebox.showinfo("Success", f"Welcome back, {fname}!")
            root.destroy()
            if role == "Admin":
                import admin_dashboard
                admin_dashboard.admin_dashboard(user_data)
            else:
                import user_dashboard
                user_dashboard.user_dashboard(user_data)
        else:
            messagebox.showerror("Error", "Invalid email or password.")

    # Login Button
    login_btn = tk.Button(main_container, text="Login", font=("Helvetica", 12, "bold"), bg="#101828", fg="white", bd=0, cursor="hand2", command=handle_login, activebackground="#1d2939", activeforeground="white")
    login_btn.pack(fill="x", ipady=14, pady=(15, 15))

    # Footer
    footer_frame = tk.Frame(main_container, bg="white")
    footer_frame.pack(pady=(40, 20))
    tk.Label(footer_frame, text="Don't have an account?", font=("Helvetica", 11), bg="white", fg="#475467").pack(side="left")
    
    def go_to_signup():
        root.destroy()
        import signup
        signup.signup_page()

    signup_link = tk.Button(footer_frame, text="Sign up!", font=("Helvetica", 11, "bold"), fg="#101828", bg="white", bd=0, cursor="hand2", command=go_to_signup)
    signup_link.pack(side="left", padx=5)

    root.mainloop()

if __name__ == "__main__":
    login_page()