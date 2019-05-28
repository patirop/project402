import gym
from gym import error, spaces, utils
from gym.utils import seeding
import random
import datetime
import numpy as np  
import math   
from gym.envs.classic_control import rendering
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
        # self.n=2
        self.itemlist = item
        
    def order(self,index):
        
        orders = np.zeros(len(self.itemlist), dtype={'names':('item','quantity'),'formats':('U10','i4')}) 
        
        
        tempname =[]
        tempquantity = self.Constant_order(index)

        for i in range(len(self.itemlist)): 
            quantity = tempquantity[i]
            tempname.append(self.itemlist[i].name)
            # tempquantity.append(quantity)
            self.order_queue.append(quantity)
            # self.producer.shop_number = self.producer.shop_number + ((math.pow(beta,self.n)*self.itemlist[i].price[0])*quantity)
        orders['item'] = tempname
        orders['quantity'] = tempquantity
        # print('shop order',orders)
        # print(self.producer.profit)
        
        
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
            self.shop_number = self.shop_number + self.shop_queue[index_profit][0]['quantity']# คำนวณ สินค้าของ shop
        
        
    def order(self,quantity):

        x1 = quantity.split(" ")        
        action =[]
        for action_index in range(9):
            action.append(int(x1[action_index]))
        count_action = 0
        for i in range(len(self.producer)):
            
            check = 0
            unit= 0
            dc_orders = np.zeros(len(self.itemlist), dtype={'names':('item','quantity'),'formats':('U10','i4')}) 
            tempname =[]
            tempquantity =[]
            tempquantity = action[count_action:count_action+3]
            for count_item in range(len(self.itemlist)): 
                tempname.append(self.itemlist[count_item].name) 
            # print('-------------------------------------')
            dc_orders['item'] = tempname
            dc_orders['quantity'] = tempquantity
            # print('supplier',i,'dc order',dc_orders)
            
            for index_quantity in range(len(tempquantity)):
                if tempquantity[index_quantity] < 0:
                    check = 1
                    break
                # elif tempquantity[0] == 0 & tempquantity[1] == 0 & tempquantity[2] == 0:
                #     check =1
                #     break

            if check == 0:
                for count in range(len(dc_orders)):
                    unit = unit + (dc_orders[count]['quantity']/self.itemlist[count].unit)
                
                self.producer[i].capacity =self.producer[i].capacity - unit
                
                if self.producer[i].capacity >=0 :
                    print("yes")
                    # print('supplier',i,'capacity',self.producer[i].capacity)
                    
                    self.producer[i].order_queue.insert(0,[dc_orders,10,unit])

                    
                    self.supply_number = self.supply_number + dc_orders['quantity']# คำนวณสินค้า ของที่ส่งไปยัง supply
                    # for j in range(len(dc_orders)):
                    #     self.supply_number  = self.supply_number  + ((math.pow(beta,self.producer[i].n)*self.itemlist[i].price[0])*dc_orders[j]['quantity']) 
                    self.producer[i].cap.append(self.producer[i].capacity)  
                    
                    # print('-------------------------------------')
                    # return 1    

                else :
                    print("No!!!!")
                    # print('supplier',i,'capacity',self.producer[i].capacity)
                    
                    self.producer[i].capacity =self.producer[i].capacity + unit
                    self.producer[i].cap.append(self.producer[i].capacity)  
                    # print('-------------------------------------')
                    # return 0
            else :
                print("No!!!!")
                # print('supplier',i,'capacity',self.producer[i].capacity)
                self.producer[i].cap.append(self.producer[i].capacity)  
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
        # print('dc store from supply',dc_store)
        for i in range(len(self.consumer)):
            for j in range(len(dc_store)):
                dc_store[j]['quantity']=dc_store[j]['quantity'] - self.shop_queue[i][0]['quantity'][j]
        # print('dc store',dc_store)
        

        for check in range(len(dc_store)):
            
            if dc_store[check]['quantity'] <0:
                self.gotomarket(dc_store)
                break
        

        
        # คำนวณหากำไร รายวัน 
        self.profit = self.calculate(self.shop_number,2)  - self.market_number - self.calculate(self.supply_number,-1)

        print('shop ',self.calculate(self.shop_number,2))
        print('market',self.market_number)
        

        # print('shop',self.shop_number)
        # print('market',self.market_number)
        print('supply',self.calculate(self.supply_number,-1))
        print('profit',self.profit)
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
        # self.n = -1
    def process(self):
        if len(self.order_queue) >0 :
            for i in range(len(self.order_queue)):
                # print('supply order',self.order_queue[i][0],'delay',self.order_queue[i][1])
                self.order_queue[i][1] = self.order_queue[i][1] -1
                if self.order_queue[i][1] == -1:    
                    self.product_queue.insert(0,self.order_queue[i][0])
                    self.order_queue.pop()
                elif self.order_queue[i][1] == 0:
                     self.capacity = self.capacity + self.order_queue[i][2]
        
    def response(self):
        if len(self.product_queue) >0:
            self.consumer.product_queue.insert(0,self.product_queue[0])
            print('supplier')
            self.product_queue.pop()    
