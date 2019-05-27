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
        self.tempquantity = []
        self.itemlist = item
        
    def order(self,index):
        
        orders = np.zeros(len(self.itemlist), dtype={'names':('item','quantity'),'formats':('U10','i4')}) 
        
        tempname =[]
        self.tempquantity =self.Constant_order(index)
        for i in range(len(self.itemlist)): 
            tempname.append(self.itemlist[i].name)

        orders['item'] = tempname
        orders['quantity'] = self.tempquantity
        # print('shop',orders['quantity'])

        
        self.producer.days.insert(0,orders)

    def Constant_order(self,argument): 
        switcher = { 
            0: [20],  # จำนวนการสั่งของ class shop เพราะทดลอง เป็น constant เลยกำหนด
            1: [0,0,0], 
            2: [0,0,0], 
        } 
        return switcher.get(argument, "nothing") 

class Dc(Business):
    def __init__(self,item):
        self.profit = 0
        self.reward_state = 0
        self.shop_number = np.zeros(1)
        self.market_number = 0
        self.supply_number = np.zeros(1)
        self.income_supply =0
        self.income_market =0
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

        for index_profit in range(len(self.shop_queue)):
            self.shop_number = self.shop_number + self.shop_queue[index_profit][0]['quantity']# คำนวณจำนวน สินค้าของ shop

    def order(self,action):
        x1 = action.split(" ")        
        quantity =[]
        for action_index in range(1):
            quantity.append(float(x1[action_index]))
     

        for i in range(len(self.producer)):
            check = 0
            unit= 0
            dc_orders = np.zeros(len(self.itemlist), dtype={'names':('item','quantity'),'formats':('U10','i4')}) 
            tempname =[]

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
                    self.producer[i].order_queue.insert(0,[dc_orders,1,unit]) # สั่งของ ไปยัง supply  1 = ค่า delay ที่จะได้รับของ 
                    self.supply_number = self.supply_number + dc_orders['quantity']# คำนวณสจำนวนสินค้าที่ส่งไปยัง supply 
               
                       

                else :
                    # print("No!!!!")
                    self.producer[i].capacity =self.producer[i].capacity + unit
                    self.producer[i].cap.append(self.producer[i].capacity)
                    # return 0
            else :
                # print("No!!!!")
                self.profit = -100
                self.producer[i].cap.append(self.producer[i].capacity)
                # print('supplier',i,'capacity',self.producer[i].capacity)

                # print('-------------------------------------')


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
            self.income_supply=dc_store['quantity'][0]
            # print('supply',dc_store['quantity'][0])
            self.product_queue.clear()
        else :
            # print('supply',dc_store['quantity'][0])
            self.income_supply = 0
        for i in range(len(self.consumer)):
            # ตัดของที่มีของบิลรายวัน เพื่อไปซื้อที่ตลาด
            for j in range(len(dc_store)):
                dc_store[j]['quantity']=dc_store[j]['quantity'] - self.shop_queue[i][0]['quantity'][j]


        for check in range(len(dc_store)):
            
            if dc_store[check]['quantity'] <0:
                self.gotomarket(dc_store)
                break
            else :
                self.income_market =0

        # คำนวณหากำไร รายวัน 
        if self.profit >= 0:
            self.profit = self.calculate(self.shop_number,2)  -   ( self.market_number+ self.calculate(self.supply_number,-1))
        
        
        for i in range(len(self.consumer)):
            self.consumer[i].product_queue.insert(0,self.shop_queue[i].pop())
        self.shop_number = np.zeros(1)
        self.market_number = 0
        self.supply_number = np.zeros(1)

    def gotomarket(self,amount):
               
        for i  in range(len(amount)):
            if amount[i]['quantity'] <0 :
                # print(abs(amount[i]['quantity']))
                self.market_number = self.market_number + ((math.pow(beta,self.n)*self.itemlist[i].price[0])*abs(amount[i]['quantity']))
        # print('market',amount[0]['quantity'])
        self.income_market =abs(amount[0]['quantity'])
        return amount

    def calculate(self,order,setn):
        sum = 0
        for cal in range(len(self.itemlist)):
            sum =sum + ((math.pow(beta,setn)*self.itemlist[cal].price[0])*order[0])
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
        
        self.low = np.ones(3)
        self.high = np.ones(3)
        # self.high[0:] = 9
        # self.high[1]=5
        
        
        self.action_space = spaces.Box(low=self.min, high=self.max, shape=(1,), dtype=np.float32)
        # self.action_space = spaces.Box(low=self.min, high=self.max, shape=(1,), dtype=np.float32)
        self.observation_space = spaces.Box(low=self.low ,high=self.high , dtype=np.float32)

        self.seed()

    def step(self, action): 
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
        tempstate = tempstate+[float(self.shop_1.tempquantity[0])]+[float(self.dc.income_supply)]+[float(self.dc.income_market)]
        
        
        self.state = np.array(tempstate) #  state ตอนนี้ มี [5,5,5] ค่าของ จำนวน การสั่งของ shop ของ [ อดีต, ปัจจุบัน , อนาคต ] แต่เพราะทดลอง เป็น constant g]
        print('day',self.day,'action',action)

        if self.day == 100 or self.day ==101:
            # print('dc_store',dc_store['quantity'][0])
            print(f'\nstate : {self.state} / action : {action} / reward: {self.reward}\n')

            

        if self.seven_day  == 7 :
            self.seven_day =0

    # return self.state, self.reward, self.done, {}

        print('reward',self.reward)


        return np.array(self.state), self.reward, self.done, {}

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def reset(self):
        self.itemA = Item('a',1)
        self.itemB = Item('b',1)
        self.itemC = Item('c',1)
        self.itemlist = [self.itemA]
        self.dc = Dc(self.itemlist)
        self.shop_1 =Shop(self.itemlist)
        # self.shop_2 = Shop(self.itemlist)
        # self.shop_3 = Shop(self.itemlist)
        self.supplier_1 = Supplier(100)
        # self.supplier_2 = Supplier(1000)
        # self.supplier_3 = Supplier(1000)
        self.shop_1.Producer(self.dc)
        # self.shop_2.Producer(self.dc)
        # self.shop_3.Producer(self.dc)
        self.supplier_1.Consumer(self.dc)
        # self.supplier_2.Consumer(self.dc)
        # self.supplier_3.Consumer(self.dc)
        self.dc.Consumer([self.shop_1])
        self.dc.Producer([self.supplier_1])
        self.dc.generate_queue()
        self.day = 0
        self.seven_day = 0
        self.state = np.zeros(3)
        
        
        return np.array(self.state)
    def render(self, mode='human', close=False):
        """ test render"""
        print(self.state)
    def order(self):
        self.shop_1.order(0)
        # self.shop_2 .order(1)
        # self.shop_3.order(2)
        self.dc.manage_order()
    def process(self):
        self.supplier_1.process()
        # self.supplier_2.process()
        # self.supplier_3.process()
    def response(self):
        self.supplier_1.response()
        # self.supplier_2.response()
        # self.supplier_3.response()
        self.dc.response()
    def numbers_to_strings(self,argument): 
        switcher = { 
            0: 100, 
            # 1: 1000, 
            # 2: 1000, 
        } 

        return switcher.get(argument, "nothing") 
 

f= open('randomforest.txt','r')
message = f.read()
lst = message.split()
lst[0] = lst[0][1:]
lst[-1] = lst[-1][:-1]



x = FooEnv()
for j in range(1):
    x.reset()
    for i in range(len(lst)) :

        
        # x.seven_days +=1




        
        # input_action = input('order ?')

        x.step(lst[i]) 

