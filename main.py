from concurrent.futures import thread
from operator import truediv
from os import stat
from tkinter import *

import tkinter
from tkinter import ttk
from manager import Manager

class UI:

    def __init__(self, manager):
        self.manager = manager
        self.manager.register_callback("PENDING", self.__update_pending)
        self.manager.register_callback("COMPLETED", self.__update_completed)
        self.manager.register_callback("BOTS", self.__update_bot_no)

        self.main = tkinter.Tk()
        self.main.title("McDonald's Auto Cooking Bot")
        self.main.minsize(300,300)
        self.main.maxsize(300,300)
        self.frame = ttk.Frame(self.main)
        self.frame.pack()
        self.vertical_scroll = Scrollbar(self.frame)
        self.vertical_scroll.pack(side=RIGHT, fill=Y)
        self.__create_list_box()
        self.__create_button()
        self.__create_bot_no()
        self.main.mainloop()

    def __create_list_box(self):
        self.pending_list = Text(self.main, height=17, width=20)
        self.pending_list.config(state=DISABLED)
        self.pending_label = Label(self.main, text='PENDING')
        self.completed_list = Text(self.main, height=17, width=20)
        self.completed_list.config(state=DISABLED)
        self.completed_label = Label(self.main, text='COMPLETED')
        self.pending_list.place(relx=0.25, rely=0.05, anchor='n')
        self.pending_label.place(relx=0.25, rely=0, anchor='n')
        self.completed_list.place(relx=0.75, rely=0.05, anchor='n')
        self.completed_label.place(relx=0.75, rely=0, anchor='n')

    def __update_pending(self, list):    
        self.pending_list.config(state=NORMAL)
        self.pending_list.delete(1.0, END)
        for item in list:
            self.pending_list.insert('end', item[0]+'\n')
        self.pending_list.config(state=DISABLED)

    def __update_completed(self, list):
        self.completed_list.config(state=NORMAL)
        self.completed_list.delete(1.0, END)
        for item in list:
            self.completed_list.insert('end', item+'\n')
        self.completed_list.config(state=DISABLED)

    def __update_bot_no(self, no):
        self.bot_no.config(state=NORMAL)
        self.bot_no.delete(1.0,END)
        self.bot_no.insert('end', "No of Bots: "+ str(no))
        self.bot_no.config(state=DISABLED)

    def __create_bot_no(self):
        self.bot_no = Text(self.main, height=1, width= 15)
        self.bot_no.insert('end', "No of Bots: 0")
        self.bot_no.place(relx=1.0, rely=1.0, x=-30, y=-70, anchor=SE)
        self.bot_no.config(state=DISABLED)
    
    def __create_button(self):
        self.add_normal_order_btn = Button(self.main, text="Add Normal Order", command=self.__add_normal_order)
        self.add_vip_order_btn = Button(self.main, text="Add VIP Order", command=self.__add_vip_order)
        self.add_bot_btn = Button(self.main, text="+ Bot", command=self.__add_bot)
        self.remove_bot_btn = Button(self.main, text="- Bot", command=self.__remove_bot)
        self.add_bot_btn.place(rely=1.0, relx=1.0, x=-10, y=-40, anchor=SE)
        self.remove_bot_btn.place(rely=1.0, relx=1.0, x=-10, y=-10, anchor=SE)
        self.add_normal_order_btn.place(rely=1.0, relx=0.5, x=0, y=-40, anchor=SE)
        self.add_vip_order_btn.place(rely=1.0, relx=0.5, x=0, y=-10, anchor=SE)

    def __add_normal_order(self):
        self.manager.push_order(False)

    def __add_vip_order(self):
        self.manager.push_order(True)

    def __add_bot(self):
        self.manager.add_bot()
    
    def __remove_bot(self):
        self.manager.remove_bot()

if __name__ == '__main__':
    ui = UI(Manager())