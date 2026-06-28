import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import database

def admin_dashboard(admin_data):
    root = tk.Tk()
    root.title("Admin Dashboard - Notice Hub")
    root.state('zoomed')
    root.configure(bg="#f0f2f5")

    # Define common styles
    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 10), rowheight=25)
    style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

    # Sidebar
    sidebar = tk.Frame(root, bg="#2c3e50", width=260, highlightbackground="#1a252f", highlightthickness=1)
    sidebar.pack(side="left", fill="y")

    # Sidebar Header
    sb_header = tk.Frame(sidebar, bg="#1a252f", pady=40)
    sb_header.pack(fill="x")
    tk.Label(sb_header, text="NOTICE HUB", font=("Helvetica", 18, "bold"), bg="#1a252f", fg="white").pack()
    tk.Label(sb_header, text="ADMIN PANEL", font=("Arial", 9), bg="#1a252f", fg="#94a3b8").pack()

    current_frame = None

    def logout():
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            root.destroy()
            import login
            login.login_page()
            messagebox.showinfo("Success", "Logged out successfully")

    def show_post_notice_view():
        nonlocal current_frame
        if current_frame: current_frame.destroy()
        
        frame = tk.Frame(content, bg="#f8f9fa")
        frame.pack(fill="both", expand=True)
        current_frame = frame

        tk.Label(frame, text="Post New Announcement", font=("Helvetica", 22, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(anchor="w", pady=(0, 20))

        # Notice Form Container
        form_container = tk.Frame(frame, bg="white", highlightbackground="#ddd", highlightthickness=1)
        form_container.pack(fill="x", pady=10)
        
        form_header = tk.Frame(form_container, bg="#f1f3f5", pady=10)
        form_header.pack(fill="x")
        tk.Label(form_header, text="Create Notice", font=("Arial", 11, "bold"), bg="#f1f3f5", fg="#495057").pack(side="left", padx=15)

        form_body = tk.Frame(form_container, bg="white", padx=20, pady=20)
        form_body.pack(fill="x")

        tk.Label(form_body, text="Title / Subject:", bg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        title_entry = tk.Entry(form_body, font=("Arial", 12), width=60, highlightbackground="#ced4da", highlightthickness=1, bd=0)
        title_entry.grid(row=0, column=1, padx=15, pady=5, sticky="w")

        tk.Label(form_body, text="Notice Category:", bg="white", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        categories = ["Event", "Holiday", "Emergency", "Exam"]
        cat_var = tk.StringVar(value="Event")
        cat_menu = ttk.Combobox(form_body, textvariable=cat_var, values=categories, state="readonly", width=18)
        cat_menu.grid(row=1, column=1, sticky="w", padx=15, pady=5)

        tk.Label(form_body, text="Notice Content:", bg="white", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="nw", pady=5)
        content_text = tk.Text(form_body, font=("Arial", 11), width=60, height=8, highlightbackground="#ced4da", highlightthickness=1, bd=0)
        content_text.grid(row=2, column=1, padx=15, pady=5, sticky="w")

        tk.Label(form_body, text="Attachment:", bg="white", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", pady=5)
        file_path_var = tk.StringVar(value="No file selected")
        file_label = tk.Label(form_body, textvariable=file_path_var, bg="white", font=("Arial", 9), fg="#666")
        file_label.grid(row=3, column=1, sticky="w", padx=15, pady=5)

        def choose_file():
            path = filedialog.askopenfilename(filetypes=[("All Files", "*.*"), ("PDF files", "*.pdf"), ("Audio files", "*.mp3 *.wav"), ("Video files", "*.mp4 *.mkv")])
            if path:
                file_path_var.set(path)

        tk.Button(form_body, text="Choose File", bg="#6c757d", fg="white", font=("Arial", 9), bd=0, command=choose_file, cursor="hand2", padx=10).grid(row=3, column=1, sticky="e", padx=15)

        def add_notice():
            title = title_entry.get().strip()
            msg = content_text.get("1.0", tk.END).strip()
            cat = cat_var.get()
            f_path = file_path_var.get() if file_path_var.get() != "No file selected" else None
            if title and msg:
                database.add_notice(title, msg, cat, admin_data['name'], f_path)
                messagebox.showinfo("Published", "Notice posted successfully!")
                title_entry.delete(0, tk.END)
                content_text.delete("1.0", tk.END)
                file_path_var.set("No file selected")
            else:
                messagebox.showwarning("Incomplete", "Please enter title and content.")

        tk.Button(form_body, text="Publish Notice", bg="#1877f2", fg="white", font=("Arial", 11, "bold"), bd=0, command=add_notice, cursor="hand2", padx=30, pady=10).grid(row=4, column=1, sticky="e", pady=20)

    def show_manage_notices_view():
        nonlocal current_frame
        if current_frame: current_frame.destroy()
        
        frame = tk.Frame(content, bg="#f8f9fa")
        frame.pack(fill="both", expand=True)
        current_frame = frame

        tk.Label(frame, text="Manage Active Notices", font=("Helvetica", 22, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(anchor="w", pady=(0, 20))

        # Notice Table Container
        table_container = tk.Frame(frame, bg="white", highlightbackground="#ddd", highlightthickness=1)
        table_container.pack(fill="both", expand=True, pady=10)
        
        table_header = tk.Frame(table_container, bg="#f1f3f5", pady=10)
        table_header.pack(fill="x")
        tk.Label(table_header, text="Browse and Edit Announcements", font=("Arial", 11, "bold"), bg="#f1f3f5", fg="#495057").pack(side="left", padx=15)

        table_body = tk.Frame(table_container, bg="white", padx=15, pady=15)
        table_body.pack(fill="both", expand=True)

        cols = ("ID", "Title", "Category", "Date")
        tree = ttk.Treeview(table_body, columns=cols, show="headings")
        for col in cols:
            tree.heading(col, text=col.upper())
            tree.column(col, width=100, anchor="center")
        tree.column("Title", width=400, anchor="w")
        tree.pack(fill="both", expand=True, side="left")

        sb = ttk.Scrollbar(table_body, orient="vertical", command=tree.yview)
        tree.configure(yscroll=sb.set)
        sb.pack(side="right", fill="y")

        def refresh_notices():
            for i in tree.get_children(): tree.delete(i)
            for n in database.get_all_notices():
                # Indices: 0(ID), 1(Title), 3(Category), 5(Date)
                tree.insert("", tk.END, values=(n[0], n[1], n[3], n[5]))

        def delete_notice():
            sel = tree.selection()
            if not sel: return
            if messagebox.askyesno("Confirm Deletion", "Permanently delete this notice?"):
                database.delete_notice(tree.item(sel[0])['values'][0])
                refresh_notices()

        def open_update_modal():
            sel = tree.selection()
            if not sel: return
            notice_id = tree.item(sel[0])['values'][0]
            data = database.get_notice_by_id(notice_id)
            
            up_win = tk.Toplevel(root)
            up_win.title("Update Notice")
            up_win.geometry("600x600")
            up_win.configure(bg="white", padx=30, pady=30)
            
            tk.Label(up_win, text="Update Notice Details", font=("Helvetica", 16, "bold"), bg="white", fg="#2c3e50").pack(pady=(0, 20))
            
            tk.Label(up_win, text="Title:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
            t_ent = tk.Entry(up_win, font=("Arial", 12), width=50, highlightbackground="#ddd", highlightthickness=1, bd=0)
            t_ent.insert(0, data[1])
            t_ent.pack(fill="x", pady=(5, 15), ipady=8)
            
            tk.Label(up_win, text="Category:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
            c_var = tk.StringVar(value=data[3])
            c_menu = ttk.Combobox(up_win, textvariable=c_var, values=["Event", "Holiday", "Emergency", "Exam"], state="readonly")
            c_menu.pack(fill="x", pady=(5, 15), ipady=5)
            
            tk.Label(up_win, text="Content:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
            c_txt = tk.Text(up_win, font=("Arial", 11), height=10, highlightbackground="#ddd", highlightthickness=1, bd=0)
            c_txt.insert("1.0", data[2])
            c_txt.pack(fill="both", expand=True, pady=(5, 20))
            
            def save():
                if t_ent.get() and c_txt.get("1.0", tk.END).strip():
                    database.update_notice(notice_id, t_ent.get(), c_txt.get("1.0", tk.END).strip(), c_var.get())
                    messagebox.showinfo("Success", "Notice updated successfully!")
                    up_win.destroy()
                    refresh_notices()
                else:
                    messagebox.showwarning("Error", "Fields cannot be empty")
            
            tk.Button(up_win, text="Save Changes", bg="#28a745", fg="white", font=("Arial", 11, "bold"), bd=0, command=save, pady=10).pack(fill="x")

        def view_tracking():
            sel = tree.selection()
            if not sel: return
            notice_id = tree.item(sel[0])['values'][0]
            title = tree.item(sel[0])['values'][1]
            
            track_win = tk.Toplevel(root)
            track_win.title(f"Views: {title}")
            track_win.geometry("500x500")
            track_win.configure(bg="white", padx=30, pady=30)
            
            tk.Label(track_win, text="Read Receipts", font=("Helvetica", 16, "bold"), bg="white").pack(pady=(0, 20))
            
            views = database.get_views_for_notice(notice_id)
            if not views:
                tk.Label(track_win, text="No views recorded yet.", bg="white").pack(pady=20)
            else:
                v_cols = ("Viewer", "Timestamp")
                v_tree = ttk.Treeview(track_win, columns=v_cols, show="headings")
                v_tree.heading("Viewer", text="VIEWER")
                v_tree.heading("Timestamp", text="TIME")
                v_tree.pack(fill="both", expand=True)
                for v in views: v_tree.insert("", tk.END, values=v)

        btn_box = tk.Frame(frame, bg="#f8f9fa", pady=10)
        btn_box.pack(fill="x")
        
        tk.Button(btn_box, text="Delete Notice", bg="#dc3545", fg="white", font=("Arial", 10, "bold"), command=delete_notice, padx=20, pady=8, bd=0).pack(side="right", padx=5)
        tk.Button(btn_box, text="Update Notice", bg="#ffc107", fg="black", font=("Arial", 10, "bold"), command=open_update_modal, padx=20, pady=8, bd=0).pack(side="right", padx=5)
        tk.Button(btn_box, text="View Tracking", bg="#17a2b8", fg="white", font=("Arial", 10, "bold"), command=view_tracking, padx=20, pady=8, bd=0).pack(side="right", padx=5)

        refresh_notices()

    def show_feedback_view():
        nonlocal current_frame
        if current_frame: current_frame.destroy()
        
        frame = tk.Frame(content, bg="#f8f9fa")
        frame.pack(fill="both", expand=True)
        current_frame = frame

        tk.Label(frame, text="User Feedback", font=("Helvetica", 22, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(anchor="w", pady=(0, 20))
        
        list_container = tk.Frame(frame, bg="white", highlightbackground="#ddd", highlightthickness=1)
        list_container.pack(fill="both", expand=True)

        table_header = tk.Frame(list_container, bg="#f1f3f5", pady=10)
        table_header.pack(fill="x")
        tk.Label(table_header, text="Messages from Users", font=("Arial", 11, "bold"), bg="#f1f3f5", fg="#495057").pack(side="left", padx=15)

        table_body = tk.Frame(list_container, bg="white", padx=15, pady=15)
        table_body.pack(fill="both", expand=True)

        cols = ("Name", "Role", "Message", "Date")
        f_tree = ttk.Treeview(table_body, columns=cols, show="headings")
        for col in cols:
            f_tree.heading(col, text=col)
            f_tree.column(col, anchor="center", width=120)
        f_tree.heading("Message", text="Feedback Content")
        f_tree.column("Message", width=450, anchor="w")
        f_tree.pack(fill="both", expand=True)

        for f in database.get_all_feedback():
            f_tree.insert("", tk.END, values=(f[1], f[2], f[3], f[4]))

    # Sidebar Buttons with better styling
    def create_nav_btn(text, cmd):
        return tk.Button(sidebar, text=text, bg="#2c3e50", fg="#bdc3c7", activebackground="#34495e", activeforeground="white", bd=0, font=("Arial", 11, "bold"), pady=15, anchor="w", padx=30, cursor="hand2", command=cmd)

    create_nav_btn("Post Notice", show_post_notice_view).pack(fill="x")
    create_nav_btn("Manage Notices", show_manage_notices_view).pack(fill="x")
    create_nav_btn("View Feedback", show_feedback_view).pack(fill="x")
    
    tk.Button(sidebar, text="LOG OUT", bg="#e74c3c", fg="white", activebackground="#c0392b", activeforeground="white", font=("Arial", 11, "bold"), pady=15, bd=0, command=logout, cursor="hand2").pack(side="bottom", fill="x")

    # Overall Content Area
    content = tk.Frame(root, bg="#f8f9fa", padx=30, pady=30)
    content.pack(side="left", fill="both", expand=True)

    header = tk.Frame(content, bg="#f0f2f5")
    header.pack(fill="x", pady=(0, 25))
    tk.Label(header, text="Admin Dashboard", font=("Helvetica", 22, "bold"), bg="#f0f2f5", fg="#1e293b").pack(side="left")
    
    profile_info = tk.Frame(header, bg="white", highlightbackground="#ddd", highlightthickness=1, padx=15, pady=5)
    profile_info.pack(side="right")
    tk.Label(profile_info, text=f"Admin: {admin_data['name']}", font=("Arial", 10, "bold"), bg="white", fg="#7f8c8d").pack(side="left")

    show_post_notice_view() 
    root.mainloop()

if __name__ == "__main__":
    admin_dashboard({"id": 1, "role": "Admin", "name": "Main Admin", "email": "admin@test.com"})
