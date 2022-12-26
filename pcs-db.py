import tkinter
from tkinter import ttk, Menu
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter.messagebox import askyesno
import os
import sqlite3
from sqlite3 import Error
from PIL import Image, ImageTk
import csv
import pyperclip
import matplotlib.pyplot as plt
import numpy as np

backgroud_color = "#F1F7FB"
font_color = "#2e3361"
button_color = "white"
global to_set_item, database_undo_cach, on_load
to_set_item = "No"
filepath = "pcs_data.db"
database_undo_cach = []
on_load = 0
room_values = []
box_values = []
global full_details
full_details = "No thank tou"


def creat_table():
    connection = sqlite3.connect("pcs_data.db")
    cursor = connection.cursor()
    try:
        sql = """CREATE TABLE pcs_data(
                Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                PC_Name text,
                Room text,
                Box text,
                itest text,
                office text,
                deepfreez text,
                proccessor text,
                memory text,
                status text,
                comment text)"""
        with connection:
            cursor.execute(sql)

    except:
        print("Table exist")
    if connection:
        connection.close()

def cach_database():
    connection = sqlite3.connect("pcs_data.db")
    cursor = connection.cursor()
    with connection:
        cursor.execute("SELECT * from pcs_data")
        cach_data = cursor.fetchall()
    if connection:
        connection.close()
    database_undo_cach.append(cach_data)
    print(len(database_undo_cach))

def enter_data():
    cach_database()
    to_set_item == "No"
    pc_name  = pc_name_entry.get().strip()
    print(pc_name)
    if pc_name:
        room = room_combobox.get()
        box = box_combobox.get()
        itest = itest_var.get()
        office = office_var.get()
        deepfreez = freez_var.get()
        status = status_combobox.get()
        comment = comment_entry.get()

#
        connection = sqlite3.connect(filepath)
        cursor = connection.cursor()

        if not name_exist(pc_name):
            sql = 'INSERT INTO pcs_data(PC_Name, Room, Box, itest, office, deepfreez, status, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
            val = (pc_name, room, box, itest, office, deepfreez, status, comment)
            with connection:
                cursor.execute(sql,val)
            db_update_status = f"{pc_name} was added to database"
        else:
            sql = 'UPDATE pcs_data SET Room = ? , Box = ? , itest = ? , office = ?, deepfreez = ? , status = ?,  comment = ? WHERE PC_Name = ?'
            val = (room, box, itest, office, deepfreez, status, comment, pc_name)
            with connection:
                cursor.execute(sql,val)
            db_update_status = f"PC {pc_name} entry was updated"
        if connection:
            connection.close()
        delete_text()
        print("data saved")
        answers.configure(state='normal')
        answers.insert("1.0", f"{db_update_status}")

    else:
        print("enter Name")
        delete_text()
        answers.configure(state='normal')
        answers.insert("1.0", "לא הכנסת שם מחשב")

    print_data()

def delete_pc():
    pc_to_delete = pc_name_entry.get()
    confirmation = delete_confirmation(pc_to_delete)
    print(confirmation)
    if confirmation == True:
        cach_database()
        print("delete_pc")
        connection = sqlite3.connect(filepath)
        cursor = connection.cursor()
        print(pc_to_delete)
        var = (pc_to_delete,)
        sql = "DELETE from pcs_data WHERE PC_Name = ?"
        with connection:
            cursor.execute(sql, var)
        if connection:
            connection.close()
        delete_text()
        answers.configure(state='normal')
        answers.insert("1.0", f"{[pc_to_delete]} - deleted from database")
        answers.configure(state='disabled')

def name_exist(pc_name):
    connection = sqlite3.connect(filepath)
    cursor = connection.cursor()
    sql = "SELECT PC_Name from pcs_data where PC_Name = ?"
    var = (pc_name,)
    with connection:
        cursor.execute(sql, var)
        answer01 = cursor.fetchall()
    if connection:
        connection.close()
    return answer01

