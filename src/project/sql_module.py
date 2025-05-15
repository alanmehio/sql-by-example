import sqlite3
from pprint import pprint


import os.path
from pathlib import Path

s = os.path.dirname(__file__)
p = Path(s).parent.parent.joinpath("database")



class DetailDataBaseManager():
    db_detail_path = str(p) + os.path.sep + "dealer.db" # dealer database
    con = sqlite3.connect(db_detail_path)
    c = con.cursor()

    def __init__(self)->None:
        pass

    @classmethod
    def add_customer(cls,name,email,tele):   
        cls.c.execute("insert into customer values (null,?,?,?)", (name,email,tele))
        cls.con.commit()

    @classmethod    
    def add_car(cls,desc,mil,man_id,seller_id,sold):
        cls.c.execute("insert into car values (null,?,?,?,?,?)", (desc,mil,man_id,seller_id,sold))
        cls.con.commit()

    @classmethod
    def add_manuf(cls,name,country):
        cls.c.execute("insert into manufacturer values (null,?,?)", (name,country))
        cls.con.commit()
    
    @classmethod
    def add_seller(cls,name,email,addr,teleph):
        cls.c.execute("insert into seller values (null,?,?,?,?)", (name,email,addr,teleph))
        cls.con.commit()
    
    @classmethod
    def sell_car(cls,car_id, customer_id, sale_date, sale_price):
        cls.c.execute("insert into sale values(null, ?, ?, ?, ?)", (car_id,customer_id, sale_date, sale_price))

        cls.c.execute("update car set sold = 'yes' where id = :car_id ", {'car_id': car_id})
        cls.con.commit()

    @classmethod
    def list_unsold_cars(cls):
        print("\nUnsold cars:")
        cls.c.execute("select description,mileage from car where sold = 'no'")
        column_names = [description[0] for description in cls.c.description]
        print(" | ".join(column_names))
        unsold_cars = cls.c.fetchall()
        pprint(unsold_cars)

    @classmethod
    def show_cars_by(cls,name):
        print(f"\ncars by {name}:")
        cls.c.execute("""select * from car
                where manufacturer_id = (select id from manufacturer where name = :name)""", {"name": name})
        column_names = [description[0] for description in cls.c.description]
        print(" | ".join(column_names))
        cars = cls.c.fetchall()
        pprint(cars)

    @classmethod
    def show_customers(cls):
        print("\nCustomers: ")
        cls.c.execute("select name,email,telephone from customer")
        column_names = [description[0] for description in cls.c.description]
        print(" | ".join(column_names))
        customers = cls.c.fetchall()
        pprint(customers)

    @classmethod
    def show_sales_record(cls):
        print("\nSales record:")
        cls.c.execute("""select c.description,cu.name as customer_name, sale_date, sale_price from sale s
                join car c on s.car_id = c.id
                join customer cu on s.customer_id = cu.id
                """)
        column_names = [description[0] for description in cls.c.description]
        print(" | ".join(column_names))
        sales = cls.c.fetchall()
        pprint(sales)

    @classmethod
    def show_average_sold(cls):
        print("\nAverage sales in dollars:")
        cls.c.execute("select round(avg(sale_price),2) as average_sales from sale")
        column_names = [description[0] for description in cls.c.description]
        print(" | ".join(column_names))
        sales = cls.c.fetchall()
        pprint(sales)

    @classmethod
    def show_cars_with_mileage(cls,mileage):
        print(f"\nCars with mileage less than {mileage} miles: ")
        cls.c.execute("select description, mileage from car where mileage <= :mile", {'mile':mileage})
        column_names = [description[0] for description in cls.c.description]
        print(" | ".join(column_names))
        cars = cls.c.fetchall()
        pprint(cars)

    @classmethod
    def show_sellers_total(cls):
        print("\nSeller's total: $")
        cls.c.execute("""select s.name, sum(sale_price) as total from sale sa
                join car c on car_id = c.id
                join seller s on c.seller_id = s.id
                group by s.name""")
        column_names = [description[0] for description in cls.c.description]
        print(" | ".join(column_names))
        total = cls.c.fetchall()
        pprint(total)

    @classmethod
    def manufacturer_total_cars(cls):
        print("\nTotal cars for each manufacturer: ")
        cls.c.execute("""select count(*) as total, m.name from car
                join manufacturer m on m.id = manufacturer_id
                group by m.name""")
        column_names = [description[0] for description in cls.c.description]
        print(" | ".join(column_names))
        total = cls.c.fetchall()
        pprint(total)

    @classmethod
    def country_total_cars(cls):
        print("\nTotal cars for each country: ")
        cls.c.execute("""select count(*) as total, m.country from car
                join manufacturer m on m.id = manufacturer_id
                group by m.country""")
        column_names = [description[0] for description in cls.c.description]
        print(" | ".join(column_names))
        total = cls.c.fetchall()
        pprint(total)    

