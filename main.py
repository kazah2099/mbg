# Импорт.
import tkinter
from tkinter import ttk
import sqlite3

# Основной класс.
class Main(tkinter.Frame):

    # Инициализация.
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # Главное окно.
    def init_main(self):

        # toolbar и его размещение.
        toolbar = tkinter.Frame(bg="#000000", bd=5)
        toolbar.pack(side=tkinter.LEFT, fill=tkinter.Y)

        # Treeview.
        self.tree = ttk.Treeview(self, columns=('ID', "SNP", "Telephone", "Email", "Salary"), height=45, show="headings")
        # Интерфейс колонок.
        self.tree.column("ID", width=30, anchor=tkinter.CENTER)
        self.tree.column("SNP", width=300, anchor=tkinter.CENTER)
        self.tree.column("Telephone", width=150, anchor=tkinter.CENTER)
        self.tree.column("Email", width=150, anchor=tkinter.CENTER)
        self.tree.column("Salary", width=150, anchor=tkinter.CENTER)

        # Названия.
        self.tree.heading("ID", text="ID")
        self.tree.heading("SNP", text="ФИО")
        self.tree.heading("Telephone", text="Номер телефона")
        self.tree.heading("Email", text="Электронная почта")
        self.tree.heading("Salary", text="Заработная плата")

        # Возможность пролистывать вниз.
        scroll = tkinter.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.tree.configure(yscrollcommand=scroll.set)

        # Вывод на экран.
        self.tree.pack(side=tkinter.LEFT)

        # Картинка для переменной ADDIMAGE.
        self.ADDIMAGE = tkinter.PhotoImage(file="./img/add.png")
        # Кнопка add и её размещение.
        btn_open_Add = tkinter.Button(toolbar, bg="#525252", bd=0, image=self.ADDIMAGE, command=self.open_add)
        btn_open_Add.pack(side=tkinter.TOP) 

        # Картинка для переменной DELETEIMAGE.
        self.DELETEIMAGE = tkinter.PhotoImage(file="./img/delete.png")

        # Кнопка delete и её размещение.
        btn_open_Delete = tkinter.Button(toolbar, bg="#525252", bd=0, image=self.DELETEIMAGE, command=self.delete_records)
        btn_open_Delete.pack(side=tkinter.TOP, pady=5) 
        
        # Картинка для переменной REDACTIMAGE.
        self.REDACTIMAGE = tkinter.PhotoImage(file="./img/redact.png")
        # Кнопка redact и её размещение.
        btn_open_Redact = tkinter.Button(toolbar, bg="#525252", bd=0, image=self.REDACTIMAGE, command=self.open_redact)
        btn_open_Redact.pack(side=tkinter.TOP, pady=5) 

        # Картинка для переменной SEARCHIMG.
        self.SEARCHIMAGE = tkinter.PhotoImage(file="./img/search.png")

        # Кнопка search и её размещение.
        btn_open_Redact = tkinter.Button(toolbar, bg="#525252", bd=0, image=self.SEARCHIMAGE, command=self.open_search)
        btn_open_Redact.pack(side=tkinter.TOP, pady=5) 

        # Кнопка обновления страницы:
        self.REFRESHIMAGE = tkinter.PhotoImage(file='./img/refresh.png')
        btn_Refresh = tkinter.Button(toolbar, bg="#525252", bd=0, image=self.REFRESHIMAGE, command=self.view_records)
        btn_Refresh.pack(side=tkinter.TOP, pady=5) # Размещение кнопки refresh.

    # Функция открытия окна add.
    def open_add(self):
        add_window()

    # Функция открытия окна redact.
    def open_redact(self):
        redact_window()

    # Функция открытия окна search.
    def open_search(self):
        search_window()

    # Добавление записи в бд.
    def records(self, SNP, Telephone, Email, Salary):
        self.db.insert_data(SNP, Telephone, Email, Salary)
        self.view_records()

    def view_records(self): # Вывод записей бд.
        self.db.cur.execute("""SELECT * FROM db""")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row)
                        for row in self.db.cur.fetchall()]
        
    # Для удаления записей.
    def delete_records(self):
        for selection_time in self.tree.selection():
            self.db.cur.execute("""DELETE FROM db WHERE ID = ?""",
                                (self.tree.set(selection_time, "#1")))
        self.db.con.commit()
        self.view_records()

    # Для редактирования записей.
    def redact_records(self, SNP, Telephone, Email, Salary):
        self.db.cur.execute("""UPDATE db SET SNP=?, Telephone=?,
                                Email=?, Salary=? WHERE ID = ?""",
                                (SNP, Telephone, Email, Salary, self.tree.set
                                 (self.tree.selection()[0], "#1")))
        self.db.con.commit()
        self.view_records()

    # Для поиска записей.
    def search_record(self,SNP):
        SNP = ('%' + SNP +'%',) # Запятая тут важна!
        self.db.cur.execute("""SELECT * FROM db WHERE SNP LIKE ?""", SNP)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', "end", values=row) for row in self.db.cur.fetchall()]


