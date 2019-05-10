import gym
from gym import error, spaces, utils
from gym.utils import seeding
import random
import datetime
import numpy as np  
import math   
beta =2  
PRICE = 10

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
        self.n=2
        self.itemlist = item
        
    def order(self,index):
        
        orders = np.zeros(len(self.itemlist), dtype={'names':('item','quantity'),'formats':('U10','i4')}) 
        
        tempname =[]
        tempquantity =self.Constant_order(index)
        for i in range(len(self.itemlist)): 
            quantity = tempquantity[i]
            tempname.append(self.itemlist[i].name)
            # tempquantity.append(quantity)
            self.order_queue.append(quantity)
            self.producer.profit = self.producer.profit + ((math.pow(beta,self.n)*self.itemlist[i].price[0])*quantity)
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
    def order(self,quantity,i):

        # for i in range(len(self.producer)):
        unit= 0
        dc_orders = np.zeros(len(self.itemlist), dtype={'names':('item','quantity'),'formats':('U10','i4')}) 
        tempname =[]
        # tempquantity =[]
        for count_item in range(len(self.itemlist)): 
            # quantity = random.randint(5,20) # ai 
            tempname.append(self.itemlist[count_item].name)
            # tempquantity.append(quantity)     
        dc_orders['item'] = tempname
        dc_orders['quantity'] = quantity
        # print(dc_orders)


        for count in range(len(dc_orders)):
            unit = unit + (dc_orders[count]['quantity']/self.itemlist[count].unit)
        

        self.producer[i].capacity =self.producer[i].capacity - unit
        
        if self.producer[i].capacity >=0 :
            # print("yes")
            
            self.producer[i].order_queue.insert(0,[dc_orders,30,unit])
            for j in range(len(dc_orders)):
                self.profit = self.profit - ((math.pow(beta,self.producer[i].n)*self.itemlist[i].price[0])*dc_orders[j]['quantity'])  
            self.producer[i].cap.append(self.producer[i].capacity)                
            # return 1    

        else :
            # print("No!!!!")
            self.producer[i].capacity =self.producer[i].capacity + unit
            self.producer[i].cap.append(self.producer[i].capacity)
            # return 0

    def response(self):
        dc_store = np.zeros(len(self.itemlist), dtype={'names':('item','quantity'),'formats':('U10','i4')}) 
        tempname =[]
        for count_item in range(len(self.itemlist)): 
            tempname.append(self.itemlist[count_item].name)               
        dc_store['item'] = tempname
        # print(self.profit)
        if len(self.product_queue) >0: 
            # ถ้ามีของจาก supllier
            for i in range(len(self.product_queue)):
                # print(self.product_queue[i])
                for j in range(len(dc_store)):
                    dc_store[j]['quantity']=dc_store[j]['quantity'] + self.product_queue[i]['quantity'][j]
            self.product_queue.clear()
        # print(dc_store)
        for i in range(len(self.consumer)):
            for j in range(len(dc_store)):
                dc_store[j]['quantity']=dc_store[j]['quantity'] - self.shop_queue[i][0]['quantity'][j]
        # print(dc_store)
        for check in range(len(dc_store)):
            
            if dc_store[check]['quantity'] <0:
                self.gotomarket(dc_store)
                break
        # print(self.profit)
        for i in range(len(self.consumer)):
            self.consumer[i].product_queue.insert(0,self.shop_queue[i].pop())

    def gotomarket(self,amount):
        # print('market')       
        for i  in range(len(amount)):
            if amount[i]['quantity'] <0 :
                # print(abs(amount[i]['quantity']))
                self.profit = self.profit - ((math.pow(beta,self.n)*self.itemlist[i].price[0])*abs(amount[i]['quantity']))
        return amount

class Supplier(Business):
    def __init__(self,capacity):
        self.capacity = capacity
        self.order_queue = list()
        self.product_queue = list()
        self.cap =list()
        self.n = -1
    def process(self):
        if len(self.order_queue) >0 :
            for i in range(len(self.order_queue)):
                # print(self.order_queue[i][0])
                self.order_queue[i][1] = self.order_queue[i][1] -1
                if self.order_queue[i][1] == -1:
                    self.capacity = self.capacity + self.order_queue[i][2]
                    self.product_queue.insert(0,self.order_queue[i][0])
                    self.order_queue.pop()
        
    def response(self):
        if len(self.product_queue) >0:
            self.consumer.product_queue.insert(0,self.product_queue[0])
            # print('supplier')
            self.product_queue.pop()    



class FooEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    self.state = None
    self.done = False
    self.reward = 0
    self.min = 0
    self.max = 9
    self._seed()
    self.low = np.zeros(85)
    self.high = np.zeros(85)
    self.high[0] = 730
    self.high[1:8]=self.numbers_to_strings(0)
    self.high[8:15] = self.numbers_to_strings(1)
    self.high[15:22] = self.numbers_to_strings(2)
    self.high[22:] =self.max
    self.action_space = spaces.Box(low=self.min, high=self.max, shape=(9,), dtype=np.int32)
    self.observation_space = spaces.Box(low=self.low ,high=self.high , dtype=np.float32)
    
    

  def _step(self, action): 
    self.day+=1
    self.itemA.price_days(PRICE)
    self.itemB.price_days(PRICE)
    self.itemC.price_days(PRICE)
    self.order()
    temp = []
    count = 0
    for x in range(3):
        temp.append(action[count:count+3])
        count+=3

    for i in range(len(self.dc.producer)):
        # print('ooooo',temp[i])
        self.dc.order(temp[i],i)   
    self.process()
    self.response()
    self.reward =self.dc.profit
    tempstate = []
    tempstate = tempstate+[self.day]
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
    
    print(self.state)
    # print('days',self.day)
    # return self.state, self.reward, self.done, {}
    return np.array(self.state), self.reward, self.done, {}

  def _seed(self, seed=None):
    self.np_random, seed = seeding.np_random(seed)
    return [seed]

  def _reset(self):
    self.itemA = Item('a',40)
    self.itemB = Item('b',30)
    self.itemC = Item('c',15)
    self.itemlist = [self.itemA,self.itemB,self.itemC]
    self.dc = Dc(self.itemlist)
    self.shop_1 =Shop(self.itemlist)
    self.shop_2 = Shop(self.itemlist)
    self.shop_3 = Shop(self.itemlist)
    self.supplier_1 = Supplier(2)
    self.supplier_2 = Supplier(10)
    self.supplier_3 = Supplier(2)
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
   
    self.state = np.zeros(85)
    self.state[1:8]= self.numbers_to_strings(0)
    self.state[8:15] = self.numbers_to_strings(1)
    self.state[15:22] = self.numbers_to_strings(2)
    return np.array(self.state)
  def _render(self, mode='human', close=False):
    ...
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
        0: 2, 
        1: 10, 
        2: 2, 
    } 

    return switcher.get(argument, "nothing") 