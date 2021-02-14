from tkinter import PhotoImage, Scrollbar, Tk, Entry, Button, Frame, Label, messagebox, LabelFrame
from tkinter.constants import E, END, LEFT, RIGHT, W, Y
from tkinter.ttk import Treeview
from datetime import datetime
from db import create_connection, load_all_records, add_record, update_record, get_last_record, delete_record
from document import export_record_to_doc


db_file = "data/table.db"
ICON_PHOTO_PATH = "data/images/icon.png"
entry_font = ("Arial", 15)
label_font = entry_font


class MainApp():
    def __init__(self, master):
        self.master = master
        self.master.title("Covid Test System Management")
        img = PhotoImage(file=ICON_PHOTO_PATH)
        self.master.iconphoto(False, img)

        # Frames
        self.main_f = Frame(master)
        self.main_f.pack(padx=5, pady=5)

        self.top_f = LabelFrame(self.main_f, text="Údaje")
        self.top_f.pack(side="top", padx=5, pady=5)
        self.top_inner_f = Frame(self.top_f)
        self.top_inner_f.pack(padx=5, pady=10)
        self.top_serial_num_f = Frame(self.top_inner_f)
        self.top_serial_num_f.pack(pady=5)
        self.top_field_f_wrapper = Frame(self.top_inner_f)
        self.top_field_f_wrapper.pack(side="top", pady=10)
        self.top_f_wrapper = Frame(self.top_inner_f)
        self.top_f_wrapper.pack(side="bottom", pady=5)

        self.right_f = LabelFrame(self.main_f, text="Tabuľka")
        self.right_f.pack(side="bottom", padx=5, pady=5)
        self.table_f = Frame(self.right_f)
        self.table_f.pack(pady=10)
        self.table_self_f = Frame(self.table_f)     # Frame which contains treeview and scrollbar
        self.table_self_f.pack(padx=10)             # To add padding aroung (X axis)
        self.table_btn_f = Frame(self.right_f)
        self.table_btn_f.pack()
        

        # LEFT FRAME
        self.serial_num_l = Entry(self.top_serial_num_f, font=("Arial", 15, "bold"), width=4, justify="center")
        self.serial_num_l.pack()

        fname_l = Label(self.top_field_f_wrapper, text="Meno:", font=label_font)
        fname_l.grid(row=1, column=0, sticky=E, pady=3)
        self.fname_e = Entry(self.top_field_f_wrapper, font=entry_font)
        self.fname_e.grid(row=1, column=1, padx=12, pady=3)

        lname_l = Label(self.top_field_f_wrapper, text="Priezvisko:", font=label_font)
        lname_l.grid(row=2, column=0, sticky=E, pady=3)
        self.lname_e = Entry(self.top_field_f_wrapper, font=entry_font)
        self.lname_e.grid(row=2, column=1, padx=12, pady=3)

        birthday_l = Label(self.top_field_f_wrapper, text="Dátum narodenia:",font=label_font)
        birthday_l.grid(row=3, column=0, sticky=E, pady=3)
        self.birthday_e = Entry(self.top_field_f_wrapper, font=entry_font)
        self.birthday_e.grid(row=3, column=1, padx=12, pady=3)

        identif_num_l = Label(self.top_field_f_wrapper, text="Rodné číslo:", font=label_font)
        identif_num_l.grid(row=1, column=2, sticky=E)
        self.identif_num_e = Entry(self.top_field_f_wrapper, font=entry_font)
        self.identif_num_e.grid(row=1, column=3, padx=12)

        street_l = Label(self.top_field_f_wrapper, text="Ulica:", font=label_font)
        street_l.grid(row=2, column=2, sticky=E)
        self.street_e = Entry(self.top_field_f_wrapper, font=entry_font)
        self.street_e.grid(row=2, column=3, padx=12)

        city_l = Label(self.top_field_f_wrapper, text="Mesto:", font=label_font)
        city_l.grid(row=3, column=2, sticky=E)
        self.city_e = Entry(self.top_field_f_wrapper, font=entry_font)
        self.city_e.grid(row=3, column=3, padx=12)

        postcode_l = Label(self.top_field_f_wrapper, text="PSČ:", font=label_font)
        postcode_l.grid(row=1, column=4, sticky=E)
        self.postcode_e = Entry(self.top_field_f_wrapper, font=entry_font)
        self.postcode_e.grid(row=1, column=5, padx=12)

        phone_num_l = Label(self.top_field_f_wrapper, text="Tel. číslo:", font=label_font)
        phone_num_l.grid(row=2, column=4, sticky=E)
        self.phone_num_e = Entry(self.top_field_f_wrapper, font=entry_font)
        self.phone_num_e.grid(row=2, column=5, padx=12)

        note_l = Label(self.top_field_f_wrapper, text="Poznámka:", font=label_font)
        note_l.grid(row=3, column=4, sticky=E)
        self.note_e = Entry(self.top_field_f_wrapper, font=entry_font)
        self.note_e.grid(row=3, column=5, padx=12)

        self.id_l = Label(self.top_field_f_wrapper, text="")

        self.submit_btn = Button(self.top_f_wrapper, text="Pridať", command=lambda: self.save_new_record(), width=20)
        self.submit_btn.pack(side="left", padx=5)

        self.discard_btn = Button(self.top_f_wrapper, text="X", command=lambda: self.discard_changes(), foreground="red")
        self.discard_btn.pack(side="right", padx=5)

        # RIGHT FRAME
        self.table = Treeview(self.table_self_f)
        self.table.pack(side=LEFT)

        edit_btn = Button(self.table_btn_f, text="Upraviť", command=lambda: self.select_row(), width=20)
        edit_btn.grid(row=1, column=0, padx=5, pady=10)

        delete_btn = Button(self.table_btn_f, text="Vymazať", command=lambda: self.delete_row(), width=20)
        delete_btn.grid(row=1, column=1, padx=5)

        create_doc_btn = Button(self.table_btn_f, text="Tlač", command=lambda: self.create_document(), width=20)
        create_doc_btn.grid(row=1, column=2, padx=5)

        self.define_table()
        self.set_next_serial_num()


    def define_table(self):
        """ Define columns of table treeview """

        self.table["columns"] = ("fname", "lname", "bday", "identif_num", "street",
                                "city", "postcode_num", "phone_num", "note", "id")
        
        self.table.column("#0", width=50)
        self.table.column("fname", width=120)
        self.table.column("lname", width=120)
        self.table.column("bday", width=120)
        self.table.column("identif_num", width=120)
        self.table.column("street", width=140)
        self.table.column("city", width=120)
        self.table.column("postcode_num", width=70)
        self.table.column("phone_num", width=120)
        self.table.column("note", width=120)
        self.table.column("id", width=30)     # Hidden column to track record id

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
        self.table.heading("id", text="ID")
        
        table_scrollbar = Scrollbar(self.table_self_f, command=self.table.yview, orient="vertical")
        table_scrollbar.pack(side=RIGHT, fill=Y)
        self.table.configure(yscrollcommand=table_scrollbar.set)

        visible_cols = ["fname", "lname", "bday", "identif_num",
                    "street", "city", "postcode_num", "phone_num", "note"]
        self.table["displaycolumns"] = visible_cols

        self.fill_table()


    
    def fill_table(self):
        """ Fill treeview with data from databse """

        conn = create_connection(db_file)
        data = load_all_records(conn)
        conn.close()

        for row in data:
            self.table.insert(parent="", index=0, text=row[1], values=(row[2], row[3], row[4],
                                row[5], row[6], row[7], row[8], row[9], row[10], row[0]))


    def set_next_serial_num(self):
        """ Set next available serial number to to the field,
            which stores serial number in app """

        conn = create_connection(db_file)
        last_record = get_last_record(conn)
        conn.close()

        new_serial_num = int(last_record[1]) + 1

        self.serial_num_l.insert(0, str(new_serial_num))


    def save_new_record(self):
        """ Handle all functions, which are neccessery
            to save a new record """

        row = self.get_inputs()
        if row == False:
            messagebox.showwarning("Chyba",
                                "Niektoré polia sú prázdne!\n" \
                                "Prosím skontrolujte, či ste vyplnili všetky polia.")
            return
        elif row[:-1]:
            row = row[:-1]
    
        conn = create_connection(db_file)
        add_record(conn, row)
        conn.close()  

        self.clear_entries()
        self.clear_table()
        self.fill_table()     
        self.set_next_serial_num()


    def save_update(self):
        """ Handle all functions, which are neccessery
            to update an existing record """

        record = self.get_inputs()
        self.update_record(record)

        self.submit_btn.configure(command=lambda: self.save_new_record(), text="Pridať")
        self.clear_entries()
        self.clear_table()
        self.fill_table()
        self.set_next_serial_num()


    def select_row(self):
        """ Insert data to the data fields,
            according to selected row in treeview """

        selection = self.table.focus()
        if not selection:
            messagebox.showwarning("Chyba", "Nebol vybraný žiaden riadok!\n" \
                                "Prosím vyberte riadok a skúste to znova.")
            return
        
        serial_num = self.table.item(selection)["text"]
        row = self.table.item(selection, option="values")

        self.clear_entries()
        self.serial_num_l.insert(0, serial_num)
        self.fname_e.insert(0, row[0])
        self.lname_e.insert(0, row[1])
        self.birthday_e.insert(0, row[2])
        self.identif_num_e.insert(0, row[3])
        self.street_e.insert(0, row[4])
        self.city_e.insert(0, row[5])
        self.postcode_e.insert(0, row[6])
        self.phone_num_e.insert(0, row[7])
        self.note_e.insert(0, row[8])
        self.id_l["text"] = row[9]

        self.submit_btn.configure(command=lambda: self.save_update(), text="Uložiť")


    def get_inputs(self):
        """ Return data from data fields """

        row = []
        row.append(self.serial_num_l.get())
        row.append(self.fname_e.get())
        row.append(self.lname_e.get())
        row.append(self.birthday_e.get())
        row.append(self.identif_num_e.get())
        row.append(self.street_e.get())
        row.append(self.city_e.get())
        row.append(self.postcode_e.get())
        row.append(self.phone_num_e.get())
        row.append(self.note_e.get())
        row.append(self.id_l["text"])

        # Check if entries are empty
        for i in range(len(row)-3):    # Excluding serial_num(0), notes(9), id(10)
            if row[i+1] == "":
                return False
        return row


    def update_record(self, record):
        """ Update record 'record' with updated data """

        conn = create_connection(db_file)
        update_record(conn, record)
        conn.close()


    def clear_table(self):
        """ Delete all rows from treeview """
        for r in self.table.get_children():
            self.table.delete(r) 

    
    def clear_entries(self):
        """ Clear all entry fields """

        self.serial_num_l.delete(0, "end")
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
        """ Don't save changes from fields
            and update next available serial number """

        self.clear_entries()
        self.set_next_serial_num()
        self.submit_btn.configure(command=lambda: self.save_new_record(), text="Pridať")

    
    def delete_row(self):
        """ Delete record from database """

        item = self.table.focus()
        if not item:
            messagebox.showwarning("Chyba", "Nebol vybraný žiaden riadok!\n" \
                                "Prosím vyberte riadok a skúste to znova.")
            return

        row = self.table.item(item)

        conn = create_connection(db_file)
        delete_record(conn, row["text"])
        conn.close()

        self.clear_table()
        self.fill_table()
        # Ensure "hard refresh", prevent the occurrence of bugs
        self.clear_entries()
        self.set_next_serial_num()
        self.submit_btn.configure(command=lambda: self.save_new_record(), text="Pridať")


    def create_document(self):
        """ Modify document to print with data of selected row
            in table and open in Excel """
        
        record = {}
        selection = self.table.focus()
        if not selection:
            messagebox.showwarning("Chyba", "Nebol vybraný žiaden riadok!\n" \
                                "Prosím vyberte riadok a skúste to znova.")
            return
        
        data = self.table.item(selection, option="values")
        
        record["fname"] = data[0]
        record["lname"] = data[1]
        record["residence"] = ", ".join([data[4], data[6], data[5]])
        record["birth_date"] = data[2]
        record["today"] = datetime.now().strftime("%d/%m/%y")
        export_record_to_doc(record)

        


if __name__ == "__main__":
    root = Tk()
    app = MainApp(root)
    root.mainloop()