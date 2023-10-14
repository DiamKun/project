#импортирование нужных модулей
import tkinter as tk
from tkinter import ttk
import sqlite3

#класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    #функция главного экрана
    def init_main(self):
        #кнопка добавления контакта
        toolbar = tk.Frame(bg= '#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.add_img = tk.PhotoImage(file='./img/add.png')
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        #добавление всех столбцов
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'tel', 'email', 'price'), height=80, show='headings')
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('tel', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('price', width=150, anchor=tk.CENTER)
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Телефон')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('price', text='Заработная плата')
        
        self.tree.pack(side=tk.LEFT)

        #наложение иконок на кнопки
        self.update_img = tk.PhotoImage(file='./img/update.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.update_img, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.delete_img, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.search_img, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

    #использование класса открытия дочернего окна
    def open_dialog(self):
        Child()

    #использование функции добавления столбцов в базу данных
    def records(self, name, tel, email, price):
        self.db.insert_data(name, tel, email, price)
        self.view_records()

    #отображение данных из базы данных
    def view_records(self):
        self.db.cursor.execute('SELECT * FROM db')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

    #использование класса редактирования контакта
    def open_update_dialog(self):
        Update()

    #отображение редактирования контакта
    def update_records(self, name, tel, email, price):
        self.db.cursor.execute('''UPDATE db SET name=?, tel=?, email=? price=&WHERE id=?''', (name, tel, email, price, self.tree.set(self.tree.selection() [0], '#1')))
        self.db.conn.commit()
        self.view_records()

    #отображение удаление контакта
    def delete_records(self):
        for selection_items in self.tree.selection():
            self.db.cursor.execute('DELETE FROM db WHERE id=?', (self.tree.set(selection_items, '#1')))
        self.db.conn.commit()
        self.view_records()

    #использование класса поиска контакта
    def open_search_dialog(self):
        Search()

    #отображение поиска контакта
    def search_records(self, name):
        name = ('%' + name + "%")
        self.db.cursor.execute('SELECT * FROM db WHERE name LIKE ?', (name,))

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

#класс дочернего окна
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    #функция добавления
    def init_child(self):
        self.title('Добавить')
        self.geometry('400x220')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        #расположение кнопок
        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text='Телефон:')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text = 'E-mail:')
        label_sum.place(x=50, y=110)
        label_money = tk.Label(self, text = 'Заработная плата:')
        label_money.place(x=50, y=140)
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)
        self.entry_price = ttk.Entry(self)
        self.entry_price.place(x=200, y=140)
        self.btn_cancel = ttk.Button(self, text="Закрыть", command = self.destroy)
        self.btn_cancel.place(x=220, y=170)
        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=300, y=170)

        self.btn_ok.bind('<Button-1>', lambda event:
                         self.view.records(self.entry_name.get(),
                                           self.entry_email.get(),
                                           self.entry_tel.get(),
                                           self.entry_price.get()))
        
        
#класс для редактирования контактов
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db

    #функция редактирования контакта
    def init_edit(self):
        self.title('Редактирование контакта')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event:
                      self.view.update_records(self.entry_name.get(),
                                               self.entry_email.get(),
                                               self.entry_tel.get(),
                                               self.entry_price.get()))
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()

    #подгрузка данных в форму для редактирования
    def default_data(self):
        self.db.cursor.execute('SELECT * FROM db WHERE id=?', self.view.tree.set(self.view.tree.selection() [0], '#1'))
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row(1))
        self.entry_email.insert(0, row(2))
        self.entry_tel.insert(0, row(3))


#класс для окна поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app
    
    #функция окна поиска
    def init_search(self):
        self.title('Поиск контакта')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Имя:')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=100, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)
        
        btn_search = ttk.Button(self, text='Найти')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event:
                        self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

#класс для создания базы данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS db (
                id INTEGER PRIMARY KEY,
                name TEXT,
                tel TEXT,
                email TEXT,
                price TEXT
            )'''
        )
        self.conn.commit()

    #фунция добавления столбцов в базу данных
    def insert_data(self, name, tel, email, price):
        self.cursor.execute(
            '''INSERT INTO db(name, tel, email, price) VALUES(?, ?, ?, ?)''', (name, tel, email, price)
        )
        self.conn.commit()


#создание окон
if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников')
    root.geometry('865x550')
    root.resizable(False, False)
    root.mainloop()