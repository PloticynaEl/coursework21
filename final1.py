from tkinter import *
from tkinter import ttk
import final1_module
import csv
from PIL import Image, ImageTk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

text = ['Страна:', 'Семейство:', 'Род:', 'Название вида:', 'Внутренний номер:', 'Коллектор/-ы:', 'Место сбора:',
        'Экология:', 'Высота н.у.м.:', 'Координаты сбора:', 'Дата сбора:', 'Автор определения:', 'Типовой статус:']


def func_fill_tree(value='-'):
    count = 0
    for i in text:
        my_tree.insert(parent='', index=END, iid=str(count), text='', values=(str(count), i, value))
        count += 1


def select_all():
    result = entryDataText.get()
    for item in my_listbox.curselection():
        result = result + str(my_listbox.get(item)) + ' '
    entryDataText.set(result)


def func_add_record():
    global count
    my_tree.insert(parent='', index=END, iid=str(count), text='', values=(count, name_box.get(), data_box.get()))
    count += 1
    name_box.delete(0, END)
    data_box.delete(0, END)


def func_remove_all():
    global count
    for record in my_tree.get_children():
        my_tree.delete(record)
        count = 0


def func_select(event):
    id_box.delete(0, END)
    name_box.delete(0, END)
    data_box.delete(0, END)
    # номер строки
    selected = my_tree.focus()
    # значение
    values = my_tree.item(selected, 'values')
    entryIdText.set(values[0])
    entryNameText.set(values[1])
    entryDataText.set(values[2])


def func_update():
    if entryIdText.get() and entryNameText.get():
        selected = my_tree.focus()
        my_tree.item(selected, text="", values=(entryIdText.get(), entryNameText.get(), entryDataText.get()))
    entryIdText.set("")
    entryNameText.set("")
    data_box.delete(0, END)


def func_save():
    file_name = fd.asksaveasfile(mode='w', defaultextension=".csv")
    if file_name is None:
        return
    with open(file_name.name, 'w', newline="") as text_file:
        writer = csv.writer(text_file)
        writer.writerow(func_insert())


def func_insert():
    insert_arr = []
    for items in my_tree.get_children():
        values = my_tree.item(items, 'values')
        insert_arr.append(values[2])
    return insert_arr


def select_file(choice):
    if choice:
        filetypes = (('images files', '*.jpg'),
                     ('All files', '*.*'))
        filename_img = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        if filename_img:
            img = Image.open(filename_img)
        else:
            img = None
        if img is None:
            showinfo(title='Could not open or find the image:',
                     message=filename_img)
        else:
            showinfo(title='Selected File',
                     message=filename_img)
            func_view_photo(img)
            ttk.Button(my_frame_but_2, text="Сканировать изображение",
                       command=lambda: func_scan_img(filename_img)).grid(row=0, column=0)
            func_fill_tree()
    else:
        filetypes = (('images files', '*.csv'),
                     ('All files', '*.*'))
        filename_csv = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        showinfo(title='Selected File',
                 message=filename_csv)
        if filename_csv:
            func_view_csv(filename_csv)