def retrieve_data():
    global to_set_item, full_details
    full_details = "No thank you"
    to_set_item = "No"
    pc_name  = pc_name_entry.get().strip()
    room = room_combobox.get()
    box = box_combobox.get()
    itest = itest_var.get()
    office = office_var.get()
    deepfreez = freez_var.get()
    status = status_combobox.get()
    comment = comment_entry.get()

    if pc_name:
        sql= "SELECT * from pcs_data WHERE PC_Name = ?"
        var = (pc_name,)
        print(var)
        to_set_item = "Yes"


    elif room and box and itest == "Itest - Yes" and office == "office - Yes" and deepfreez == "DeepFreez - Yes":
        sql= "SELECT * from pcs_data WHERE Room = ? and Box = ? and itest = ? and office = ? and deepfreez = ? "
        var = (room, box, itest, office, deepfreez)


    elif box and itest =="Itest - Yes" and office == "office - Yes" and deepfreez == "DeepFreez - Yes":
        sql  =  "SELECT * from pcs_data WHERE Box = ? and itest = ? and office = ? and deepfreez = ?"
        var = (box, itest, office, deepfreez)
    elif room and itest =="Itest - Yes" and office == "office - Yes" and deepfreez == "DeepFreez - Yes":
        sql  =  "SELECT * from pcs_data WHERE Room = ? and itest = ? and office = ? and deepfreez = ? "
        var = (room, itest, office, deepfreez)
    elif room and box and itest == "Itest - Yes" and office == "office - Yes":
        sql= "SELECT * from pcs_data WHERE Room = ? and Box = ? and itest = ? and office = ?"
        var = (room, box, itest, office)


    elif room and box and itest =="Itest - Yes":
        sql  =  "SELECT * from pcs_data WHERE Room = ? and Box = ? and itest = ?"
        var = (room, box, itest)
    elif room and box and office == "office - Yes":
        sql  =  "SELECT * from pcs_data WHERE Room = ? and Box = ? and office = ?"
        var = (room, box, office)
    elif room and box and deepfreez == "DeepFreez - Yes":
        sql  =  "SELECT * from pcs_data WHERE Room = ? and Box = ? and deepfreez = ?"
        var = (room, box, deepfreez)
    elif box and itest =="Itest - Yes" and office == "office - Yes":
        sql  =  "SELECT * from pcs_data WHERE Box = ? and itest = ? and office = ?"
        var = (box, itest, office)
    elif box and office == "office - Yes" and deepfreez == "DeepFreez - Yes":
        sql  =  "SELECT * from pcs_data WHERE Box = ? and office = ? and deepfreez = ?"
        var = (box, office, deepfreez)
    elif deepfreez == "DeepFreez - Yes" and itest =="Itest - Yes" and office == "Office - Yes":
        sql  =  "SELECT * from pcs_data WHERE itest = ? and office = ?  and deepfreez = ?"
        var = (itest, office, deepfreez)
    elif room and box and status:
        sql  =  "SELECT * from pcs_data WHERE Room = ? and Box = ? and Status = ?"
        var = (room, box, status)


    elif room and box:
        sql= "SELECT * from pcs_data WHERE Room = ? and Box = ?"
        var = (room, box)
    elif room and status:
        sql= "SELECT * from pcs_data WHERE Room = ? and Status = ?"
        var = (room, status)
    elif room and itest =="Itest - Yes":
        sql  =  "SELECT * from pcs_data WHERE Room = ? and itest = ?"
        var = (room, itest)
    elif room and office == "Office - Yes":
        sql  =  "SELECT * from pcs_data WHERE Room = ? and office = ?"
        var = (room, office)
    elif room and deepfreez == "DeepFreez - Yes":
        sql  =  "SELECT * from pcs_data WHERE Room = ? and deepfreez = ?"
        var = (room, deepfreez)
    elif box and status:
        sql= "SELECT * from pcs_data WHERE Box = ? and Status = ?"
        var = (box, status)
    elif box and itest =="Itest - Yes":
        sql  =  "SELECT * from pcs_data WHERE Box = ? and itest = ?"
        var = (box, itest)
    elif box and office == "Office - Yes":
        sql  =  "SELECT * from pcs_data WHERE Box = ? and office = ?"
        var = (box, office)
    elif box and deepfreez == "DeepFreez - Yes":
        sql  =  "SELECT * from pcs_data WHERE Box = ? and deepfreez = ?"
        var = (box, deepfreez)
    elif status and room:
        sql= "SELECT * from pcs_data WHERE Room = ? and Status = ?"
        var = (room, status)
    elif  itest =="Itest - Yes" and office == "Office - Yes":
        sql  =  "SELECT * from pcs_data WHERE itest = ? and office = ?"
        var = (itest, office)
    elif itest =="Itest - Yes" and deepfreez == "DeepFreez - Yes":
        sql  =  "SELECT * from pcs_data WHERE itest = ? and deepfreez = ?"
        var = (itest, deepfreez)
    elif office == "Office - Yes" and deepfreez == "DeepFreez - Yes":
        sql  =  "SELECT * from pcs_data WHERE office = ? and deepfreez = ?"
        var = (office, deepfreez)


    elif room:
        sql  =  "SELECT * from pcs_data WHERE Room = ?"
        var = (room,)
    elif box:
        sql  =  "SELECT * from pcs_data WHERE Box = ?"
        var = (box,)
    elif itest =="Itest - Yes":
        sql  =  "SELECT * from pcs_data WHERE itest = ?"
        var = (itest,)
    elif office =="Office - Yes":
        sql  =  "SELECT * from pcs_data WHERE office = ?"
        var = (office,)
    elif deepfreez =="DeepFreez - Yes":
        sql  =  "SELECT * from pcs_data WHERE deepfreez = ?"
        var = (deepfreez,)
    elif status:
        sql  =  "SELECT * from pcs_data WHERE status = ?"
        var = (status,)


    else:
        sql = "SELECT * from pcs_data order by room"
        var = ()
        to_set_item == "No"

    filepath = "pcs_data.db"
    connection = sqlite3.connect(filepath)
    cursor = connection.cursor()
    print(sql)
    with connection:
        cursor.execute(sql, var)
        answer01 = cursor.fetchall()
        print(len(answer01))

    if connection:
        connection.close()

    if len(var) == 1 and not var == (pc_name,) and not len(answer01) == 1:
        results_for = var[0]
    elif var == ():
        results_for = "all Pc's"
    elif var == (pc_name,) and answer01 !=[]:
        print(answer01)
        results_for = f"Pc Name {answer01[0][1]}"
        full_details = "Yes Please"

    elif len(answer01) == 1:
        results_for = f"{var[0]}: Pc Name {answer01[0][1]}"
        full_details = "Yes Please"
    elif answer01 ==[]:
        results_for = var[0]
    else:
        results_for = var
    answers.configure(state='normal')
    answers.delete('1.0', tkinter.END)
    answers.insert("1.0", f"{len(answer01)} Results for {results_for}:\n")
    answers.configure(state='disabled')
    return answer01

