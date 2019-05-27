import gym
from gym import error, spaces, utils
from gym.utils import seeding
import random
import datetime
import numpy as np  
import math   
import socketio
import json

beta =2  
PRICE = 10

sio = socketio.Client()
sio.connect("http://localhost:8888")

class Item :
    def __init__(self,name,unit):
        self.name = name
        self.unit = unit
        self.price =list()

    def price_days(self,price):
        self.price.insert(0,price)

class Business :
    def Producer(self,producer):
        self.producer = producer

    def Consumer(self,consumer):
        self.consumer = consumer

class Shop(Business):
    def __init__(self,item):
        self.product_queue = list()
        self.order_queue = list()
        self.itemlist = item
        
    def order(self,index):
        
        orders = np.zeros(len(self.itemlist), dtype={'names':('item','quantity'),'formats':('U10','i4')}) 
        
        tempname =[]
        tempquantity =self.Constant_order(index)
        for i in range(len(self.itemlist)): 
            quantity = tempquantity[i]
            tempname.append(self.itemlist[i].name)
            self.order_queue.append(quantity)
        orders['item'] = tempname
        orders['quantity'] = tempquantity
        # print(orders)

        
        self.producer.days.insert(0,orders)

    def Constant_order(self,argument): 
        switcher = { 
            0: [3,4,5], 
            1: [4,5,6], 
            2: [7,8,9], 
        } 
        return switcher.get(argument, "nothing") 

class Dc(Business):
    def __init__(self,item):
        self.profit = 0
        self.shop_number = np.zeros(3)
        self.market_number = 0
        self.supply_number = np.zeros(3)
        self.product_queue = list()
        self.shop_queue = []
        self.days = list()
        self.n = 0
        self.itemlist = item
    def generate_queue(self):
        for i in range(len(self.consumer)):
            order_queue = list()
            self.shop_queue.append(order_queue)
    def manage_order(self):
        for consumer_i in range(len(self.shop_queue)):
            self.shop_queue[consumer_i].insert(0,self.days.pop())
            
        for index_profit in range(len(self.itemlist)):
            self.shop_number = self.shop_number + self.shop_queue[index_profit][0]['quantity']# คำนวณจำนวน สินค้าของ shop

    def order(self,action):
        # x1 = action.split(" ")        
        # quantity =[]
        # for action_index in range(9):
        #     quantity.append(int(x1[action_index]))
        count_action = 0      

        for i in range(len(self.producer)):
            check = 0
            unit= 0
            dc_orders = np.zeros(len(self.itemlist), dtype={'names':('item','quantity'),'formats':('U10','i4')}) 
            tempname =[]
            quantity = []
            quantity = action[count_action:count_action+3]

            for count_item in range(len(self.itemlist)): 

                tempname.append(self.itemlist[count_item].name)
    
            dc_orders['item'] = tempname
            dc_orders['quantity'] = quantity
            # print('supplier',i,'dc order',dc_orders)           
            for index_quantity in range(len(quantity)):
                if quantity[index_quantity] < 0:
                    check = 1
                    break

            if check == 0:
                for count in range(len(dc_orders)):
                    unit = unit + (dc_orders[count]['quantity']/self.itemlist[count].unit)
                

                self.producer[i].capacity =self.producer[i].capacity - unit
                
                if self.producer[i].capacity >=0 :
                    # print("yes") 
                    self.producer[i].order_queue.insert(0,[dc_orders,10,unit])
                    self.supply_number = self.supply_number + dc_orders['quantity']# คำนวณสจำนวนสินค้าที่ส่งไปยัง supply                    
                    self.producer[i].cap.append(self.producer[i].capacity)                
                    # return 1    

                else :
                    # print("No!!!!")
                    self.producer[i].capacity =self.producer[i].capacity + unit
                    self.producer[i].cap.append(self.producer[i].capacity)
                    # return 0
            else :
                # print("No!!!!")
                self.producer[i].cap.append(self.producer[i].capacity)
                # print('supplier',i,'capacity',self.producer[i].capacity)
                # print('profit',self.profit)
                # print('-------------------------------------')
            count_action+=3

    def response(self):
        dc_store = np.zeros(len(self.itemlist), dtype={'names':('item','quantity'),'formats':('U10','i4')}) 
        tempname =[]
        for count_item in range(len(self.itemlist)): 
            tempname.append(self.itemlist[count_item].name)               
        dc_store['item'] = tempname

        if len(self.product_queue) >0: 
            # ถ้ามีของจาก supllier
            for i in range(len(self.product_queue)):
                # print(self.product_queue[i])
                for j in range(len(dc_store)):
                    dc_store[j]['quantity']=dc_store[j]['quantity'] + self.product_queue[i]['quantity'][j]
            self.product_queue.clear()

        for i in range(len(self.consumer)):
            # ตัดของที่มีของบิลรายวัน เพื่อไปซื้อที่ตลาด
            for j in range(len(dc_store)):
                dc_store[j]['quantity']=dc_store[j]['quantity'] - self.shop_queue[i][0]['quantity'][j]


        for check in range(len(dc_store)):
            
            if dc_store[check]['quantity'] <0:
                self.gotomarket(dc_store)
                break

        # คำนวณหากำไร รายวัน 
        self.profit = self.calculate(self.shop_number,2)  - self.market_number - self.calculate(self.supply_number,-1)
        
        for i in range(len(self.consumer)):
            self.consumer[i].product_queue.insert(0,self.shop_queue[i].pop())
        self.shop_number = np.zeros(3)
        self.market_number = 0
        self.supply_number = np.zeros(3)

    def gotomarket(self,amount):
        # print('market')       
        for i  in range(len(amount)):
            if amount[i]['quantity'] <0 :
                # print(abs(amount[i]['quantity']))
                self.market_number = self.market_number + ((math.pow(beta,self.n)*self.itemlist[i].price[0])*abs(amount[i]['quantity']))
        return amount

    def calculate(self,order,setn):
        sum = 0
        for cal in range(len(self.itemlist)):
            sum =sum + ((math.pow(beta,setn)*self.itemlist[cal].price[0])*order[cal])
        return sum

