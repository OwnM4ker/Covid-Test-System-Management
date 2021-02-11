from tkinter import Tk, Entry, Button, Frame, Label, messagebox, LabelFrame
from tkinter.constants import E, END, W
from tkinter.ttk import Treeview
from datetime import datetime
from db import create_connection, load_all_records, add_record, update_record, get_last_record, delete_record


db_file = "table.db"


class MainApp():
    def __init__(self, master):
        self.master = master
        self.top_f = Frame(master)
        self.top_f.pack(padx=5, pady=5)
        self.left_f = LabelFrame(self.top_f, text="Údaje")
        self.left_f.pack(side="left", padx=5)
        self.right_f = LabelFrame(self.top_f, text="Tabuľka")
        self.right_f.pack(side="right", padx=5)
        # self.bottom_f = Frame()
        # self.bottom_f.pack()
        self.left_f_wrapper = Frame(self.left_f)
        self.left_f_wrapper.grid(row=10, column=0, columnspan=2, pady=10)

        self.serial_num_l = Label(self.left_f, text="")
        self.serial_num_l.grid(row=0, column=0, columnspan=2)

        fname_l = Label(self.left_f, text="Meno:")
        fname_l.grid(row=1, column=0, sticky=W)
        self.fname_e = Entry(self.left_f)
        self.fname_e.grid(row=1, column=1)

        lname_l = Label(self.left_f, text="Priezvisko:")
        lname_l.grid(row=2, column=0)
        self.lname_e = Entry(self.left_f)
        self.lname_e.grid(row=2, column=1)

        birthday_l = Label(self.left_f, text="Dátum narodenia:")
        birthday_l.grid(row=3, column=0)
        self.birthday_e = Entry(self.left_f)
        self.birthday_e.grid(row=3, column=1)

        identif_num_l = Label(self.left_f, text="Rodné číslo:")
        identif_num_l.grid(row=4, column=0)
        self.identif_num_e = Entry(self.left_f)
        self.identif_num_e.grid(row=4, column=1)

        street_l = Label(self.left_f, text="Ulica:")
        street_l.grid(row=5, column=0)
        self.street_e = Entry(self.left_f)
        self.street_e.grid(row=5, column=1)

        city_l = Label(self.left_f, text="Mesto:")
        city_l.grid(row=6, column=0)
        self.city_e = Entry(self.left_f)
        self.city_e.grid(row=6, column=1)

        postcode_l = Label(self.left_f, text="PSČ:")
        postcode_l.grid(row=7, column=0)
        self.postcode_e = Entry(self.left_f)
        self.postcode_e.grid(row=7, column=1)

        phone_num_l = Label(self.left_f, text="Tel. číslo:")
        phone_num_l.grid(row=8, column=0)
        self.phone_num_e = Entry(self.left_f)
        self.phone_num_e.grid(row=8, column=1)

        note_l = Label(self.left_f, text="Poznámka:")
        note_l.grid(row=9, column=0)
        self.note_e = Entry(self.left_f)
        self.note_e.grid(row=9, column=1)

        self.submit_btn = Button(self.left_f_wrapper, text="Pridať", command=lambda: self.save_new_record(), width=20)
        self.submit_btn.pack(side="left", padx=5)

        self.discard_btn = Button(self.left_f_wrapper, text="X", command=lambda: self.discard_changes(), foreground="red")
        self.discard_btn.pack(side="right", padx=5)

        self.table = Treeview(self.right_f)
        self.table.grid(row=0, column=0, columnspan=2, padx=15, pady=5)
        self.table["columns"] = ("fname", "lname", "bday", "identif_num", "street",
                                "city", "postcode_num", "phone_num", "note")
        
        self.table.column("#0", width=50)
        self.table.column("fname", width=100)
        self.table.column("lname", width=100)
        self.table.column("bday", width=100)
        self.table.column("identif_num", width=100)
        self.table.column("street", width=100)
        self.table.column("city", width=100)
        self.table.column("postcode_num", width=100)
        self.table.column("phone_num", width=100)
        self.table.column("note", width=100)

        self.table.heading("#0", text="P.Č.")
        self.table.heading("fname",text="Meno")
        self.table.heading("lname",text="Priezvisko")
        self.table.heading("bday",text="Dátum narodenia")
        self.table.heading("identif_num",text="Č. poistenca")
        self.table.heading("street",text="Ulica")
        self.table.heading("city",text="Mesto")
        self.table.heading("postcode_num",text="PSČ")
        self.table.heading("phone_num",text="Tel. číslo")
        self.table.heading("note",text="Poznámka")

        edit_btn = Button(self.right_f, text="Upraviť", command=lambda: self.select_row(), width=20)
        edit_btn.grid(row=1, column=0, padx=5, pady=10)

        delete_btn = Button(self.right_f, text="Vymazať", command=lambda: self.delete_row(), width=20)
        delete_btn.grid(row=1, column=1, padx=5)

        # self.submit_btn.bind("<Return>", self.add)
        # self.left_f.bind("<Return>", self.add)
        # self.fname_e.bind("<Return>", self.add)
        # self.lname_e.bind("<Return>", self.add)
        # self.birthday_e.bind("<Return>", self.add)
        # self.identif_num_e.bind("<Return>", self.add)
        # self.street_e.bind("<Return>", self.add)
        # self.city_e.bind("<Return>", self.add)
        # self.postcode_e.bind("<Return>", self.add)
        # self.phone_num_e.bind("<Return>", self.add)
        # self.note_e.bind("<Return>", self.add)

        self.fill_table()
        self.set_next_serial_num()

    
    def fill_table(self):
        conn = create_connection(db_file)
        data = load_all_records(conn)
        conn.close()

        for row in data:
            self.table.insert(parent="", index=0, text=row[1], values=(row[2], row[3], row[4],
                                row[5], row[6], row[7], row[8], row[9], row[10]))


    def set_next_serial_num(self):
        conn = create_connection(db_file)
        last_record = get_last_record(conn)
        conn.close()

        new_serial_num = int(last_record[1]) + 1

        self.serial_num_l.configure(text=str(new_serial_num))


    def save_new_record(self):
        row = self.get_inputs()
        if row == False:
            messagebox.showwarning("Chýbajúce dáta",
                                "Niektoré polia sú prázdne!\n" \
                                "Prosím skontrolujte, či ste vyplnili všetky polia")
            return

        record = self.get_inputs()
        conn = create_connection(db_file)
        add_record(conn, record)
        conn.close()  

        self.clear_entries()
        self.clear_table()
        self.fill_table()     
        self.set_next_serial_num()


    def save_update(self):
        record = self.get_inputs()
        record.append(record[0])
        self.update_record(record)

        self.submit_btn.configure(command=lambda: self.save_new_record(), text="Pridať")
        self.clear_entries()
        self.clear_table()
        self.fill_table()
        self.set_next_serial_num()


    def select_row(self):
        item = self.table.focus()
        row = self.table.item(item)

        self.clear_entries()
        self.serial_num_l["text"] = row["text"]
        self.fname_e.insert(0, row["values"][0])
        self.lname_e.insert(0, row["values"][1])
        self.birthday_e.insert(0, row["values"][2])
        self.identif_num_e.insert(0, row["values"][3])
        self.street_e.insert(0, row["values"][4])
        self.city_e.insert(0, row["values"][5])
        self.postcode_e.insert(0, row["values"][6])
        self.phone_num_e.insert(0, row["values"][7])
        self.note_e.insert(0, row["values"][8])

        self.submit_btn.configure(command=lambda: self.save_update(), text="Uložiť")


    def get_inputs(self):
        row = []
        row.append(self.serial_num_l["text"])
        row.append(self.fname_e.get())
        row.append(self.lname_e.get())
        row.append(self.birthday_e.get())
        row.append(self.identif_num_e.get())
        row.append(self.street_e.get())
        row.append(self.city_e.get())
        row.append(self.postcode_e.get())
        row.append(self.phone_num_e.get())
        row.append(self.note_e.get())

        for i in range(len(row)-2):    # Excluding index (0) and notes (9)
            if row[i+1] == "":
                return False
        return row


    def update_record(self, record):

        conn = create_connection(db_file)
        update_record(conn, record)
        conn.close()


    def clear_table(self):
        for r in self.table.get_children():
            self.table.delete(r) 

    
    def clear_entries(self):
        self.fname_e.delete(0, "end")
        self.lname_e.delete(0, "end")
        self.birthday_e.delete(0, "end")
        self.identif_num_e.delete(0, "end")
        self.street_e.delete(0, "end")
        self.city_e.delete(0, "end")
        self.postcode_e.delete(0, "end")
        self.phone_num_e.delete(0, "end")
        self.note_e.delete(0, "end")


    def discard_changes(self):
        self.clear_entries()
        self.set_next_serial_num()
        self.submit_btn.configure(command=lambda: self.save_new_record(), text="Uložiť")

    
    def delete_row(self):
        item = self.table.focus()
        row = self.table.item(item)

        conn = create_connection(db_file)
        delete_record(conn, row["text"])
        conn.close()

        self.clear_table()
        self.fill_table()


        


if __name__ == "__main__":
    root = Tk()
    app = MainApp(root)
    root.mainloop()