def delete_text():
    answers.configure(state='normal')
    answers.delete('1.0', tkinter.END)
#    name.delete('1.0', tkinter.END)
#    location.delete('1.0', tkinter.END)
#    status_info.delete('1.0', tkinter.END)
#    comment_info.delete('1.0', tkinter.END)
    answers.configure(state='disabled')


def print_data():
    delete_text()
    answer01 = retrieve_data()
    print(full_details)
    x = float(2)
    if full_details != "Yes Please":
        answers.configure(state='normal')
        for item in answer01:
            answers.insert(x, f"{int(x-1)}:\t{item[1]}\t   {item[2]}\t\t{item[9]}\t{item[10]}\n")
            x += 1
        answers.configure(state='disabled')

    elif full_details == "Yes Please":
        item = answer01[0]
        set_item(item)
        #give full detail for 1 pc
        answers.configure(state='normal', font = ("Ariel", 10, "bold"))
        answers.insert(x, f"\nRoom: {item[2]}\n\nSoftware Installed: {item[4]}, {item[5]}, {item[6]}\n\nBox: {item[3]}\n\nStatus: {item[9]}\n\nComment: {item[10]}\n")
        answers.configure(state='disabled')
    try:
        if to_set_item == "Yes":
            set_item(item)
    except: pass

def set_item(item):
    clear()
    pc_name_entry.insert(0, item[1])
    room_combobox.set(item[2])
    box_combobox.set(item[3])

    itest_var.set(item[4])
    office_var.set(item[5])
    freez_var.set(item[6])

#    proccessor_combobox.set(item[7])
#    memory_combobox.set(item[8])
    status_combobox.set(item[9])
    comment_entry.insert(0, item[10])

