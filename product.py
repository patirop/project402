import random
import datetime
import numpy as np  
import math   
beta =2          
class item :
    def __init__(self,name,unit):
        self.name = name
        self.unit = unit
        self.price =list()

    def price_days(self,price):
        self.price.insert(0,price)

class business :
    def Producer(self,producer):
        self.producer = producer

    def Consumer(self,consumer):
        self.consumer = consumer

class shop(business):
    def __init__(self):
        self.product_queue = list()
        self.n=2
        
    def order(self):
        orders = np.zeros(len(item), dtype={'names':('item','quantity'),'formats':('U10','i4')}) 
        tempname =[]
        tempquantity =[]
        for i in range(len(item)): 
            quantity = random.randint(5,20)
            tempname.append(item[i].name)
            tempquantity.append(quantity)
            self.producer.profit = self.producer.profit + ((math.pow(beta,self.n)*item[i].price[0])*quantity)
        orders['item'] = tempname
        orders['quantity'] = tempquantity
        print(orders)
        self.producer.days.insert(0,orders)

class dc(business):
    def __init__(self):
        self.profit = 0
        self.product_queue = list()
        self.shop_queue = []
        self.days = list()
        self.n = 0
    def generate_queue(self):
        for i in range(len(self.consumer)):
            order_queue = list()
            self.shop_queue.append(order_queue) 
    def order(self):
        
        for i in range(len(self.producer)):
            unit= 0
            self.shop_queue[i].insert(0,self.days.pop())  
    
            for count in range(self.shop_queue[i][0].size):
                unit = unit + (self.shop_queue[i][0]['quantity'][count]/item[count].unit)
               
            self.producer[i].capacity =self.producer[i].capacity - unit
            if self.producer[i].capacity >=0 :
                print("yes")

                self.producer[i].order_queue.insert(0,[self.shop_queue[i][0],3,unit])
                for j in range(self.shop_queue[i][0].size):
                    self.profit = self.profit - ((math.pow(beta,self.producer[i].n)*item[i].price[0])*self.shop_queue[i][0]['quantity'][j])                     

            else :
                print("No!!!!")
                self.producer[i].capacity =self.producer[i].capacity + unit
        

        
    def response(self):
        for i in range(len(self.consumer)):
            if self.product_queue[len(self.product_queue)-1] == "nope":
                self.product_queue.pop()
                self.consumer[i].product_queue.insert(0,self.gotomarket(self.shop_queue[i].pop()))
            else :
                for j in range(len(self.product_queue[len(self.product_queue)-1]['quantity'])):
                    ans = self.shop_queue[i][0]['quantity'][j] - self.product_queue[len(self.product_queue)-1]['quantity'][j] 
                    if ans >0 :
                        self.shop_queue[i][0]['quantity'][j] = ans 
                        self.product_queue[len(self.product_queue)-1]['quantity'][j] = self.product_queue[len(self.product_queue)-1]['quantity'][j] +ans
                        
                    else :
                        self.shop_queue[i][0]['quantity'][j] = 0
                        self.product_queue[len(self.product_queue)-1]['quantity'][j] = self.product_queue[len(self.product_queue)-1]['quantity'][j] + ans       
                self.gotomarket(self.shop_queue[i].pop())
                self.consumer[i].product_queue.insert(0,self.product_queue.pop())

    def gotomarket(self,amount):
        print('market')       
        for i  in range(len(amount)):
            if amount[i]['quantity'] >0 :
                self.profit = self.profit - ((math.pow(beta,self.n)*item[i].price[0])*amount[i]['quantity'])
        return amount

class supplier(business):
    def __init__(self,capacity):
        self.capacity = capacity
        self.order_queue = list()
        self.product_queue = list()
        self.n = -1
    def process(self):
        if len(self.order_queue) >0 :
            for i in range(len(self.order_queue)):
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
        else :
            self.consumer.product_queue.insert(0,"nope")        

class AllBusiness:
    def order(self):
        shop_1.order()
        shop_2.order()
        shop_3.order()
        dc.order()
    def process(self):
        supplier_1.process()
        supplier_2.process()
        supplier_3.process()
    def response(self):
        supplier_1.response()
        supplier_2.response()
        supplier_3.response()
        dc.response()


a = item('a',40)
b = item('b',30)
c = item('c',15)
dc = dc()
shop_1 =shop()
shop_2 = shop()
shop_3 = shop()
supplier_1 = supplier(2)
supplier_2 = supplier(10)
supplier_3 = supplier(2)
item = [a,b,c]
shop_1.Producer(dc)
shop_2.Producer(dc)
shop_3.Producer(dc)
dc.Consumer([shop_1,shop_2,shop_3])
dc.Producer([supplier_1,supplier_2,supplier_3])
supplier_1.Consumer(dc)
supplier_2.Consumer(dc)
supplier_3.Consumer(dc)
dc.generate_queue()

for i in range(5) :
    a.price_days(random.randint(10,30))
    b.price_days(random.randint(10,30))
    c.price_days(random.randint(10,30))
    AllBusiness().order()
    AllBusiness().process()
    AllBusiness().response()