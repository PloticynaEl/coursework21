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


def func_remove_one():
    x = my_tree.selection()[0]
    my_tree.delete(x)


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
        img = Image.open(filename_img)
        if img is None:
            showinfo(title='Could not open or find the image:',
                     message=filename_img)
        else:
            showinfo(title='Selected File',
                     message=filename_img)
            func_view_photo(img)
            Button(my_frame_but_2, text="Сканировать изображение", command=lambda: func_scan_img(filename_img)).grid(
                row=0,
                column=0)
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
        func_view_csv(filename_csv)


def func_view_photo(img):
    img = img.resize((472, 675), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel.config(image=img)
    panel.image = img


def func_view_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        read_list = list(reader)
        read_list2 = read_list[0]
        for i in range(0, len(read_list2)):
            print(read_list2[i])
        count = 0
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
ws.geometry('1600x800')

panel = Label(ws)
panel.place(x=50, y=50)

my_frame_text_before_tree = Frame(ws)

Label(my_frame_text_before_tree, text="Выберите необходимую категорию для изменения:").pack(side=LEFT)

my_frame_text_before_tree.grid(row=0, column=1, sticky=SW)

my_frame_tree = Frame(ws)
my_scrollbar_tree_y = Scrollbar(my_frame_tree, orient=VERTICAL)
my_scrollbar_tree_x = Scrollbar(my_frame_tree, orient=HORIZONTAL)

style = ttk.Style()
style.configure("Treeview",
                background="silver",
                foreground="black",
                rowheight=25,
                fieldbackground="silver")
style.map("Treeview", background=[('selected', 'green')])

my_tree = ttk.Treeview(my_frame_tree, height=13)

my_tree['columns'] = ('ID', 'Категория', 'Данные')
my_tree.column('#0', width=0, stretch=NO)
my_tree.column('ID', anchor=W, width=50, minwidth=50)
my_tree.column('Категория', anchor=W, minwidth=200)
my_tree.column('Данные', anchor=W, width=730)

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

my_frame_tree.grid(row=1, column=1, padx=0, pady=0, sticky=NW)

my_frame_text_before_list = Frame(ws)

Label(my_frame_text_before_list, text="Укажите подходящие данные для занесения в выбранную категорию:\n \
(для множественного выбора +ctrl)").pack(side=LEFT)

Button(my_frame_text_before_list, text="Взять выбранные элементы", command=select_all).pack(side=RIGHT, padx=20)

my_frame_text_before_list.grid(row=2, column=1, sticky=SW)

my_frame_listbox = Frame(ws)

my_listbox = Listbox(my_frame_listbox, width=89, selectmode=EXTENDED)
my_listbox.grid(row=0, column=0)

my_scrollbar_list_y = Scrollbar(my_frame_listbox, orient=VERTICAL)
my_scrollbar_list_x = Scrollbar(my_frame_listbox, orient=HORIZONTAL)

my_scrollbar_list_y.grid(row=0, column=1, sticky=NS)
my_scrollbar_list_x.grid(row=1, column=0, sticky=EW)

my_listbox.config(yscrollcommand=my_scrollbar_list_y.set, xscrollcommand=my_scrollbar_list_x.set)
my_scrollbar_list_y.config(command=my_listbox.yview)
my_scrollbar_list_x.config(command=my_listbox.xview)
my_frame_listbox.grid(row=3, column=1, sticky=NW)

my_frame_text_before_box = Frame(ws, width=90)

Button(my_frame_text_before_box, text="Обновить содержимое", command=func_update).pack(side=RIGHT)
my_frame_text_before_box.grid(row=4, column=1, sticky=SW)

my_frame_box = Frame(ws)

my_scrollbar_x2 = Scrollbar(my_frame_box, orient=HORIZONTAL)

Label(my_frame_box, text="№").grid(row=0, column=0)

Label(my_frame_box, text="Категория", width=20).grid(row=0, column=1)

Label(my_frame_box, text="Данные", width=60).grid(row=0, column=2)

entryIdText = StringVar()
entryNameText = StringVar()
entryDataText = StringVar()

id_box = Entry(my_frame_box, width=5, disabledbackground="white", disabledforeground="black", state='disabled',
               textvariable=entryIdText)
id_box.grid(row=1, column=0)

name_box = Entry(my_frame_box, width=20, disabledbackground="white", disabledforeground="black", state='disabled',
                 textvariable=entryNameText)
name_box.grid(row=1, column=1)

data_box = Entry(my_frame_box, width=64, textvariable=entryDataText)
data_box.grid(row=1, column=2)

my_scrollbar_x2.grid(row=2, column=2, sticky=EW)
data_box.config(xscrollcommand=my_scrollbar_x2.set)
my_scrollbar_x2.config(command=data_box.xview)

my_frame_box.grid(row=5, column=1, padx=0, pady=0, sticky=NW)


my_frame_but_1 = Frame(ws)

Button(my_frame_but_1, text="Открыть изображение", command=lambda: select_file(True)).grid(row=0, column=0)
Button(my_frame_but_1, text="Открыть .csv файл", command=lambda: select_file(False)).grid(row=0, column=1)

my_frame_but_1.grid(row=0, column=0, padx=90,  sticky=NW)


my_frame_but_2 = Frame(ws)

Button(my_frame_but_2, text='Сохранить', command=func_save).grid(row=0, column=1)

my_frame_but_2.grid(row=6, column=0)

ws.mainloop()