def clear():
    pc_name_entry.delete(0, tkinter.END)
    room_combobox.set('')
    box_combobox.set('')
    status_combobox.set('')
    itest_var.set(0)
    office_var.set(0)
    freez_var.set(0)

#    proccessor_combobox.set('')
#    memory_combobox.set('')
    comment_entry.delete(0, tkinter.END)

def onclick(event):
    print_data()

def on_ctrl_s(event):
    enter_data()

def on_ctrl_z(event):
    undo()


def sql_to_excel():
    conn=sqlite3.connect(filepath)
    export_csv = fd.asksaveasfile(initialfile = "file", mode = "w", defaultextension=".csv", filetypes=(("CSV file", "*.csv"),("All Files", "*.*")))
    if export_csv:
        abs_path = os.path.abspath(export_csv.name)
        print(abs_path)
    try:

     # Export data into CSV file
      print ("Exporting data into CSV............")
      cursor = conn.cursor()
      cursor.execute("select * from pcs_data")
      with open(abs_path, "w", encoding = 'utf-8-sig') as csv_file:
          csv_writer = csv.writer(csv_file)
          csv_writer.writerow([i[0] for i in cursor.description])
          csv_writer.writerows(cursor)

      dirpath = os.getcwd() + "pcs_data.csv"
      print ("Data exported Successfully into {}".format(dirpath))
      delete_text()
      answers.configure(state='normal')
      answers.insert("1.0", "Data exported Successfully")
      answers.configure(state='disabled')
    except Error as e:
      print(e)

    # Close database connection
    finally:
      conn.close()

def csv_to_sql():
    x = 0
    item = []
    open_excel_txt = fd.askopenfilename(filetypes = (("test", "*.txt")
                                                         ,("Text files", "*.txt")
                                                         ,("All files", "*.*") ))
    print(open_excel_txt)
    if open_excel_txt:
        connection=sqlite3.connect(filepath)
        cursor = connection.cursor()
        answer = export_confirmation()
        if answer == True:
            cursor.execute('DROP TABLE pcs_data')
            creat_table()
            with open(open_excel_txt, encoding='utf16') as f:
                for line in f:
                    x+=1
                    if x > 1:
                        item = line.split("\t")
                        if int(x/2) != x/2:
                            print(item)
                            sql = 'INSERT INTO pcs_data(PC_Name, Room, Box, itest, office, deepfreez, status, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
                            val = (item[1], item[2], item[3], item[4], item[5], item[6], item[9], item[10])
                            with connection:
                                cursor.execute(sql,val)
                        else:
                            continue
    if connection:
        connection.close()

def send_to_printer():
    try:
        os.startfile(dirpath, "print")
    except:
        "Can't do it :-("

def backup_db():
    global on_load
    if on_load != 0:
        save_db_backup = fd.asksaveasfile(initialfile = "pcs_data_BACKUP", mode = "w", defaultextension=".db", filetypes=(("SQLLite file", "*.db"),("All Files", "*.*")))
        if save_db_backup:
            abs_path = os.path.abspath(save_db_backup.name)
            destanation = abs_path
            src = r"pcs_data.db"
            os.system(f"copy {src} {destanation}")
            delete_text()
            answers.configure(state='normal')
            answers.insert("1.0", f"Backup DB saved to {abs_path}")
            answers.configure(state='disabled')
    else:
        destanation = "pcs_data_BACKUP.db"
        src = r"pcs_data.db"
        os.system(f"copy {src} {destanation}")
        delete_text()
        answers.configure(state='normal')
        answers.insert("1.0", f"Backup DB saved - {destanation}")
        answers.configure(state='disabled')
        on_load +=1


def load_from_backup():
    src = r"pcs_data_BACKUP.db"
    destanation = r"pcs_data.db"
    os.system(f"copy {src} {destanation}")
    delete_text()
    c

def undo():
    connection = sqlite3.connect(filepath)
    cursor = connection.cursor()
    global database_undo_cach
    if  len(database_undo_cach) >= 1:
        #the previous database to undo. one step
        undo_data = database_undo_cach[-1]
        cursor.execute('DROP TABLE pcs_data')
        creat_table()
        for raw in undo_data:
            sql = 'INSERT INTO pcs_data(PC_Name, Room, Box, itest, office, deepfreez, status, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
            val = (raw[1], raw[2], raw[3], raw[4], raw[5], raw[6], raw[9], raw[10])
            with connection:
                cursor.execute(sql,val)
        if connection:
            connection.close()

        database_undo_cach = database_undo_cach[:-1]
        print_data()
    else:
        answers.configure(state='normal')
        answers.insert("1.0", f"No changes to undo\n\n")
        answers.configure(state='disabled')