class Supplier(Business):
    def __init__(self,capacity):
        self.capacity = capacity
        self.order_queue = list()
        self.product_queue = list()
        self.cap =list()
    def process(self):
        if len(self.order_queue) >0 :
            for i in range(len(self.order_queue)):
                # print(self.order_queue[i][0])
                self.order_queue[i][1] = self.order_queue[i][1] -1
                if self.order_queue[i][1] == -1:
                    self.product_queue.insert(0,self.order_queue[i][0])
                    self.order_queue.pop()
                elif self.order_queue[i][1] == 0:
                     self.capacity = self.capacity + self.order_queue[i][2]
        
    def response(self):
        if len(self.product_queue) >0:
            self.consumer.product_queue.insert(0,self.product_queue[0])
            # print('supplier')
            self.product_queue.pop()    



class FooEnv(gym.Env):
  metadata = {
    'render.modes': ['human', 'rgb_array'],
    'video.frames_per_second': 30}



  def __init__(self):
    # self.state = None
    self.done = False
    self.reward = 0
    self.min = 0
    self.max = 9
    self._seed()
    self.low = np.zeros(85)
    self.high = np.zeros(85)
    self.high[0] = 7
    self.high[1:8]=self.numbers_to_strings(0)
    self.high[8:15] = self.numbers_to_strings(1)
    self.high[15:22] = self.numbers_to_strings(2)
    self.high[22:] =self.max
    self.action_space = spaces.Box(low=self.min, high=self.max, shape=(9,), dtype=np.int32)
    self.observation_space = spaces.Box(low=self.low ,high=self.high , dtype=np.float32)
    self.profit = []
    

  def _step(self, action): 
    self.day+=1
    self.seven_day+=1
    self.itemA.price_days(PRICE)
    self.itemB.price_days(PRICE)
    self.itemC.price_days(PRICE)
    self.order()

    
    self.dc.order(action)  

    self.process()
    self.response()
    self.reward =self.dc.profit
    
    tempstate = []
    tempstate = tempstate+[self.seven_day]
    for supply in range(len(self.dc.producer)):
        if len(self.dc.producer[supply].cap) <7:
            sum =7-len(self.dc.producer[supply].cap)
            tempstate = tempstate + self.dc.producer[supply].cap
            for number in range(sum):
                tempstate.append(self.numbers_to_strings(supply))
        else :
            tempstate = tempstate + self.dc.producer[supply].cap[self.day-7:self.day+1]
    
    for demand in range(len(self.dc.consumer)):
        if len(self.dc.consumer[demand].order_queue) < 21:
            sum = 21 - len(self.dc.consumer[demand].order_queue)
            tempstate = tempstate + self.dc.consumer[demand].order_queue
            for zero in range(sum):
                tempstate.append(0)
        else :
            tempstate = tempstate + self.dc.consumer[demand].order_queue[(self.day-7)*3:(self.day*3)+1]

    self.state = np.array(tempstate)
    # print('day',self.day,'action',action)
    
    if self.day == 1000:
        print('action',action)
        print('reward',self.reward)
        print('state',self.state)
        print('days',self.day)

    if self.seven_day  == 7 :
        self.seven_day =0

    # return self.state, self.reward, self.done, {}
    
    return np.array(self.state), self.reward, self.done, {}

  def _seed(self, seed=None):
    self.np_random, seed = seeding.np_random(seed)
    return [seed]

  def _reset(self):
    self.itemA = Item('a',1)
    self.itemB = Item('b',1)
    self.itemC = Item('c',1)
    self.itemlist = [self.itemA,self.itemB,self.itemC]
    self.dc = Dc(self.itemlist)
    self.shop_1 =Shop(self.itemlist)
    self.shop_2 = Shop(self.itemlist)
    self.shop_3 = Shop(self.itemlist)
    self.supplier_1 = Supplier(130)
    self.supplier_2 = Supplier(160)
    self.supplier_3 = Supplier(250)
    self.shop_1.Producer(self.dc)
    self.shop_2.Producer(self.dc)
    self.shop_3.Producer(self.dc)
    self.supplier_1.Consumer(self.dc)
    self.supplier_2.Consumer(self.dc)
    self.supplier_3.Consumer(self.dc)
    self.dc.Consumer([self.shop_1,self.shop_2,self.shop_3])
    self.dc.Producer([self.supplier_1,self.supplier_2,self.supplier_3])
    self.dc.generate_queue()
    self.day = 0
    self.seven_day = 0
    self.state = np.zeros(85)
    self.state[1:8]= self.numbers_to_strings(0)
    self.state[8:15] = self.numbers_to_strings(1)
    self.state[15:22] = self.numbers_to_strings(2)
    return np.array(self.state)

  def _render(self, mode='human', close=False):
    """ test render"""
    # print("render: state ",self.state)
    data = []
    item1 = ['item1']
    item2 = ['item2'] 
    item3 = ['item3']     
    j = 22
    for i in range(7):
        item1.append(self.state[j]+self.state[j+21]+self.state[j+42])
        item2.append(self.state[j+1]+self.state[j+22]+self.state[j+43])
        item3.append(self.state[j+2]+self.state[j+23]+self.state[j+44])
        j += 3
    data.append(item1)
    data.append(item2)
    data.append(item3)

    data1 = []
    data2 = ['profit']
    
    su1 = ['supply1']
    su2 = ['supply2']
    su3 = ['supply3']

    self.profit.append(self.dc.profit)
    for i in range(7):
        # data2.append(self.profit[i])
        su1.append(self.state[i])
        # su2.append(self.state[i+7])
        # su3.append(self.state[i+14])
        su2.append(0)
        su3.append(0)
    print("su1", su1)
    data1.append(su1)
    data1.append(su2)
    data1.append(su3)

    # for i in self.profit:
    #     data2.append(i)
    # data2.append(self.dc.profit)
    # print(data1,"\n")
    data2.append(self.dc.profit)
    print(self.dc.profit)
    # print(self.profit)

    sio.emit('channel_b', json.dumps(data))
    sio.emit('channel_c', json.dumps(data1))
    sio.emit('channel_d', json.dumps(data2))

  def order(self):
    self.shop_1.order(0)
    self.shop_2 .order(1)
    self.shop_3.order(2)
    self.dc.manage_order()
  def process(self):
    self.supplier_1.process()
    self.supplier_2.process()
    self.supplier_3.process()
  def response(self):
    self.supplier_1.response()
    self.supplier_2.response()
    self.supplier_3.response()
    self.dc.response()
  def numbers_to_strings(self,argument): 
    switcher = { 
        0: 130, 
        1: 160, 
        2: 250, 
    } 

    return switcher.get(argument, "nothing") 