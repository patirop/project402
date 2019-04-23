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
        self.n=2
        self.itemlist = item
        
    def order(self):
        
        orders = np.zeros(len(self.itemlist), dtype={'names':('item','quantity'),'formats':('U10','i4')}) 
        
        tempname =[]
        tempquantity =[]
        for i in range(len(self.itemlist)): 
            quantity = random.randint(0,9)
            tempname.append(self.itemlist[i].name)
            tempquantity.append(quantity)
            self.producer.profit = self.producer.profit + ((math.pow(beta,self.n)*self.itemlist[i].price[0])*quantity)
        orders['item'] = tempname
        orders['quantity'] = tempquantity
        print(orders)
        self.producer.days.insert(0,orders)

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
        print(dc_orders)


        for count in range(len(dc_orders)):
            unit = unit + (dc_orders[count]['quantity']/self.itemlist[count].unit)
        

        self.producer[i].capacity =self.producer[i].capacity - unit
        
        if self.producer[i].capacity >=0 :
            print("yes")
            
            self.producer[i].order_queue.insert(0,[dc_orders,30,unit])
            for j in range(len(dc_orders)):
                self.profit = self.profit - ((math.pow(beta,self.producer[i].n)*self.itemlist[i].price[0])*dc_orders[j]['quantity'])                 
            # return 1    

        else :
            print("No!!!!")
            self.producer[i].capacity =self.producer[i].capacity + unit
            # return 0

    def response(self):
        dc_store = np.zeros(len(self.itemlist), dtype={'names':('item','quantity'),'formats':('U10','i4')}) 
        tempname =[]
        for count_item in range(len(self.itemlist)): 
            tempname.append(self.itemlist[count_item].name)               
        dc_store['item'] = tempname
        print(self.profit)
        if len(self.product_queue) >0: 
            # ถ้ามีของจาก supllier
            for i in range(len(self.product_queue)):
                # print(self.product_queue[i])
                for j in range(len(dc_store)):
                    dc_store[j]['quantity']=dc_store[j]['quantity'] + self.product_queue[i]['quantity'][j]
            self.product_queue.clear()
        print(dc_store)
        for i in range(len(self.consumer)):
            for j in range(len(dc_store)):
                dc_store[j]['quantity']=dc_store[j]['quantity'] - self.shop_queue[i][0]['quantity'][j]
        print(dc_store)
        for check in range(len(dc_store)):
            
            if dc_store[check]['quantity'] <0:
                self.gotomarket(dc_store)
                break
        print(self.profit)
        for i in range(len(self.consumer)):
            self.consumer[i].product_queue.insert(0,self.shop_queue[i].pop())

    def gotomarket(self,amount):
        print('market')       
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
            print('supplier')
            self.product_queue.pop()    
     


   

# class AllBusiness:
#     def reset_test(self):
#         self.itemA = Item('a',40)
#         self.itemB = Item('b',30)
#         self.itemC = Item('c',15)
#         self.itemlist = [self.itemA,self.itemB,self.itemC]
#         self.dc = Dc(self.itemlist)
#         self.shop_1 =Shop(self.itemlist)
#         self.shop_2 = Shop(self.itemlist)
#         self.shop_3 = Shop(self.itemlist)
#         self.supplier_1 = Supplier(2)
#         self.supplier_2 = Supplier(10)
#         self.supplier_3 = Supplier(2)
#         self.shop_1.Producer(self.dc)
#         self.shop_2.Producer(self.dc)
#         self.shop_3.Producer(self.dc)
#         self.supplier_1.Consumer(self.dc)
#         self.supplier_2.Consumer(self.dc)
#         self.supplier_3.Consumer(self.dc)
#         self.dc.Consumer([self.shop_1,self.shop_2,self.shop_3])
#         self.dc.Producer([self.supplier_1,self.supplier_2,self.supplier_3])
#         self.dc.generate_queue()
#     def order(self):
#         self.shop_1.order()
#         self.shop_2 .order()
#         self.shop_3.order()
#         self.dc.manage_order()
#         self.dc.order()
#     def process(self):
#         self.supplier_1.process()
#         self.supplier_2.process()
#         self.supplier_3.process()
#     def response(self):
#         self.supplier_1.response()
#         self.supplier_2.response()
#         self.supplier_3.response()
#         self.dc.response()


# a = item('a',40)
# b = item('b',30)
# c = item('c',15)


# dc = dc()
# shop_1 =Shop()
# shop_2 = Shop()
# shop_3 = Shop()
# supplier_1 = Supplier(2)
# supplier_2 = Supplier(10)
# supplier_3 = Supplier(2)
# item = [a,b,c]

# shop_1.Producer(dc)
# shop_2.Producer(dc)
# shop_3.Producer(dc)

# dc.Consumer([shop_1,shop_2,shop_3])
# dc.Producer([supplier_1,supplier_2,supplier_3])

# supplier_1.Consumer(dc)
# supplier_2.Consumer(dc)
# supplier_3.Consumer(dc)

# dc.generate_queue()
# x = AllBusiness()
# x.reset_test()
# for i in range(5) :
    
#     x.itemA.price_days(PRICE)

#     x.itemB.price_days(PRICE)
#     x.itemC.price_days(PRICE)

#     print("days")
#     x.order()
#     x.process()
#     x.response()


class FooEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    self.state = None
    self.done = False
    self.reward = 0
    self.min = 0
    self.max = 9
    self.cap1 = 2
    self.cap2 = 10
    self.cap3 = 2
    self._seed()
    self.low = np.array([1,
                        0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
                        ])
    self.high = np.array([1,
                        self.cap1,self.cap1,self.cap1,self.cap1,self.cap1,self.cap1,self.cap1,
                        self.cap2,self.cap2,self.cap2,self.cap2,self.cap2,self.cap2,self.cap2,
                        self.cap3,self.cap3,self.cap3,self.cap3,self.cap3,self.cap3,self.cap3,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
                        ])
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
        print('ooooo',temp[i])
        self.dc.order(temp[i],i)   
    self.process()
    self.response()

    self.reward =self.dc.profit
    

    self.state = np.array([self.supplier_1.capacity,self.supplier_2.capacity,self.supplier_3.capacity])
    
    # print(self.state)
    print('days',self.day)
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
    self.supplier_1 = Supplier(self.cap1)
    self.supplier_2 = Supplier(self.cap2)
    self.supplier_3 = Supplier(self.cap3)
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
    self.state = np.array([0,0,0]) 
    return np.array(self.state)
  def _render(self, mode='human', close=False):
    ...
  def order(self):
    self.shop_1.order()
    self.shop_2 .order()
    self.shop_3.order()
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