def delete_confirmation(pc_to_delete):
    answer = askyesno(title='confirmation', message=f'Are you sure that you want to delete pc {pc_to_delete} from DB')
    print(answer)
    return answer

def export_confirmation():
    answer = askyesno(title='confirmation', message=f'Export from Excel will change the database. Are you sure?')
    print(answer)
    return answer

def room_combo_values(do_it):
    if do_it == "do it":
        with open("room.txt", 'r', encoding = 'utf-8-sig') as file:
            for item in file:
                value = item.strip()
                room_values.append(value)
    return room_values

def room_summery():
    room_sam_list = []
    connection = sqlite3.connect(filepath)
    cursor = connection.cursor()
    sql = "SELECT COUNT(Room) from pcs_data where Room = ?"
    for item in room_combo_values("dont"):
        var = (item,)
        with connection:
            cursor.execute(sql, var)
            summery01 = cursor.fetchall()
#            list = [item, summery01[0][0]]
            room_sam_list.append(summery01[0][0])
    connection.close()
    return room_sam_list

def room_pie_chart():
    def absolute_value(val):
        a  = np.round(val/100.*y.sum(), 0)
        return a

    room_values_heb = []
    room_sam_list = room_summery()
    for item in room_combo_values("dont"):
        room_values_heb.append(item[::-1])
    y = np.array(room_sam_list)
    mylabels = room_values_heb

    plt.pie(y, labels = mylabels, autopct=absolute_value)
#    plt.legend()
    plt.show()



#Two  lines to make our compiler able to draw:
#    plt.savefig(sys.stdout.buffer)
#    sys.stdout.flush()

def box_combo_values(do_it):
    if do_it == "do it":
        with open("box.txt", 'r', encoding = 'utf-8-sig') as file:
            for item in file:
                value = item.strip()
                box_values.append(value)
    return box_values

def box_summery():
    box_sam_list = []
    connection = sqlite3.connect(filepath)
    cursor = connection.cursor()
    sql = "SELECT COUNT(Box) from pcs_data where Box = ?"
    for item in box_combo_values("dont"):
        var = (item,)
        with connection:
            cursor.execute(sql, var)
            summery01 = cursor.fetchall()
            box_sam_list.append(summery01[0][0])
    connection.close()
    return box_sam_list

def box_pie_chart():
    def absolute_value(val):
        a  = np.round(val/100.*y.sum(), 0)
        return a
    box_sam_list = box_summery()
    box_values = box_combo_values("dont")
#    for item in box_combo_values("dont"):
#        box_values_heb.append(item[::-1])
    y = np.array(box_sam_list)
    mylabels = box_values


    plt.pie(y, labels = mylabels, autopct=absolute_value)
#    plt.legend()
    plt.show()


def on_close_app():
    window.destroy()

def rClicker(e):
    ''' right click context menu for all Tk Entry and Text widgets
    '''

    try:
        def rClick_Copy(e, apnd=0):
            e.widget.event_generate('<Control-c>')
        def rClick_Paste(e):
            e.widget.event_generate('<Control-v>')
        def rClick_Select_all(e):
            e.widget.event_generate('<Control-a>')
        def rSearch(e):
            e.widget.event_generate('<Control-c>')
            clipboard_value = window.clipboard_get()
#            clipboard_value  = pyperclip.paste()
            print(clipboard_value)
            clear()
            pc_name_entry.insert(0, clipboard_value)
            print_data()
        def rDelete(e):
            e.widget.event_generate('<Control-c>')
            clipboard_value = window.clipboard_get()
