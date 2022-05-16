from concurrent.futures import thread
from operator import truediv
from tkinter import *

import threading
import logging
import time
from datetime import datetime, timedelta

class CookingBot:
    def __init__(self, id, callback):
        self.id = id
        self.is_free = True
        self.active = True
        self.notify_work_done = callback
        self.condition = threading.Condition()
        self.lock = threading.Lock()
        self.work = threading.Thread(target=self.__cooking_thread)
        self.work.start()

    def register_callback(self, callback):
        self.notify_work_done = callback
    
    def get_id(self):
        return self.id

    def is_bot_free(self):
        return self.is_free

    def is_bot_active(self):
        return self.is_bot_active

    def assign_work(self, work_id):
        self.work_id = work_id
        self.__notify_thread()

    def stop_bot(self):
        self.lock.acquire()
        self.active = False
        self.lock.release()
        if(self.is_free):
            self.__notify_thread()
        self.work.join()

    def __notify_thread(self):
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()
    
    def __cooking_thread(self):
        while self.active:
            self.is_free = True
            self.condition.acquire()
            self.condition.wait()
            self.is_free = False
            
            if not self.active:
                break
            ret = self.__cook()
            if (not self.notify_work_done(ret, self.work_id)):
                break               
            self.condition.release()
        
        print("Bot "+ str(self.id) +", Work "+self.work_id+": exiting...")

    def __cook(self):
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=10)
        #print("Bot "+ str(self.id) +": start cooking")
        while (datetime.now() < end_time ):
            self.lock.acquire()
            if(not self.active):
                self.lock.release()
                return False
            self.lock.release()    
            time.sleep(0.2)
        print("Bot "+ str(self.id) +", Work "+self.work_id+": finished cooking")
        return True
    
class Manager:
    def __init__(self):
        print("manager created")
        self.cooking_bots = []
        self.order_list = []
        self.vip_order_no = 100
        self.vip_order_list = []
        self.normal_order_no = 100
        self.normal_order_list = []
        self.completed_order_list = []
        self.condition = threading.Condition()
        self.manager_thread = threading.Thread(target=self.__manage_order)
        self.manager_thread.start()
        self.notify_work_done_lock = threading.Lock()
        
    def add_bot(self, id):
        self.condition.acquire()
        self.cooking_bots.insert(len(self.cooking_bots), CookingBot(id,self.__notify_work_done))
        self.condition.notify()
        self.condition.release()

    def remove_bot(self, count):
        for x in range(count):
            latest_bot = self.cooking_bots.pop()
            latest_bot.stop_bot()
        print("Done remove")
    
    def push_order(self, is_vip):
        if is_vip:
            self.vip_order_no += 1
            work_id = "V" + str(self.vip_order_no)
            self.vip_order_list.insert(len(self.vip_order_list), work_id)
        else:
            self.normal_order_no += 1
            work_id = "N" + str(self.normal_order_no)
            self.normal_order_list.insert(len(self.normal_order_list), work_id)
        self.__notify_manager()
        
    def __notify_manager(self):
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()
    
    def __notify_work_done(self, status, work_id):
        self.condition.acquire()

        if status:
            self.completed_order_list.insert(len(self.completed_order_list), work_id)
        else:
            if(work_id[0] == 'V'):
                self.vip_order_list.insert(0, work_id)
            else:
                self.normal_order_list.insert(0, work_id)
        
        self.condition.notify()
        self.condition.release()
        return status

    def __manage_order(self):
        print("starting order management...")
        while True:
            self.condition.acquire()
            self.condition.wait()
            for bot in self.cooking_bots:
                if bot.is_bot_free():
                    if self.vip_order_list:
                        bot.assign_work(self.vip_order_list[0])
                        self.vip_order_list.pop(0)
                    else:
                        if self.normal_order_list:
                            bot.assign_work(self.normal_order_list[0])
                            self.normal_order_list.pop(0)
            self.condition.release()

if __name__ == '__main__':
    #cook = CookingBot(111)
    manager = Manager()
    #create 10 bots
    x = range(5)
    for id in x:
        manager.add_bot(id)

    for id in range(10):
        #if (bot.get_id() % 2) == 0:
        manager.push_order(True)

    for id in range(20):
        #if (bot.get_id() % 2) == 0:
        manager.push_order(False)
    
    time.sleep(25)

    for id in range(5):
        #if (bot.get_id() % 2) == 0:
        manager.push_order(True)
    

    #for bot in manager.cooking_bots:
    #   print(bot.get_id())


    #for bot in manager.cooking_bots:
        #print(bot.get_id() % 2)
        #if (bot.get_id() % 2) == 1:
           #print(bot.get_id())
    manager.remove_bot(2)

    #for bot in manager.cooking_bots:
    #    print(bot.get_id())
    #print("EXIT")
    #exit()

    time.sleep(20)
    manager.add_bot(11)
    manager.add_bot(12)



    

        
        