# from main import read
import random
import datetime
import time
from cone import Cone
import queue
from lora_connection import lora
import abc
import queue
from sami import ConeCloud
import pytz
import concurrent.futures
import threading


class Brain:
    
    queue_cloud = queue.Queue()
    dispatch_num = 5 
    fi_timeZone = pytz.country_timezones['fi'][0]
    fi_tz = pytz.timezone(fi_timeZone)
    
    def __init__(self) -> None:
        self.lora = lora(init=True)
        self.cones = []
        self.id_address = {}
        self.address_id = {}
        self.start = time.time()
        self.test_address = [5, 8, 9, 3]
        self.picked_address = []
        self.senderid_queue = queue.Queue()
        self.senderid_queue.put(1)
        ## functions for sending the data
        self._dispatch_threads = [threading.Thread(target=Brain.sendCloud, name=f"dispatch{i}") for i in range(Brain.dispatch_num)]
        for thread in self._dispatch_threads:
            thread.start()
        

    
    def run(self):
        
        self._connect_cones(num=2)
        i = 1
        while True : # self.chrono() <= 3
            received_message =  self.lora.read() #self._read_test()
            if received_message :
                print(received_message)
                address, message =  self._preprare_message(received_message)
                
                messages_dic = self._message_types(message)
                if "S" in messages_dic:
                    print(f"address: {address}")
                    print(f"id: {self.address_id[address]}")
                   # print(self.address_id)
                    id = self.address_id[address]
                    next_cone_id = self._pick_cone(id)
                    print(self.id_address)
                    Brain.queue_cloud.put(ConeCloud(id,"SK518-202166FD01759B6E312-13", datetime.datetime.now(tz=Brain.fi_tz).strftime("%Y-%m-%d %H:%M:%S")))
                    self.send(next_cone_id, self.id_address[next_cone_id])

   
    
    def _preprare_message(self, data: str):
        if"=" in data:
            split_data = data.split(",")
            address = split_data[0].split("=")[1]
            return address, split_data[2]
        else:
            return "", ""
        
    def _message_types(self, message: str) -> dict:
        messages = {}
        split_message = message.split("*")
        for i in range(0,len(split_message) - 1, 2):
            messages[split_message[i]] = split_message[i + 1]
        
        return messages

        
    def _connect_cones(self, num: int):

        while len(self.cones) < num:
            received_message =  self.lora.read() #self._read()
            if received_message :
                print("received message:")
                print(received_message)
                address, messages = self._preprare_message(received_message)
                if "C" in  messages and address not in self.address_id :
                    self.cones.append(Cone(address, len(self.cones) + 1))
                    self.id_address[len(self.cones)] = address
                    self.address_id[address] = len(self.cones)
                    self.send(len(self.cones), address)
        
        print( "==={} Cones are connected ! ===".format(len(self.cones)))

    
    def _read(self):
        ip_i = random.randint(0,len(self.test_address) - 1)
        m =f"AT+RCV={self.test_address[ip_i]},5,C*on" 
        self.picked_address.append(self.test_address[ip_i])
        self.test_address.pop(ip_i)
        return m
    
    def _read_test(self):
        id = self.senderid_queue.get()
        message = f"AT+RCV={self.id_address[id]},5,S*on"
        self.senderid_queue.task_done()
        return message 

    
    def _pick_cone(self, cone_messenger_id: int):
        if cone_messenger_id < len(self.cones):
            return  cone_messenger_id + 1
        else:
            return 1
    
    def send(self, cone_id: int, cone_address: str):

        self.lora.send("connected", cone_address)
        print(" send message to: address:{}\tid:{} !".format(cone_address, cone_id))
        self.senderid_queue.put(cone_id)

    
    def chrono(self):
        return time.time() - self.start 

    @staticmethod
    def sendCloud():
        while True:
        
            #print("queue size before taking event: {}".format(Brain.queue_cloud.qsize()))
            event =  Brain.queue_cloud.get()
            if(event is None): # the condition is used when we send a terminating event s
                break
            #read(event)
            event.dispatched()
            #print("got an event {} let's sleep".format(event))
            #print("queue size bofre sleep: {}".format(Brain.queue_cloud.qsize()))
            #time.sleep(3)
            Brain.queue_cloud.task_done()
            #print("back again !")
            #print("queue size after sleep: {}".format(Brain.queue_cloud.qsize()))
        
    
    


   



a = Brain()
a.run()
Brain.queue_cloud.join()
for _ in range(Brain.dispatch_num): # add none event to close the thread
    Brain.queue_cloud.put(None)
    
# test_address = [5, 8, 9, 3]
# i  = 0
# while i < 20 :
#     i += 1
#     print(random.randint(0,len(test_address) - 1))

print("ended !!")
