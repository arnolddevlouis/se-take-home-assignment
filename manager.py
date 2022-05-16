import threading
from cooking_bot import CookingBot
from datetime import datetime, timedelta
import numpy as np

class Manager:
    def __init__(self):
        print("manager created")
        self.cooking_bots = []
        self.order_list = []
        self.vip_order_no = 100
        self.normal_order_no = 100
        self.vip_order_list = []
        self.normal_order_list = []
        self.completed_order_list = []
        self.condition = threading.Condition()
        self.manager_thread = threading.Thread(target=self.__manage_order)
        self.manager_thread.start()
        self.notify_work_done_lock = threading.Lock()
        
    def add_bot(self):
        self.condition.acquire()
        self.cooking_bots.insert(len(self.cooking_bots), CookingBot(len(self.cooking_bots),self.__notify_work_done))
        print("No of bot: "+ str(len(self.cooking_bots)))
        self.update_bot_callback(len(self.cooking_bots))
        self.condition.notify()
        self.condition.release()

    def remove_bot(self):
        if(self.cooking_bots):
            latest_bot = self.cooking_bots.pop()
            latest_bot.stop_bot()
            self.update_bot_callback(len(self.cooking_bots))
        print("Done remove")
    
    def get_vip_list(self):
        return self.vip_order_list
    
    def get_normal_list(self):
        return self.normal_order_list
    
    def get_completed_list(self):
        return self.completed_order_list

    def push_order(self, is_vip):
        self.condition.acquire()
        if is_vip:
            self.vip_order_no += 1
            work_id = "V" + str(self.vip_order_no)
            self.vip_order_list.insert(len(self.vip_order_list), [work_id,0])
        else:
            self.normal_order_no += 1
            work_id = "N" + str(self.normal_order_no)
            self.normal_order_list.insert(len(self.normal_order_list), [work_id,0])
        
        self.condition.release()
        self.__update_list()
        self.__notify_manager()

    def __update_list(self):
        self.condition.acquire()
        if(self.normal_order_list and self.vip_order_list):
            update_list = np.concatenate((self.vip_order_list, self.normal_order_list))
            self.update_pending_callback(update_list)
        else:
            if self.normal_order_list:
                self.update_pending_callback(self.normal_order_list)
            else:
                if self.vip_order_list:
                    self.update_pending_callback(self.vip_order_list)
                else:
                    self.update_pending_callback([])
        self.condition.release()      
                    
    def register_callback(self, state, callback):
        if (state == "PENDING"):
            self.update_pending_callback = callback
        else:   
            if (state == "COMPLETED"):
                self.update_completed_callback = callback
            else:    
                if (state == "BOTS"):
                    self.update_bot_callback = callback
        
    def __notify_manager(self):
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()
    
    def __notify_work_done(self, status, work_id):
        self.condition.acquire()
        if(work_id[0] == 'V'):
            for index,list in enumerate(self.vip_order_list):
                if(list[0] == work_id):
                    self.vip_order_list.pop(index) 
                    break
            if not status:
                self.vip_order_list.insert(0, [work_id,0])
        else:
            for index,list in enumerate(self.normal_order_list):
                if(list[0] == work_id):
                    self.normal_order_list.pop(index) 
                    break
            if not status:
                self.normal_order_list.insert(0, [work_id,0])

        if status:
            self.completed_order_list.insert(len(self.completed_order_list), work_id)
            self.update_completed_callback(self.completed_order_list)

        self.__update_list()
        self.condition.notify()
        self.condition.release()
        return status

    def __manage_order(self):
        print("starting order management...")
        while True:
            self.condition.acquire()
            self.condition.wait()
            for index, bot in enumerate(self.cooking_bots):
                if bot.is_bot_free():
                    if self.vip_order_list:
                        for item in self.vip_order_list:
                            if(item[1] == 0):
                                bot.assign_work(item[0])
                                item[1] = 1
                                break
                    else:
                        if self.normal_order_list:
                            for item in self.normal_order_list:
                                if(item[1] == 0):
                                    bot.assign_work(item[0])
                                    item[1] =1
                                    break
            self.condition.release()