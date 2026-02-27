from tkinter import *
import sqlite3, sys
from tkinter import ttk, filedialog, messagebox
import pandas as pd

# ===== Database Connection =====
def connection():
    try:
        conn = sqlite3.connect("student.db")
    except Exception as e:
        messagebox.showerror("DB Error", f"Cannot connect to the database:\n{e}")
        raise
    return conn

# ===== Field Verifier =====
def verifier():
    for key, value in {
        "Student name": student_name.get(),
        "Roll no": roll_no.get(),
        "Branch": branch.get(),
        "Phone number": phone.get(),
        "Father name": father.get(),
        "Address": address.get(),
        "Blood Group": blood_group.get(),
        "Mother Name": mother_name.get(),
        "Community": community.get(),
        "Email": email.get(),
        "Aadhar Card": aadhar.get(),
        "Hostel/Day Scholar": hostel_status.get(),
        "Bank Account Number": bank_acc.get(),
        "Date of Birth": dob.get(),
        "Medium": medium.get()
    }.items():
        if not value:
            msg_text.set(f"⚠ {key} is required!")
            return False
    return True

# ===== CRUD Operations =====
def add_student():
    if not verifier():
        return
    try:
        rno = int(roll_no.get())
        ph = int(phone.get())
    except ValueError:
        msg_text.set("⚠ Roll No and Phone number must be numeric.")
        return

    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS STUDENTS(
                        NAME TEXT,
                        ROLL_NO INTEGER PRIMARY KEY,
                        BRANCH TEXT,
                        PHONE_NO INTEGER,
                        FATHER TEXT,
                        ADDRESS TEXT,
                        BLOOD_GROUP TEXT,
                        MOTHER_NAME TEXT,
                        COMMUNITY TEXT,
                        EMAIL TEXT,
                        AADHAR TEXT,
                        HOSTEL_STATUS TEXT,
                        BANK_ACCOUNT TEXT,
                        DOB TEXT,
                        MEDIUM TEXT
                    )''')
        cur.execute("INSERT INTO STUDENTS VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            student_name.get().strip(),
            rno,
            branch.get().strip(),
            ph,
            father.get().strip(),
            address.get().strip(),
            blood_group.get().strip(),
            mother_name.get().strip(),
            community.get().strip(),
            email.get().strip(),
            aadhar.get().strip(),
            hostel_status.get().strip(),
            bank_acc.get().strip(),
            dob.get().strip(),
            medium.get().strip()
        ))
        conn.commit()
        conn.close()
        msg_text.set("✅ Student added successfully!")
        clear_fields()
        view_student()
    except sqlite3.IntegrityError:
        msg_text.set("⚠ Roll number already exists.")
    except Exception as e:
        msg_text.set(f"Error adding student: {e}")

def view_student():
    for row in t1.get_children():
        t1.delete(row)
    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM STUDENTS ORDER BY ROLL_NO")
        data = cur.fetchall()
        conn.close()
        if not data:
            msg_text.set("⚠ No records found.")
        else:
            for i in data:
                t1.insert("", END, values=i)
            msg_text.set(f"✅ {len(data)} records displayed.")
    except Exception as e:
        msg_text.set(f"Error reading records: {e}")

def delete_student():
    if not roll_no.get():
        msg_text.set("⚠ Roll number is required to delete.")
        return
    try:
        rno = int(roll_no.get())
    except ValueError:
        msg_text.set("⚠ Roll No must be an integer.")
        return
    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM STUDENTS WHERE ROLL_NO=?", (rno,))
        conn.commit()
        conn.close()
        msg_text.set("🗑️ Student deleted successfully!")
        clear_fields()
        view_student()
    except Exception as e:
        msg_text.set(f"Error deleting student: {e}")

def update_student():
    if not verifier():
        return
    try:
        rno = int(roll_no.get())
        ph = int(phone.get())
    except ValueError:
        msg_text.set("⚠ Roll No and Phone number must be numeric.")
        return
    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute('''UPDATE STUDENTS SET
                        NAME=?, BRANCH=?, PHONE_NO=?, FATHER=?, ADDRESS=?,
                        BLOOD_GROUP=?, MOTHER_NAME=?, COMMUNITY=?, EMAIL=?, 
                        AADHAR=?, HOSTEL_STATUS=?, BANK_ACCOUNT=?, DOB=?, MEDIUM=?
                        WHERE ROLL_NO=?''', (
            student_name.get().strip(),
            branch.get().strip(),
            ph,
            father.get().strip(),
            address.get().strip(),
            blood_group.get().strip(),
            mother_name.get().strip(),
            community.get().strip(),
            email.get().strip(),
            aadhar.get().strip(),
            hostel_status.get().strip(),
            bank_acc.get().strip(),
            dob.get().strip(),
            medium.get().strip(),
            rno
        ))
        conn.commit()
        conn.close()
        msg_text.set("✅ Student record updated successfully!")
        clear_fields()
        view_student()
    except Exception as e:
        msg_text.set(f"Error updating student: {e}")

def clse():
    root.quit()

# ===== Download to Excel/CSV =====
def download_data():
    try:
        conn = connection()
        df = pd.read_sql_query("SELECT * FROM STUDENTS", conn)
        conn.close()
    except Exception as e:
        messagebox.showerror("Export Error", f"Could not read DB: {e}")
        return

    if df.empty:
        messagebox.showwarning("No Data", "⚠ No student records found to export.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")],
        title="Save File As"
    )
    if file_path:
        try:
            if file_path.endswith(".csv"):
                df.to_csv(file_path, index=False)
            else:
                df.to_excel(file_path, index=False)
            messagebox.showinfo("Download Complete", f"✅ Records saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save file: {e}")

# ===== Clear Fields =====
def clear_fields():
    for var in [student_name, roll_no, branch, phone, father, address, blood_group,
                mother_name, community, email, aadhar, hostel_status, bank_acc, dob, medium]:
        var.set("")
    try:
        t1.selection_remove(t1.selection())
    except:
        pass

def on_row_select(event):
    sel = t1.selection()
    if not sel:
        return
    vals = t1.item(sel[0], "values")
    if not vals:
        return
    student_name.set(vals[0])
    roll_no.set(vals[1])
    branch.set(vals[2])
    phone.set(vals[3])
    father.set(vals[4])
    address.set(vals[5])
    blood_group.set(vals[6])
    mother_name.set(vals[7])
    community.set(vals[8])
    email.set(vals[9])
    aadhar.set(vals[10])
    hostel_status.set(vals[11])
    bank_acc.set(vals[12])
    dob.set(vals[13])
    medium.set(vals[14])

# ===== Main UI =====
root = Tk()
root.title("Student Management System")
root.state("zoomed")

# ===== Gradient Background =====
bg_canvas = Canvas(root, highlightthickness=0)
bg_canvas.pack(fill=BOTH, expand=True)

def draw_gradient(canvas, color1, color2):
    canvas.update()
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    (r1, g1, b1) = root.winfo_rgb(color1)
    (r2, g2, b2) = root.winfo_rgb(color2)
    r_ratio = float(r2 - r1) / height
    g_ratio = float(g2 - g1) / height
    b_ratio = float(b2 - b1) / height
    for i in range(height):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = "#%04x%04x%04x" % (nr, ng, nb)
        canvas.create_line(0, i, width, i, fill=color)

def update_gradient(event):
    bg_canvas.delete("all")
    draw_gradient(bg_canvas, "#f8f6ff", "#cbd9ff")

bg_canvas.bind("<Configure>", update_gradient)

# ===== Scrollable Frame =====
outer_canvas = Canvas(bg_canvas, bg="#f5f5fa", highlightthickness=0)
outer_v = Scrollbar(root, orient=VERTICAL, command=outer_canvas.yview)
outer_h = Scrollbar(root, orient=HORIZONTAL, command=outer_canvas.xview)
outer_canvas.configure(yscrollcommand=outer_v.set, xscrollcommand=outer_h.set)
outer_v.place(relx=0.98, rely=0, relheight=1)
outer_h.pack(side=BOTTOM, fill=X)
outer_canvas.pack(fill=BOTH, expand=True, padx=20, pady=20)

main_frame = Frame(outer_canvas, bg="#ffffff", bd=2, relief="ridge")
outer_canvas.create_window((0, 0), window=main_frame, anchor="nw")
main_frame.bind("<Configure>", lambda e: outer_canvas.configure(scrollregion=outer_canvas.bbox("all")))

# ===== Mouse Scroll =====
def _on_mouse_wheel(event):
    if event.state & 0x0001:
        outer_canvas.xview_scroll(-1 * (event.delta // 120), "units")
    else:
        outer_canvas.yview_scroll(-1 * (event.delta // 120), "units")

outer_canvas.bind_all("<MouseWheel>", _on_mouse_wheel)
outer_canvas.bind_all("<Shift-MouseWheel>", _on_mouse_wheel)

# ===== Variables =====
student_name, roll_no, branch, phone, father, address, blood_group = [StringVar() for _ in range(7)]
mother_name, community, email, aadhar, hostel_status, bank_acc, dob, medium = [StringVar() for _ in range(8)]
msg_text = StringVar()

# ===== Title =====
Label(main_frame, text="🎓 STUDENT MANAGEMENT SYSTEM",
      font=("Segoe UI", 24, "bold"), fg="#1c2e4a", bg="#ffffff").pack(pady=25)

details_frame = Frame(main_frame, bg="#ffffff")
details_frame.pack(pady=10)
Frame(main_frame, bg="#cbd9ff", height=2).pack(fill=X, padx=80, pady=(0, 20))

fields_container = Frame(details_frame, bg="#ffffff")
fields_container.pack(anchor="center")
left_frame = Frame(fields_container, bg="#ffffff")
right_frame = Frame(fields_container, bg="#ffffff")
left_frame.pack(side=LEFT, padx=50, pady=10)
right_frame.pack(side=LEFT, padx=50, pady=10)

def create_field(frame, label_text, var):
    Label(frame, text=label_text, font=("Segoe UI", 10, "bold"), fg="#1a2b4b", bg="#ffffff").pack(anchor="w")
    Entry(frame, textvariable=var, width=30, font=("Segoe UI", 10), relief="solid", bd=1, bg="#f9f9ff").pack(pady=4)

left_fields = [
    ("Student Name:", student_name),
    ("Roll No:", roll_no),
    ("Branch:", branch),
    ("Phone Number:", phone),
    ("Father Name:", father),
    ("Address:", address),
    ("Blood Group:", blood_group),
]
right_fields = [
    ("Mother Name:", mother_name),
    ("Community:", community),
    ("Email:", email),
    ("Aadhar Card:", aadhar),
    ("Hostel/Day Scholar:", hostel_status),
    ("Bank Account No:", bank_acc),
    ("Date of Birth:", dob),
    ("Medium:", medium),
]

for f_list, frame in [(left_fields, left_frame), (right_fields, right_frame)]:
    for label_text, var in f_list:
        create_field(frame, label_text, var)

# ===== Buttons =====
btn_frame = Frame(main_frame, bg="#ffffff")
btn_frame.pack(pady=20)
btn_style = {"width": 20, "height": 2, "font": ("Segoe UI", 10, "bold"), "relief": "groove", "bd": 1}
Button(btn_frame, text="ADD STUDENT", command=add_student, bg="#a8e6cf", **btn_style).grid(row=0, column=0, padx=10, pady=5)
Button(btn_frame, text="VIEW ALL STUDENTS", command=view_student, bg="#dcedc1", **btn_style).grid(row=0, column=1, padx=10, pady=5)
Button(btn_frame, text="DELETE STUDENT", command=delete_student, bg="#ffaaa5", **btn_style).grid(row=0, column=2, padx=10, pady=5)
Button(btn_frame, text="UPDATE INFO", command=update_student, bg="#ffd3b6", **btn_style).grid(row=1, column=0, padx=10, pady=5)
Button(btn_frame, text="DOWNLOAD RECORDS", command=download_data, bg="#a0ced9", **btn_style).grid(row=1, column=1, padx=10, pady=5)
Button(btn_frame, text="CLOSE", command=clse, bg="#666666", fg="white", **btn_style).grid(row=1, column=2, padx=10, pady=5)

# ===== Status Message =====
Label(main_frame, textvariable=msg_text, font=("Segoe UI", 10, "bold"), fg="#b91c1c", bg="#ffffff").pack(pady=10)

# ===== Table =====
Label(main_frame, text="📋 STUDENT RECORDS", font=("Segoe UI", 14, "bold"), fg="#1c2e4a", bg="#ffffff").pack(pady=(15, 5))
table_frame = Frame(main_frame, bg="#ffffff")
table_frame.pack(fill=BOTH, expand=True, padx=50, pady=10)

columns = ["NAME", "ROLL_NO", "BRANCH", "PHONE_NO", "FATHER", "ADDRESS", "BLOOD_GROUP",
           "MOTHER_NAME", "COMMUNITY", "EMAIL", "AADHAR", "HOSTEL_STATUS", "BANK_ACCOUNT", "DOB", "MEDIUM"]

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#cfe0fc", foreground="black")
style.configure("Treeview", font=("Segoe UI", 9), rowheight=28, background="#f8f9ff", fieldbackground="#f8f9ff")

t1 = ttk.Treeview(table_frame, columns=columns, show="headings", style="Treeview")
vsb = ttk.Scrollbar(table_frame, orient="vertical", command=t1.yview)
hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=t1.xview)
t1.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
for col in columns:
    t1.heading(col, text=col)
    t1.column(col, width=130, anchor="center")
vsb.pack(side=RIGHT, fill=Y)
hsb.pack(side=BOTTOM, fill=X)
t1.pack(side=LEFT, fill=BOTH, expand=True)
t1.bind("<<TreeviewSelect>>", on_row_select)

view_student()
root.mainloop()