def func_view_photo(img):
    img = img.resize((int(new_width/2)-150, int(new_height)-100), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel.config(image=img)
    panel.image = img


def func_view_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        read_list = list(reader)
        read_list2 = read_list[0]
        count = 0
        func_remove_all()
        for i in text:
            my_tree.insert(parent='', index=END, iid=str(count), text='', values=(str(count), i, read_list2[count]))
            count += 1


def func_scan_img(filename_img):
    info_list, img = final1_module.main(filename_img)
    img_into = Image.fromarray(img)
    func_view_photo(img_into)
    for item in info_list:
        my_listbox.insert(END, item)


ws = Tk()
ws.title('OCR')
ws.config(background='#AFE1AF')
width_wind = ws.winfo_screenwidth()
height_wind = ws.winfo_screenheight()
ws.geometry('%sx%s' % (int(width_wind/1.3), int(height_wind/1.5)))
ws.resizable(width=False, height=False)

new_width = int(width_wind/1.3)

new_height = int(height_wind/1.5)

style = ttk.Style()
style.configure("Treeview",
                background="silver",
                foreground="black",
                rowheight=25,
                fieldbackground="silver")
style.configure('new.TFrame', background='#AFE1AF')
style.configure('new.TLabel', foreground="black", background="#AFE1AF")
# style.configure('.', font=('Helvetica', 12))
style.map("Treeview", background=[('selected', 'green')])
style.map('TButton',
          foreground=[('!active', 'white'),
                      ('pressed', 'white'),
                      ('active', 'black')],
          background=[('!active', '#008000'),
                      ('pressed', '#006400'),
                      ('active', 'white')]
          )

panel = ttk.Label(ws, style='new.TLabel', width=int(new_width/20)-25)
panel.grid(row=1, column=0, rowspan=4)

my_frame_text_before_tree = Frame(ws, background="white")

ttk.Label(my_frame_text_before_tree, style='new.TLabel',
          text="Выберите необходимую категорию для изменения:", width=int(new_width/20)).pack(side=LEFT)

my_frame_text_before_tree.grid(row=0, column=1, sticky=SW)

my_frame_tree = Frame(ws)
my_scrollbar_tree_y = Scrollbar(my_frame_tree, orient=VERTICAL)
my_scrollbar_tree_x = Scrollbar(my_frame_tree, orient=HORIZONTAL)

my_tree = ttk.Treeview(my_frame_tree, height=10)

my_tree['columns'] = ('ID', 'Категория', 'Данные')
my_tree.column('#0', width=0, stretch=NO)
my_tree.column('ID', anchor=W, width=50, minwidth=50)
my_tree.column('Категория', anchor=W, width=200, minwidth=200)
my_tree.column('Данные', anchor=W, width=int(new_width/2)-200, minwidth=int(new_width/2)-200)

my_tree.heading('#0', text='', anchor=CENTER)
my_tree.heading('ID', text='ID', anchor=CENTER)
my_tree.heading('Категория', text='Категория', anchor=CENTER)
my_tree.heading('Данные', text='Данные', anchor=CENTER)

my_tree.bind("<Double-1>", func_select)

my_scrollbar_tree_y.pack(side=RIGHT, fill=Y)
my_scrollbar_tree_x.pack(side=BOTTOM, fill=X)

my_tree.config(yscrollcommand=my_scrollbar_tree_y.set, xscrollcommand=my_scrollbar_tree_x.set)
my_scrollbar_tree_y.config(command=my_tree.yview)
my_scrollbar_tree_x.config(command=my_tree.xview)

my_tree.pack()

my_frame_tree.grid(row=1, column=1, sticky=NW)

my_frame_text_before_list = ttk.Frame(ws, style='new.TFrame', width=int(new_width/20))

ttk.Label(my_frame_text_before_list, style='new.TLabel',
          text="Укажите подходящие данные для занесения в выбранную категорию:").pack(side=TOP)
ttk.Label(my_frame_text_before_list, style='new.TLabel',
          text="(для множественного выбора +ctrl)").pack(side=LEFT)
ttk.Button(my_frame_text_before_list, text="Взять выбранные элементы", command=select_all).pack(side=RIGHT)

my_frame_text_before_list.grid(row=2, column=1, sticky=SW)

my_frame_listbox = ttk.Frame(ws, style='new.TFrame')

my_listbox = Listbox(my_frame_listbox, width=int(new_width/20), selectmode=EXTENDED)
my_listbox.grid(row=0, column=0)

my_scrollbar_list_y = Scrollbar(my_frame_listbox, orient=VERTICAL)
my_scrollbar_list_x = Scrollbar(my_frame_listbox, orient=HORIZONTAL)

my_scrollbar_list_y.grid(row=0, column=1, sticky=NS)
my_scrollbar_list_x.grid(row=1, column=0, sticky=EW)

my_listbox.config(yscrollcommand=my_scrollbar_list_y.set, xscrollcommand=my_scrollbar_list_x.set)
my_scrollbar_list_y.config(command=my_listbox.yview)
my_scrollbar_list_x.config(command=my_listbox.xview)
my_frame_listbox.grid(row=3, column=1, sticky=NW)

my_frame_text_before_box = ttk.Frame(ws, style='new.TFrame', width=new_width/2)
ttk.Label(my_frame_text_before_box, style='new.TLabel', text="Внесите при необходимости изменения в записи данных, \n \
после чего занесите их в таблицу:").pack(side=LEFT)
ttk.Button(my_frame_text_before_box, text="Обновить", command=func_update).pack(side=RIGHT, padx=10)
my_frame_text_before_box.grid(row=4, column=1, sticky=SW)

my_frame_box = ttk.Frame(ws, style='new.TFrame', width=new_width/2)

my_scrollbar_x2 = Scrollbar(my_frame_box, orient=HORIZONTAL)

ttk.Label(my_frame_box, style='new.TLabel', text="№").grid(row=0, column=0)

ttk.Label(my_frame_box, style='new.TLabel', text="Категория", width=20).grid(row=0, column=1)

ttk.Label(my_frame_box, style='new.TLabel', text="Данные", width=int(new_width/20)-30).grid(row=0, column=2)

entryIdText = StringVar()
entryNameText = StringVar()
entryDataText = StringVar()

id_box = Entry(my_frame_box, width=5, disabledbackground="white", disabledforeground="black", state='disabled',
               textvariable=entryIdText)
id_box.grid(row=1, column=0)

name_box = Entry(my_frame_box, width=20, disabledbackground="white", disabledforeground="black", state='disabled',
                 textvariable=entryNameText)
name_box.grid(row=1, column=1)

data_box = Entry(my_frame_box, width=int(new_width/20)-25, textvariable=entryDataText)
data_box.grid(row=1, column=2)

my_scrollbar_x2.grid(row=2, column=2, sticky=EW)
data_box.config(xscrollcommand=my_scrollbar_x2.set)
my_scrollbar_x2.config(command=data_box.xview)

my_frame_box.grid(row=5, column=1, pady=0, sticky=NW)


my_frame_but_1 = ttk.Frame(ws, style='new.TFrame')

ttk.Button(my_frame_but_1, text="Открыть изображение", width=int(new_width/50),
           command=lambda: select_file(True)).grid(row=0, column=0)
ttk.Button(my_frame_but_1, text="Открыть .csv файл", width=int(new_width/50),
           command=lambda: select_file(False)).grid(row=0, column=1)

my_frame_but_1.grid(row=0, column=0)


my_frame_but_2 = ttk.Frame(ws, style='new.TFrame', width=new_width/2)

ttk.Button(my_frame_but_2, text='Сохранить', width=int(new_width/50), command=func_save).grid(row=0, column=1)

my_frame_but_2.grid(row=5, column=0)

ws.mainloop()
