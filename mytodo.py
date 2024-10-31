from tkinter import *
from tkinter import ttk
import datetime
import os.path

# Определяем глобальные переменные которыми будем пользоваться
global editline # строка редактирования
global tree     # таблица
global addbtn      # кнопка
global donevar  

# Получаем кортеж
def get_task_from_line():
    todo = editline.get()
    if not todo:
        return (False, ())

    current_date = datetime.datetime.now()
    date = current_date.strftime('%d.%m.%y')
    done = "да" if donevar.get() else ""
    
    return (True, (date, todo, done))

# Заполнить данные
def set_task_to_line(task):
    clear_line()

    if task == new_task:
        return

    done = True if task[2] == "да" else False
    todo = task[1]
    
    donevar.set(done)
    editline.insert(0, todo)
    
# Очистить строку
def clear_line():
    editline.delete(0, END)
    donevar.set(False)

def get_selected_task():
    s = tree.selection()
    if not s:
        return (False, []);
    
    task = tree.item(s)["values"]
    if new_task == task:
        return (False, [])

    return (True, s)

# Нажатие на кнопку
def write_task():
    task = get_task_from_line()
    if not task[0]:
        return 

    s = get_selected_task()
    # проверям новый или старый элемент
    if s[0]:
        tree.item(s[1], values=task[1])
    else:
        tree.insert("", 1, values = task[1])
    clear_line()
    save_to_file("tasks")

# Созадем блок редактирования
def create_edit_frame():
    global editline
    global donevar
    global addbtn
    
    donevar = BooleanVar()  # done
    
    frame = ttk.Frame()
    editline = ttk.Entry(frame)
    editline.pack(side=LEFT, fill=X, expand=True)
    
    addbtn = ttk.Button(frame, text="Записать", command=write_task)
    addbtn.pack(side=RIGHT, padx=5)
    
    donecheck = ttk.Checkbutton(frame, text="", variable = donevar)
    donecheck.pack(side=RIGHT, padx=5)
    
    return frame

def create_tree_frame():
    global tree
    # определяем столбцы
    frame = ttk.Frame()
    columns = ("date", "todo", "done")
    tree = ttk.Treeview(frame, columns=columns, show="headings")
    tree.pack(side=LEFT, expand=True, fill=BOTH)
    
    # определяем заголовки
    tree.heading("date", text="Дата", anchor=W)
    tree.heading("todo", text="Что сделать", anchor=W)
    tree.heading("done", text="Сделано", anchor=W)
    
    tree.column("#1", stretch=NO, width=70)
    tree.column("#2", stretch=YES)
    tree.column("#3", stretch=NO, width=100)
    
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    return frame

# Выделяем данные
def item_selected(event):
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        task = item["values"]
        set_task_to_line(task)
        
def save_to_file(filename):
    with open(filename, 'w') as f:
        for item in tree.get_children():
            task = tree.item(item)["values"]
            if task == new_task:
                continue
            
            if len(task) < 3 or not task[2]:
                task[2] = "нет"

            print(task[0], task[1], task[2], sep='\t', file=f)

def load_from_file(filename):
    if not os.path.exists(filename):
        return

    with open(filename, 'r') as f:
        for line in f:
            task = line.strip().split('\t');
            if task[2] == 'нет':
                task[2] = ''
            tree.insert("", END, values=task)

# нажатие на Enter
def press_enter_key(event):
    addbtn.focus()
    write_task()
    
def press_edit_key(event):
    item_selected(event)
    editline.focus()

def press_done_toggle_key(event):
    donevar.set(not donevar.get())

def press_tree_focus(event):
    tree.focus()

root = Tk()
root.title("MyTodo by Lexius")
root.geometry("500x200")

create_edit_frame().pack(anchor=N, expand=False, fill=X, padx=5, pady=5)
create_tree_frame().pack(anchor=NW, expand=True, side=TOP, fill=BOTH)

# определяем данные для отображения
new_task = ["", "Новая задача" , ""]

# добавляем данные
tree.insert("", 0, values=new_task)

# загружаем из файла
load_from_file("tasks")
 
tree.bind("<<TreeviewSelect>>", item_selected)
tree.bind("<e>", press_edit_key)

editline.bind("<Return>", press_enter_key)
editline.bind("<Insert>", press_done_toggle_key)

root.mainloop()