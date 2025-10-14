import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# --- Database Connection Function ---
def get_db_connection():
    try:
        # NOTE: Verify your credentials. The code now assumes a correct connection.
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='0206', # Assuming this is the correct password
            database='webgui'
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Database Connection Error", f"Failed to connect to database: {err}")
        return None

# --- Utility Functions ---

def clear_entries():
    """Clears all input fields and resets the ID entry state."""
    entry_id.config(state="normal")
    entry_id.delete(0, tk.END)
    entry_id.config(state="disabled")
    
    entry_name.delete(0, tk.END)
    entry_course.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_branch.delete(0, tk.END)
    entry_fee.delete(0, tk.END)
    
    entry_age_search.delete(0, tk.END)
    entry_branch_search.delete(0, tk.END)
    
    for selected_item in tree.selection():
        tree.selection_remove(selected_item)

def validate_numeric(value, field_name):
    """Helper function to validate if a string is a valid number."""
    try:
        # Check if the value is empty, which might happen if the database has NULLs,
        # but for user input validation, we assume non-empty if we reach here.
        if not value: return None
        
        if field_name == 'age':
            return int(value)
        elif field_name == 'fee':
            return float(value)
    except ValueError:
        messagebox.showerror("Input Error", f"{field_name.capitalize()} must be a valid number.")
        return None

def on_tree_select(event):
    """Populates input fields when a row in the Treeview is selected."""
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item, 'values')
        
        # Populate the ID field (enable, insert, disable)
        entry_id.config(state="normal")
        entry_id.delete(0, tk.END)
        entry_id.insert(0, values[0]) # Id
        entry_id.config(state="disabled")

        # Populate other fields
        entry_name.delete(0, tk.END); entry_name.insert(0, values[1])   # Name
        entry_course.delete(0, tk.END); entry_course.insert(0, values[2]) # Course
        entry_age.delete(0, tk.END); entry_age.insert(0, values[3])     # Age
        entry_branch.delete(0, tk.END); entry_branch.insert(0, values[4]) # Branch
        entry_fee.delete(0, tk.END); entry_fee.insert(0, values[5])     # Fee

# --- CRUD Operations ---

def add_student():
    name = entry_name.get()
    course = entry_course.get()
    age_str = entry_age.get()
    branch = entry_branch.get()
    fee_str = entry_fee.get()

    if not all([name, course, age_str, branch, fee_str]):
        messagebox.showerror("Input Error", "All fields must be filled.")
        return
    
    age = validate_numeric(age_str, 'age')
    fee = validate_numeric(fee_str, 'fee')
    if age is None or fee is None:
        return

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # SQL: ID is auto-incremented, so we insert the 5 data fields
            sql = "INSERT INTO registration (name, course, age, branch, fee) VALUES (%s, %s, %s, %s, %s)"
            values = (name, course, age, branch, fee)
            
            cursor.execute(sql, values)
            conn.commit()
            
            messagebox.showinfo("Success", "Student record added successfully!")
            clear_entries()
            load_students()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to add student: {err}\n\n"
                                 "HINT: Did you run the 'ALTER TABLE' command in MySQL?")
        finally:
            conn.close()

def update_student():
    student_id = entry_id.get() 
    if not tree.selection() or not student_id:
        messagebox.showerror("Selection Error", "Please select a student to update.")
        return

    name = entry_name.get()
    course = entry_course.get()
    age_str = entry_age.get()
    branch = entry_branch.get()
    fee_str = entry_fee.get()

    if not all([name, course, age_str, branch, fee_str]):
        messagebox.showerror("Input Error", "All fields must be filled.")
        return

    age = validate_numeric(age_str, 'age')
    fee = validate_numeric(fee_str, 'fee')
    if age is None or fee is None:
        return

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE registration SET name=%s, course=%s, age=%s, branch=%s, fee=%s WHERE id=%s"
            values = (name, course, age, branch, fee, student_id)
            
            cursor.execute(sql, values)
            conn.commit()
            
            messagebox.showinfo("Success", "Student record updated successfully!")
            clear_entries()
            load_students()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to update student: {err}")
        finally:
            conn.close()

def delete_student():
    student_id = entry_id.get() 
    if not tree.selection() or not student_id:
        messagebox.showerror("Selection Error", "Please select a student to delete.")
        return

    if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete student ID {student_id}?"):
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "DELETE FROM registration WHERE id=%s"
                cursor.execute(sql, (student_id,))
                conn.commit()
                
                messagebox.showinfo("Success", "Student record deleted successfully!")
                clear_entries()
                load_students()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Failed to delete student: {err}")
            finally:
                conn.close()

# --- Load and Search Functions ---

def load_students(query="SELECT * FROM registration", params=None):
    for i in tree.get_children():
        tree.delete(i)

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", tk.END, values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to load students: {err}")
        finally:
            conn.close()

