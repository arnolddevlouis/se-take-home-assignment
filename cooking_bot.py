import threading
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

    def __notify_thread(self):
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()
    
    def __cooking_thread(self):
        while self.active:
            self.is_free = True
            self.condition.acquire()
            self.condition.wait()
            if(not self.active):
                print("Bot "+ str(self.id)+" exiting")
                return
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
        while (datetime.now() < end_time ):
            self.lock.acquire()
            if(not self.active):
                self.lock.release()
                return False
            self.lock.release()    
            time.sleep(0.2)
        print("Bot "+ str(self.id) +", Work "+self.work_id+": finished cooking")
        return True