#            clipboard_value  = pyperclip.paste()
            print(clipboard_value)
            clear()
            pc_name_entry.insert(0, clipboard_value)
            delete_pc()
        e.widget.focus()

        nclst=[
               (' Search', lambda e=e: rSearch(e)),
               (' Delete', lambda e=e: rDelete(e)),
               (' Copy', lambda e=e: rClick_Copy(e)),
               (' Paste', lambda e=e: rClick_Paste(e)),
               (' Select All', lambda e=e: rClick_Select_all(e))
               ]

        rmenu = Menu(None, tearoff=0, takefocus=0)

        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd)

        rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")

    except TclError:
        print (' - rClick menu, something wrong')
        pass

    return "break"


window = tkinter.Tk()
window.title("Data Entry Form")
window.config(bg=backgroud_color)

window.bind('<Control-s>', on_ctrl_s)
window.bind('<Control-z>', on_ctrl_z)


frame00 = tkinter.Frame(window)
frame00.config(bg=backgroud_color)
frame00.grid(row= 0, column=0)

frame01 = tkinter.Frame(window)
frame01.config(bg=backgroud_color)
frame01.grid(row= 1, column=0)

frame02 = tkinter.Frame(window)
frame02.config(bg=backgroud_color, height = 150)
frame02.grid(row= 2, column=0)


#darca_logo
image1 = Image.open("logo01.png")
test = ImageTk.PhotoImage(image1)
label1 = tkinter.Label(frame00, image=test)
label1.image = test
label1.grid()

# Basic Info
basic_info_frame =tkinter.LabelFrame(frame01, text="מחשבים בבית הספר", font=('Arial', 12))
basic_info_frame.config(bg=backgroud_color, fg = font_color)
basic_info_frame.grid(row= 0, column=0, padx=20, pady=5)

first_name_label = tkinter.Label(basic_info_frame, text="שם מחשב")
first_name_label.config(bg=backgroud_color)
first_name_label.grid(row=0, column=2)

pc_name_entry = tkinter.Entry(basic_info_frame)
pc_name_entry.grid(row=1, column=2)
pc_name_entry.bind('<Return>', onclick)

room_label = tkinter.Label(basic_info_frame, text="מיקום")
room_label.config(bg=backgroud_color)
room_combobox = ttk.Combobox(basic_info_frame)
for value in room_combo_values("do it"):
   # Add itmes in combobox through Loop code
   room_combobox['values']= tuple(list(room_combobox['values']) + [str(value)])

room_label.grid(row=0, column=1)
room_combobox.grid(row=1, column=1, sticky='e')

box_label = tkinter.Label(basic_info_frame, text="מארז")
box_combobox = ttk.Combobox(basic_info_frame)
for value in box_combo_values("do it"):
   # Add itmes in combobox through Loop code
   box_combobox['values']= tuple(list(box_combobox['values']) + [str(value)])
box_label.grid(row=0, column=0)
box_combobox.grid(row=1, column=0)


software_check_box =tkinter.LabelFrame(frame01, text="תוכנות מותקנות\t\t\t\t       ", font=('Arial', 12))
software_check_box.config(bg=backgroud_color, fg = font_color)
software_check_box.grid(row= 1, column=0, padx=20, pady=5)

itest_var = tkinter.StringVar(value="Itest - No")
itest_check = tkinter.Checkbutton(software_check_box, text="Itest",
                                       variable=itest_var, onvalue="Itest - Yes", offvalue="Itest - No", bg = backgroud_color)
itest_check.grid(row=0, column=0)

office_var = tkinter.StringVar(value="Office - No")
office_check = tkinter.Checkbutton(software_check_box, text="Office",
                                       variable=office_var, onvalue="Office - Yes", offvalue="Office - No", bg = backgroud_color)
office_check.grid(row=0, column=1)

freez_var = tkinter.StringVar(value="DeepFreez - No")
freez_check = tkinter.Checkbutton(software_check_box, text="DeepFreez",
                                       variable=freez_var, onvalue="DeepFreez - Yes", offvalue="DeepFreez - No", bg = backgroud_color)
freez_check.grid(row=0, column=3)

hardware_check_box =tkinter.LabelFrame(frame01, text="Hardware", font=('Arial', 12))
hardware_check_box.config(bg=backgroud_color, fg = font_color)
hardware_check_box.grid(row= 2, column=0, padx=20, pady=5)

proccessor_label = tkinter.Label(hardware_check_box, text="Prossesor", bg = backgroud_color)
proccessor_combobox = ttk.Combobox(hardware_check_box, values=["I3", "I5", "Pentium"], state= 'disabled')
proccessor_label.grid(row=0, column=0)
proccessor_combobox.grid(row=1, column=0)