def search_by_age():
    age_search_value = entry_age_search.get()
    if not age_search_value:
        messagebox.showwarning("Search Input", "Please enter an age to search.")
        return
    
    if validate_numeric(age_search_value, 'age') is None:
        return

    load_students("SELECT * FROM registration WHERE age = %s", (age_search_value,))

def search_by_branch():
    branch_search_value = entry_branch_search.get()
    if not branch_search_value:
        messagebox.showwarning("Search Input", "Please enter a branch to search.")
        return
    
    load_students("SELECT * FROM registration WHERE branch LIKE %s", (f"%{branch_search_value}%",))

def refresh_students():
    clear_entries()
    load_students()

# --- GUI Setup ---
root = tk.Tk()
root.title("Student Management System")
root.geometry("800x650") 
root.configure(bg="#E0F2F7")

# --- Styling ---
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#E0F2F7", foreground="#01579B", font=("Arial", 10, "bold"))
style.configure("TButton", background="#03A9F4", foreground="#FFFFFF", font=("Arial", 10, "bold"))
style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#B3E5FC", foreground="#01579B")

# Title
title_label = tk.Label(root, text="Student Management", font=("Arial", 20, "bold"), fg="#01579B", bg="#E0F2F7")
title_label.grid(row=0, column=0, columnspan=5, pady=20)

# --- Input Frame ---
input_frame = tk.Frame(root, bg="#E0F2F7")
input_frame.grid(row=1, column=0, columnspan=5, padx=20, pady=10, sticky="ew")
input_frame.grid_columnconfigure(1, weight=1)

fields = ["Name:", "Course:", "Age:", "Branch:", "Fee:"]
entry_widgets = []

for i, text in enumerate(fields):
    ttk.Label(input_frame, text=text).grid(row=i, column=0, sticky="w", padx=10, pady=5)
    entry = ttk.Entry(input_frame, width=50)
    entry.grid(row=i, column=1, sticky="ew", padx=10, pady=5)
    entry_widgets.append(entry)

entry_name, entry_course, entry_age, entry_branch, entry_fee = entry_widgets
entry_id = ttk.Entry(input_frame); entry_id.config(state="disabled")

# --- Buttons Frame (CRUD + Refresh) ---
button_frame = tk.Frame(root, bg="#E0F2F7")
button_frame.grid(row=2, column=0, columnspan=5, pady=10)

# Custom button styles for color matching
style.configure('Add.TButton', background='#4CAF50', foreground='white') # Green
style.configure('Update.TButton', background='#FF9800', foreground='white') # Orange/Yellow
style.configure('Delete.TButton', background='#F44336', foreground='white') # Red
style.configure('Refresh.TButton', background='#2196F3', foreground='white') # Blue
style.configure('Search.TButton', background='#03A9F4', foreground='white') # Default Blue

ttk.Button(button_frame, text="Add", command=add_student, style='Add.TButton').grid(row=0, column=0, padx=5, pady=5)
ttk.Button(button_frame, text="Update", command=update_student, style='Update.TButton').grid(row=0, column=1, padx=5, pady=5)
ttk.Button(button_frame, text="Delete", command=delete_student, style='Delete.TButton').grid(row=0, column=2, padx=5, pady=5)
ttk.Button(button_frame, text="Refresh", command=refresh_students, style='Refresh.TButton').grid(row=0, column=3, padx=5, pady=5)


# --- Search Fields and Buttons ---
search_frame = tk.Frame(root, bg="#E0F2F7")
search_frame.grid(row=3, column=0, columnspan=5, pady=10)

# Age Search
entry_age_search = ttk.Entry(search_frame, width=15)
entry_age_search.grid(row=0, column=0, padx=5, pady=5)
ttk.Button(search_frame, text="Age Search", command=search_by_age, style='Search.TButton').grid(row=0, column=1, padx=5)

# Branch Search
entry_branch_search = ttk.Entry(search_frame, width=15)
entry_branch_search.grid(row=0, column=2, padx=5)
ttk.Button(search_frame, text="Branch Search", command=search_by_branch, style='Search.TButton').grid(row=0, column=3, padx=5)


# --- Treeview (Data Display) ---
tree_frame = ttk.Frame(root)
tree_frame.grid(row=4, column=0, columnspan=5, padx=20, pady=10, sticky="nsew")
root.grid_rowconfigure(4, weight=1)
root.grid_columnconfigure(0, weight=1)

cols = ("Id", "Name", "Course", "Age", "Branch", "Fee")
tree = ttk.Treeview(tree_frame, columns=cols, show="headings")

# Column configuration
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER)

tree.column("Id", width=50)
tree.column("Name", width=120)
tree.column("Course", width=100)
tree.column("Age", width=70)
tree.column("Branch", width=100)
tree.column("Fee", width=100)

tree.pack(side="left", fill="both", expand=True)

# Scrollbar
scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand=scrollbar.set)

tree.bind("<<TreeviewSelect>>", on_tree_select)

# Initial load
load_students()

root.mainloop()