# Добавление функции add.
class add_window(tkinter.Toplevel):

    def __init__(self):
        super().__init__(root)
        self.init_add()
        self.view = app

    def init_add(self):
        self.title("Добавление сотрудника")
        self.geometry("400x300")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_SNP = tkinter.Label(self, text="ФИО:", fg="#000000")
        label_SNP.place(x=50, y=50)
        label_Telephone = tkinter.Label(self, text="Номер телефона:", fg="#000000")
        label_Telephone.place(x=50, y=80)
        label_Email = tkinter.Label(self, text="Электронная почта:", fg="#000000")
        label_Email.place(x=50, y=110)
        label_Salary = tkinter.Label(self, text="Заработная плата:", fg="#000000")
        label_Salary.place(x=50, y=140)

        label_info = tkinter.Label(self, text="Добавление сотрудника", fg="#000000", font="helvetica 14")
        label_info.place(x=60, y=15)
        
        self.entry_SNP = ttk.Entry(self, foreground="#000000")
        self.entry_SNP.place(x=200, y=50)
        self.entry_Telephone = ttk.Entry(self, foreground="#000000")
        self.entry_Telephone.place(x=200, y=80)
        self.entry_Email = ttk.Entry(self, foreground="#000000")
        self.entry_Email.place(x=200, y=110)
        self.entry_Salary = ttk.Entry(self, foreground="#000000")
        self.entry_Salary.place(x=200, y=140)

        self.btn_exit = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_exit.place(x=250, y=190)

        self.btn_confirm = ttk.Button(self, text="Подтвердить")
        self.btn_confirm.place(x=50, y=190)

        self.btn_confirm.bind("<Button-1>", lambda event: self.view.records
                              (self.entry_SNP.get(), self.entry_Telephone.get(),
                               self.entry_Email.get(), self.entry_Salary.get()))
        
# Добавление функции redact.
class redact_window(tkinter.Toplevel):

    def __init__(self):
        super().__init__(root)
        self.init_seacrh()
        self.view = app

    def init_seacrh(self):
        self.title("Изменение данных о сотруднике")
        self.geometry("400x300")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_SNP = tkinter.Label(self, text="ФИО:", fg="#000000")
        label_SNP.place(x=50, y=50)
        label_Telephone = tkinter.Label(self, text="Номер телефона:", fg="#000000")
        label_Telephone.place(x=50, y=80)
        label_Email = tkinter.Label(self, text="Электронная почта:", fg="#000000")
        label_Email.place(x=50, y=110)
        label_Salary = tkinter.Label(self, text="Заработная плата:", fg="#000000")
        label_Salary.place(x=50, y=140)
        

        label_info = tkinter.Label(self, text="Изменение данных о сотруднике", fg="#000000", font="helvetica 14")
        label_info.place(x=45, y=15)
        
        self.entry_SNP = ttk.Entry(self, foreground="#000000")
        self.entry_SNP.place(x=200, y=50)
        self.entry_Telephone = ttk.Entry(self, foreground="#000000")
        self.entry_Telephone.place(x=200, y=80)
        self.entry_Email = ttk.Entry(self, foreground="#000000")
        self.entry_Email.place(x=200, y=110)
        self.entry_Salary = ttk.Entry(self, foreground="#000000")
        self.entry_Salary.place(x=200, y=140)

        self.btn_exit = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_exit.place(x=250, y=190)

        self.btn_confirm = ttk.Button(self, text="Подтвердить")
        self.btn_confirm.place(x=50, y=190)

        self.btn_confirm.bind("<Button-1>", lambda event: self.view.redact_records
                              (self.entry_SNP.get(), self.entry_Telephone.get(),
                               self.entry_Email.get(), self.entry_Salary.get()))
        
# Добавление функции search.
class search_window(tkinter.Toplevel):

    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app
        self.grab_set()
        self.focus_set()

   
    def init_search(self):
       
        self.title("Поиск данных о сотруднике")
        self.geometry('400x300')
        self.resizable(False, False)

        
        label_info = tkinter.Label(self, text="Поиск данных о сотруднике", fg="#0066CC", font="helvetica 14")
        label_info.place(x=80, y=55)

       
        label_search = tkinter.Label(self, text="Поиск:")
        label_search.place(x=90, y=100)

        self.entry_search = ttk.Entry(self, foreground="#2489A8")
        self.entry_search.place(x=135, y=100, width=150)

        
        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=220, y=160)

        
        btn_search = ttk.Button(self, text="Поиск")
        btn_search.place(x=85, y=160)
        btn_search.bind("<Button-1>", lambda event:self.view.search_record
                                        (self.entry_search.get()))
        btn_search.bind("<Button-1>", lambda event:self.destroy(), add="+")
        

class DB:
    def __init__(self):
        # Подключение к базе данных.
        self.con = sqlite3.connect("db.db")
        self.cur = self.con.cursor()

        # Создание таблицы данных.
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS db(
            id INTEGER PRIMARY KEY NOT NULL,
            SNP TEXT NOT NULL,
            Telephone TEXT,
            Email TEXT,
            Salary INTEGER)""")

        # Сохранение базы данных.
        self.con.commit()

    # Функция для вставления новых данных в базу данных.
    def insert_data(self, SNP, Telephone, Email, Salary):
        self.cur.execute("""INSERT INTO db(SNP, Telephone, Email, Salary)
                         VALUES (?, ?, ?, ?)""",
                         (SNP, Telephone, Email, Salary))

        # Сохранение базы данных.
        self.con.commit()

if __name__ == "__main__":
    root = tkinter.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Список сотрудников компании")
    root.geometry("900x700")
    root.mainloop()