memory_label = tkinter.Label(hardware_check_box, text="Memory", bg = backgroud_color)
memory_combobox = ttk.Combobox(hardware_check_box, values=["2G", "4G", "8G"], state= 'disabled')
memory_label.grid(row=0, column=1)
memory_combobox.grid(row=1, column=1)

status_label = tkinter.Label(hardware_check_box, text="Status", bg = backgroud_color)
status_values = ["", "תקין", "לא תקין"]
status_combobox = ttk.Combobox(hardware_check_box, values = status_values)
status_combobox.current(1)
status_label.grid(row=0, column=2)
status_combobox.grid(row=1, column=2)

comment_label = tkinter.Label(hardware_check_box, text="Comment:", bg = backgroud_color)
comment_entry = tkinter.Entry(hardware_check_box, font = ('Arial', '8'), width=40)
comment_label.grid(row=2, column=0, padx=10, pady=5)
comment_entry.grid(row=2, column=1, columnspan = 2, padx=10, pady=5, sticky = "W")


button = tkinter.Button(frame01, text="Search", command= print_data, bg = button_color)
button.grid(row=3, column=0, sticky="news", padx=20, pady=1)

button = tkinter.Button(frame01, text="Clear Form", command= clear, bg = button_color)
button.grid(row=4, column=0, sticky="news", padx=20, pady=1)

#button = tkinter.Button(frame01, text="Save/Update", command= enter_data, bg = backgroud_color)
#button.grid(row=5, column=0, sticky="news", padx=20, pady=1)

#button = tkinter.Button(frame01, text="Delete PC", command= delete_pc, bg = backgroud_color)
#button.grid(row=6, column=0, sticky="news", padx=20, pady=1)

#results frame
info_table =tkinter.LabelFrame(frame02, text="Information", font = ('Arial', '10'))
info_table.config(bg=backgroud_color, fg = font_color)
info_table.grid(row= 0, column=0, padx=20, pady=5)

tkinter.Label(info_table, text="Index", width= 4,  bg = backgroud_color).grid(row=0, column=0)
tkinter.Label(info_table, text="Name",  width= 7, bg = backgroud_color).grid(row=0, column=1)
tkinter.Label(info_table, text="Location", width= 10, bg = backgroud_color).grid(row=0, column=2)
tkinter.Label(info_table, text="Status", width= 8, bg = backgroud_color).grid(row=0, column=3)
tkinter.Label(info_table, text="Comment", width= 8,  bg = backgroud_color).grid(row=0, column=4)

answers_frame = tkinter.Frame(info_table)
answers_frame.grid(row=1, column = 0, columnspan = 10)

answers = tkinter.Text(answers_frame, width=60,  height=12, font = ("Ariel", 10, "bold"))
answers.config(wrap='none')
answers.grid(row = 0, column = 0)
answers.bind('<Button-3>',rClicker, add='')

menubar = Menu(window)
window.config(menu = menubar)
options = Menu(menubar)
update = Menu(menubar)
charts = Menu(menubar)
menubar.add_cascade(menu = update, label = 'Update Data')
menubar.add_cascade(menu = options, label = 'Options')
menubar.add_cascade(menu = charts, label = 'Pie Charts')
update.add_command(label = 'Save/Update Pc Information <Ctrl s>', command = lambda: enter_data())
update.add_command(label = 'Delete PC from Database', command = lambda: delete_pc())
update.add_command(label = 'Undo <Ctrl z>', command = lambda: undo())
options.add_command(label = 'Export to Excel', command = lambda: sql_to_excel())
options.add_command(label = 'Import from Excel(*.txt)', command = lambda: csv_to_sql())
options.add_command(label = 'Backup Database', command = lambda: backup_db())
options.add_command(label = 'Load Backup Database', command = lambda: load_from_backup())
charts.add_command(label = 'Room Pie Chart', command = lambda: room_pie_chart())
charts.add_command(label = 'Box Pie Chart', command = lambda: box_pie_chart())

window.protocol("WM_DELETE_WINDOW", on_close_app)

creat_table()
backup_db()
pyperclip.copy('')
window.mainloop()