class AllBusiness:
    def reset_test(self):
        self.itemA = Item('a',1)
        self.itemB = Item('b',1)
        self.itemC = Item('c',1)
        self.itemlist = [self.itemA,self.itemB,self.itemC]
        self.dc = Dc(self.itemlist)
        self.shop_1 =Shop(self.itemlist)
        self.shop_2 = Shop(self.itemlist)
        self.shop_3 = Shop(self.itemlist)
        self.supplier_1 = Supplier(120)
        self.supplier_2 = Supplier(150)
        self.supplier_3 = Supplier(240)
        self.shop_1.Producer(self.dc)
        self.shop_2.Producer(self.dc)
        self.shop_3.Producer(self.dc)
        self.supplier_1.Consumer(self.dc)
        self.supplier_2.Consumer(self.dc)
        self.supplier_3.Consumer(self.dc)
        self.dc.Consumer([self.shop_1,self.shop_2,self.shop_3])
        self.dc.Producer([self.supplier_1,self.supplier_2,self.supplier_3])
        self.dc.generate_queue()
        self.days = 0
    def order(self):
        self.shop_1.order(0)
        self.shop_2 .order(1)
        self.shop_3.order(2)
        self.dc.manage_order()
        # self.dc.order()
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
            0: 120, 
            1: 150, 
            2: 240, 
        } 
    
        return switcher.get(argument, "nothing") 






x = AllBusiness()
for j in range(2):
    x.reset_test()
    for i in range(30) :

        x.days+=1
        x.itemA.price_days(PRICE)

        x.itemB.price_days(PRICE)
        x.itemC.price_days(PRICE)

        print("days",x.days)

        x.order()
        
        input_action = input('order ?')

        x.dc.order(input_action) 

        temp =[]
        temp = temp+[x.days]
        for supply in range(len(x.dc.producer)):
            if len(x.dc.producer[supply].cap) <7:
                sum =7-len(x.dc.producer[supply].cap)
                temp = temp + x.dc.producer[supply].cap
                for number in range(sum):
                    temp.append(x.numbers_to_strings(supply))
            else :
                temp = temp + x.dc.producer[supply].cap[x.days-7:x.days+1]
        
        for demand in range(len(x.dc.consumer)):
            if len(x.dc.consumer[demand].order_queue) < 21:
                sum = 21 - len(x.dc.consumer[demand].order_queue)
                temp = temp + x.dc.consumer[demand].order_queue
                for zero in range(sum):
                    temp.append(0)
            else :
                temp = temp + x.dc.consumer[demand].order_queue[(x.days-7)*3:(x.days*3)+1]
        # print('sum',sum)           
        # for count in range(len(x.shop_1.order_queue)):
        #     temp = temp+x.shop_1.order_queue[count]
        # print('state',temp)
        # print(x.dc.producer[0].cap)
        # print(x.supplier_2.cap)
        # print(x.supplier_3.cap)
        # print(x.shop_1.order_queue)
        # print(x.shop_2.order_queue) 
        # print(x.shop_3.order_queue) 
        x.process()
        x.response()
        print('reward',x.dc.profit)
        


  
