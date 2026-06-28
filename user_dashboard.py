import tkinter as tk
from tkinter import ttk, messagebox
import database
import os
import shutil
from tkinter import filedialog

def user_dashboard(user_data):
    root = tk.Tk()
    root.title("User Dashboard - Notice Hub")
    root.state('zoomed')
    root.configure(bg="#f4f7f6")

    # Header
    header = tk.Frame(root, bg="#1877f2", pady=15, highlightbackground="#145dbf", highlightthickness=1)
    header.pack(fill="x")
    
    tk.Label(header, text="NOTICE HUB", font=("Helvetica", 20, "bold"), bg="#1877f2", fg="white", padx=30).pack(side="left")
    
    def logout():
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            root.destroy()
            import login
            login.login_page()
            messagebox.showinfo("Success", "Logged out successfully")
    
    tk.Button(header, text="Log Out", bg="#dc3545", fg="white", font=("Arial", 10, "bold"), bd=0, padx=20, pady=7, command=logout, cursor="hand2").pack(side="right", padx=30)

    # Content Area
    content = tk.Frame(root, bg="#f4f7f6", padx=50, pady=30)
    content.pack(fill="both", expand=True)

    # User Profile Info Bar
    top_bar = tk.Frame(content, bg="#f4f7f6")
    top_bar.pack(fill="x", pady=(0, 25))

    profile_card = tk.Frame(top_bar, bg="white", padx=25, pady=20, highlightbackground="#d1d9e6", highlightthickness=1)
    profile_card.pack(side="left", fill="x", expand=True)
    
    tk.Label(profile_card, text=f"Welcome back, {user_data['name']}", font=("Helvetica", 16, "bold"), bg="white", fg="#2c3e50").pack(side="left")
    tk.Label(profile_card, text=f" |  {user_data['email']}", font=("Arial", 11), bg="white", fg="#7f8c8d").pack(side="left")

    def open_feedback():
        fb_win = tk.Toplevel(root)
        fb_win.title("Send Feedback")
        fb_win.geometry("450x400")
        fb_win.configure(bg="white", padx=30, pady=30)

        tk.Label(fb_win, text="We value your feedback!", font=("Helvetica", 16, "bold"), bg="white", fg="#1877f2").pack(pady=(0, 5))
        tk.Label(fb_win, text="Let us know if you have any suggestions or issues.", font=("Arial", 9), bg="white", fg="#7f8c8d", wraplength=350).pack(pady=(0, 20))
        
        msg_frame = tk.Frame(fb_win, bg="#ddd", padx=1, pady=1)
        msg_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        msg_text = tk.Text(msg_frame, font=("Arial", 11), bg="#f9f9f9", bd=0, highlightthickness=0)
        msg_text.pack(fill="both", expand=True)

        def submit_fb():
            msg = msg_text.get("1.0", tk.END).strip()
            if msg:
                database.add_feedback(user_data['name'], "User", msg)
                messagebox.showinfo("Success", "Thank you! Your feedback has been submitted.")
                fb_win.destroy()
            else:
                messagebox.showwarning("Warning", "Please enter a message before submitting.")

        tk.Button(fb_win, text="Send Feedback", bg="#1877f2", fg="white", font=("Arial", 11, "bold"), bd=0, command=submit_fb, pady=10, cursor="hand2").pack(fill="x")

    tk.Button(top_bar, text="Send Feedback", bg="#6c757d", fg="white", font=("Arial", 11, "bold"), bd=0, command=open_feedback, padx=25, cursor="hand2").pack(side="right", fill="y", padx=(20, 0))

    # Control Panel (Filtering)
    controls = tk.Frame(content, bg="white", padx=20, pady=15, highlightbackground="#d1d9e6", highlightthickness=1)
    controls.pack(fill="x", pady=(0, 20))
    
    tk.Label(controls, text="View Notices by Category:", font=("Arial", 10, "bold"), bg="white", fg="#333").pack(side="left", padx=(0, 15))
    
    categories = ["All Notices", "Event", "Holiday", "Emergency", "Exam"]
    filter_var = tk.StringVar(value="All Notices")
    
    def on_filter_change(event=None):
        refresh_user_notices(filter_var.get())

    filter_menu = ttk.Combobox(controls, textvariable=filter_var, values=categories, state="readonly", width=25)
    filter_menu.pack(side="left")
    filter_menu.bind("<<ComboboxSelected>>", on_filter_change)

    # Notice Table Container
    list_container = tk.Frame(content, bg="white", highlightbackground="#d1d9e6", highlightthickness=1)
    list_container.pack(fill="both", expand=True)
    
    list_header = tk.Frame(list_container, bg="#f1f3f5", pady=10)
    list_header.pack(fill="x")
    tk.Label(list_header, text="Announcement Board", font=("Arial", 11, "bold"), bg="#f1f3f5", fg="#495057").pack(side="left", padx=20)

    table_body = tk.Frame(list_container, bg="white", padx=15, pady=15)
    table_body.pack(fill="both", expand=True)

    # Treeview Styling
    style = ttk.Style()
    style.configure("User.Treeview", font=("Arial", 10), rowheight=30)
    style.configure("User.Treeview.Heading", font=("Arial", 11, "bold"))

    columns = ("Date", "Title", "Category", "Posted By")
    tree = ttk.Treeview(table_body, columns=columns, show="headings", style="User.Treeview")
    tree.heading("Date", text="DATE POSTED")
    tree.heading("Title", text="SUBJECT / TITLE")
    tree.heading("Category", text="CATEGORY")
    tree.heading("Posted By", text="FROM")
    
    tree.column("Date", width=160, anchor="center")
    tree.column("Title", width=400, anchor="w")
    tree.column("Category", width=120, anchor="center")
    tree.column("Posted By", width=160, anchor="center")
    tree.pack(fill="both", expand=True, side="left")

    # Tag for highlighting new notices
    tree.tag_configure("new_notice", foreground="#4caa15", font=("Times New Roman", 12, "bold","italic"))

    scrollbar = ttk.Scrollbar(table_body, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    def show_details(event):
        item = tree.selection()
        if not item: return
        
        values = tree.item(item)['values']
        tags = tree.item(item)['tags']
        if not tags: return
        notice_id = tags[0]
        title = values[1]
        
        # Track view
        database.mark_as_seen(user_data['id'], notice_id)
        database.add_view(notice_id, user_data['name'])
        refresh_user_notices(filter_var.get())
        
        # Fetch fresh data by ID
        notice_data = database.get_notice_by_id(notice_id)
        
        if notice_data:
            detail_win = tk.Toplevel(root)
            detail_win.title(title)
            detail_win.geometry("550x500")
            detail_win.configure(bg="white", padx=35, pady=35)
            
            tk.Label(detail_win, text=notice_data[1], font=("Helvetica", 18, "bold"), bg="white", fg="#1877f2", wraplength=480, justify="left").pack(anchor="w", pady=(0, 5))
            
            cat_tag = tk.Label(detail_win, text=f" {notice_data[3].upper()} ", font=("Arial", 9, "bold"), bg="#e7f3ff", fg="#1877f2", pady=3)
            cat_tag.pack(anchor="w", pady=(0, 15))
            
            tk.Label(detail_win, text=f"Posted by {notice_data[4]} on {notice_data[5]}", font=("Arial", 9), bg="white", fg="#7f8c8d").pack(anchor="w", pady=(0, 25))
            
            txt_box_frame = tk.Frame(detail_win, bg="#ced4da", padx=1, pady=1)
            txt_box_frame.pack(fill="both", expand=True)
            
            scroll_text = tk.Text(txt_box_frame, font=("Arial", 11), bg="#f9f9f9", bd=0, padx=20, pady=20, spacing2=5)
            scroll_text.insert("1.0", notice_data[2])
            scroll_text.config(state="disabled")
            scroll_text.pack(fill="both", expand=True)

            if notice_data[7]: # file_path
                def open_file():
                    try:
                        os.startfile(notice_data[7])
                    except Exception as e:
                        messagebox.showerror("Error", f"Could not open file: {e}")

                file_ext = os.path.splitext(notice_data[7])[1].upper()[1:]
                
                btn_frame = tk.Frame(detail_win, bg="white")
                btn_frame.pack(fill="x", pady=(20, 0))
                
                tk.Button(btn_frame, text=f"View Attachment ({file_ext})", bg="#28a745", fg="white", font=("Arial", 10, "bold"), bd=0, command=open_file, pady=8, cursor="hand2").pack(side="left", fill="x", expand=True, padx=(0, 5))

                def download_file():
                    source = notice_data[7]
                    if not os.path.exists(source):
                        messagebox.showerror("Error", "Source file not found.")
                        return
                        
                    filename = os.path.basename(source)
                    dest = filedialog.asksaveasfilename(initialfile=filename, title="Download Attachment",
                                                       filetypes=[("All Files", "*.*")])
                    if dest:
                        try:
                            shutil.copy(source, dest)
                            messagebox.showinfo("Success", f"File downloaded successfully to:\n{dest}")
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to download file: {e}")

                tk.Button(btn_frame, text="Download", bg="#6f42c1", fg="white", font=("Arial", 10, "bold"), bd=0, command=download_file, pady=8, cursor="hand2").pack(side="left", fill="x", expand=True, padx=(5, 0))
            
            tk.Button(detail_win, text="Dismiss", bg="#f1f3f5", fg="#495057", font=("Arial", 10, "bold"), bd=0, command=detail_win.destroy, pady=8, cursor="hand2").pack(fill="x", pady=(10, 0))
        else:
            messagebox.showerror("Error", "Could not load the notice content. It may have been deleted.")

    tree.bind("<Double-1>", show_details)

    def refresh_user_notices(category="All Notices"):
        for i in tree.get_children():
            tree.delete(i)
        
        if category == "All Notices":
            notices = database.get_all_notices()
        else:
            notices = database.get_notices_by_category(category)
            
        for n in notices:
            is_seen = database.is_notice_seen(user_data['id'], n[0])
            display_title = n[1] if is_seen else f"[NEW] {n[1]}"
            tags = (n[0],) if is_seen else (n[0], "new_notice")
            tree.insert("", tk.END, values=(n[5], display_title, n[3], n[4]), tags=tags)

    refresh_user_notices()
    
    footer = tk.Frame(content, bg="#f4f7f6")
    footer.pack(fill="x", pady=15)
    tk.Label(footer, text="Double-click any notice to view full details.", font=("Arial", 10, "italic"), bg="#f4f7f6", fg="#7f8c8d").pack()

    root.mainloop()

if __name__ == "__main__":
    user_dashboard({"id": 2, "role": "User", "name": "Test Student", "email": "student@test.com"})
