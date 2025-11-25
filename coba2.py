import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

#       DATABASE (SQLite)
conn = sqlite3.connect("nilai_siswa.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS siswa (
    id TEXT PRIMARY KEY,
    nama TEXT,
    bio INTEGER,
    fis INTEGER,
    ing INTEGER,
    prediksi TEXT
)
""")
conn.commit()

#   FUNGSI PREDIKSI JURUSAN

def prediksi_jurusan(bio, fis, ing):
    if bio >= fis and bio >= ing:
        return "Kedokteran"
    elif fis >= bio and fis >= ing:
        return "Teknik"
    else:
        return "Bahasa"

#           CREATE DATA

def create_data():
    try:
        bio = int(bio_var.get())
        fis = int(fis_var.get())
        ing = int(ing_var.get())
        hasil_prediksi = prediksi_jurusan(bio, fis, ing)

        cursor.execute("""
            INSERT INTO siswa (id, nama, bio, fis, ing, prediksi)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            id_var.get(),
            nama_var.get(),
            bio,
            fis,
            ing,
            hasil_prediksi
        ))
        conn.commit()

        refresh_table()
        clear_form()

    except Exception as e:
        messagebox.showerror("Error", str(e))

#           UPDATE DATA

def update_data():
    siswa_id = id_var.get()
    if siswa_id == "":
        messagebox.showwarning("Warning", "Masukkan ID siswa!")
        return

    try:
        bio = int(bio_var.get())
        fis = int(fis_var.get())
        ing = int(ing_var.get())
        hasil_prediksi = prediksi_jurusan(bio, fis, ing)

        cursor.execute("""
            UPDATE siswa 
            SET nama=?, bio=?, fis=?, ing=?, prediksi=?
            WHERE id=?
        """, (
            nama_var.get(),
            bio,
            fis,
            ing,
            hasil_prediksi,
            siswa_id
        ))
        conn.commit()

        if cursor.rowcount == 0:
            messagebox.showinfo("Info", "ID tidak ditemukan!")
        else:
            messagebox.showinfo("Success", "Data berhasil di-update!")

        refresh_table()
        clear_form()

    except Exception as e:
        messagebox.showerror("Error", str(e))

#           DELETE DATA


def delete_data():
    siswa_id = id_var.get()
    if siswa_id == "":
        messagebox.showwarning("Warning", "Masukkan ID siswa!")
        return

    cursor.execute("DELETE FROM siswa WHERE id=?", (siswa_id,))
    conn.commit()

    if cursor.rowcount == 0:
        messagebox.showinfo("Info", "ID tidak ditemukan!")
    else:
        messagebox.showinfo("Success", "Data berhasil dihapus!")

    refresh_table()
    clear_form()

#        REFRESH TABLE

def refresh_table():
    for row in data_tree.get_children():
        data_tree.delete(row)

    cursor.execute("SELECT * FROM siswa")
    for row in cursor.fetchall():
        data_tree.insert('', 'end', values=row)

#          CLEAR FORM

def clear_form():
    id_var.set('')
    nama_var.set('')
    bio_var.set('')
    fis_var.set('')
    ing_var.set('')

#     AUTO FILL FORM TABLE

def fill_form(event):
    selected = data_tree.selection()
    if selected:
        row = data_tree.item(selected)['values']
        id_var.set(row[0])
        nama_var.set(row[1])
        bio_var.set(row[2])
        fis_var.set(row[3])
        ing_var.set(row[4])

#             GUI

root = tk.Tk()
root.title("Input Nilai Siswa + Prediksi Jurusan")
root.geometry("850x600")

# Variables
id_var = tk.StringVar()
nama_var = tk.StringVar()
bio_var = tk.StringVar()
fis_var = tk.StringVar()
ing_var = tk.StringVar()


# FORM INPUT
tk.Label(root, text="ID Siswa").grid(row=0, column=0)
tk.Entry(root, textvariable=id_var).grid(row=0, column=1)

tk.Label(root, text="Nama Siswa").grid(row=1, column=0)
tk.Entry(root, textvariable=nama_var).grid(row=1, column=1)

tk.Label(root, text="Nilai Biologi").grid(row=2, column=0)
tk.Entry(root, textvariable=bio_var).grid(row=2, column=1)

tk.Label(root, text="Nilai Fisika").grid(row=3, column=0)
tk.Entry(root, textvariable=fis_var).grid(row=3, column=1)

tk.Label(root, text="Nilai Inggris").grid(row=4, column=0)
tk.Entry(root, textvariable=ing_var).grid(row=4, column=1)


# BUTTONS
btn_style = {
    "fg": "white",
    "width": 15,
    "activebackground": "#444"
}

tk.Button(root, text="Submit (Create)", bg="#28a745", **btn_style,
          command=create_data).grid(row=5, column=0)

tk.Button(root, text="Update", bg="#ffc107", **btn_style,
          command=update_data).grid(row=5, column=1)

tk.Button(root, text="Delete", bg="#dc3545", **btn_style,
          command=delete_data).grid(row=5, column=2)

tk.Button(root, text="Clear Form", bg="#007bff", **btn_style,
          command=clear_form).grid(row=5, column=3)


# TABEL (TreeView)
data_tree = ttk.Treeview(
    root,
    columns=("id", "nama", "bio", "fis", "ing", "prediksi"),
    show="headings"
)

for col in ("id", "nama", "bio", "fis", "ing", "prediksi"):
    data_tree.heading(col, text=col.upper())
    data_tree.column(col, width=120)

data_tree.grid(row=6, column=0, columnspan=5)

data_tree.bind("<ButtonRelease-1>", fill_form)

refresh_table()

root.mainloop()