'''
DetailDataBaseManager.add_customer("jess","re@gmail.com","2343 54")
DetailDataBaseManager.add_customer("abdo","ab@gmail.com","23 34 1232")
DetailDataBaseManager.add_customer("rodi","rod@gmail.com","324 2134 21")
DetailDataBaseManager.add_customer("brock","sim@hotmail.com","213 43 2298")

DetailDataBaseManager.add_seller("iso","iso@gmail.com","beirut","71 52 42 32")
DetailDataBaseManager.add_seller("john","john@gmail.com","new york","0002 324 43")
DetailDataBaseManager.add_seller("sza","sza@hotmai.com","berlin","2132 43534 23")
DetailDataBaseManager.add_seller("peter","peter@gmail.com","new york","23 4332 3431")

DetailDataBaseManager.add_manuf("bmw","germany")
DetailDataBaseManager.add_manuf("volvo","sweden")
DetailDataBaseManager.add_manuf("audi","germany")
DetailDataBaseManager.add_manuf("mercedes","germany")
DetailDataBaseManager.add_manuf("ford","usa")
DetailDataBaseManager.add_manuf("honda","japan")
DetailDataBaseManager.add_manuf("toyota","japan")
DetailDataBaseManager.add_manuf("nissan","japan")
DetailDataBaseManager.add_manuf("hyundai","south korea")

DetailDataBaseManager.add_car("m4",1900,1,1,"no")
DetailDataBaseManager.add_car("m8",1000,1,1,"no")
DetailDataBaseManager.add_car("accent",7000,9,2,"no")
DetailDataBaseManager.add_car("xc90",4000,2,1,"no")
DetailDataBaseManager.add_car("activa",0,5,3,"no")
DetailDataBaseManager.add_car("A5",0,3,1,"no")
DetailDataBaseManager.add_car("Q7",12000,3,1,"no")
DetailDataBaseManager.add_car("c197 amg",20000,4,4,"no")
DetailDataBaseManager.add_car("mustang",0,5,3,"no")
DetailDataBaseManager.add_car("accord",300,6,4,"no")
DetailDataBaseManager.add_car("R8",300,3,2,"no")

DetailDataBaseManager.sell_car(1,1,"12/5/2025","7000$")
DetailDataBaseManager.sell_car(3,2,"12/5/2025","2100$")
DetailDataBaseManager.sell_car(4,2,"12/5/2025","9000$")
DetailDataBaseManager.sell_car(5,4,"12/5/2025","4500$")
DetailDataBaseManager.sell_car(9,3,"12/5/2025","2500$")
'''

DetailDataBaseManager.list_unsold_cars()
DetailDataBaseManager.show_cars_by("audi")
DetailDataBaseManager.show_customers()
DetailDataBaseManager.show_sales_record()
DetailDataBaseManager.show_average_sold()

DetailDataBaseManager.show_cars_with_mileage(2000)
DetailDataBaseManager.show_sellers_total()

DetailDataBaseManager.manufacturer_total_cars()
DetailDataBaseManager.country_total_cars()
