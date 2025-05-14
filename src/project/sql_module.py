import sqlite3
from pprint import pprint

conn = sqlite3.connect(':memory:')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS "manufacturer" (
	"id"	INTEGER,
	"name"	TEXT,
	"country"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)""")

conn.commit()

c.execute("""CREATE TABLE IF NOT EXISTS "seller" (
	"id"	INTEGER,
	"name"	TEXT,
	"email"	TEXT,
	"address"	TEXT,
	"telephone"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)""")
conn.commit()

c.execute("""CREATE TABLE customer (
	"id"	INTEGER,
	"name"	TEXT,
	"email"	TEXT,
	"telephone"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)""")
conn.commit()

c.execute("""CREATE TABLE car (
	"id"	INTEGER,
	"description"	TEXT,
	"mileage"	REAL,
	"manufacturer_id"	INTEGER,
	"seller_id"	INTEGER,
	"sold"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("manufacturer_id") REFERENCES "manufacturer"("id"),
	FOREIGN KEY("seller_id") REFERENCES "seller"("id")
)
""")
conn.commit()

c.execute("""create table sale(
          id integer,
          car_id integer,
          customer_id integer,
          sale_date text,
          sale_price real,
          primary key (id autoincrement),
          foreign key (car_id) references car(id),
          foreign key (customer_id) references customer(id)
          )""")
conn.commit()


def add_customer(name,email,tele):
    c.execute("insert into customer values (null,?,?,?)", (name,email,tele))
    conn.commit()

def add_car(desc,mil,man_id,seller_id,sold):
    c.execute("insert into car values (null,?,?,?,?,?)", (desc,mil,man_id,seller_id,sold))
    conn.commit()

def add_manuf(name,country):
    c.execute("insert into manufacturer values (null,?,?)", (name,country))
    conn.commit()

def add_seller(name,email,addr,teleph):
    c.execute("insert into seller values (null,?,?,?,?)", (name,email,addr,teleph))
    conn.commit()

def sell_car(car_id, customer_id, sale_date, sale_price):
    c.execute("insert into sale values(null, ?, ?, ?, ?)", (car_id,customer_id, sale_date, sale_price))

    c.execute("update car set sold = 'yes' where id = :car_id ", {'car_id': car_id})
    conn.commit()

def list_unsold_cars():
    print("\nUnsold cars:")
    c.execute("select description,mileage from car where sold = 'no'")
    column_names = [description[0] for description in c.description]
    print(" | ".join(column_names))
    unsold_cars = c.fetchall()
    pprint(unsold_cars)

def show_cars_by(name):
    print(f"\ncars by {name}:")
    c.execute("""select * from car
              where manufacturer_id = (select id from manufacturer where name = :name)""", {"name": name})
    column_names = [description[0] for description in c.description]
    print(" | ".join(column_names))
    cars = c.fetchall()
    pprint(cars)

def show_customers():
    print("\nCustomers: ")
    c.execute("select name,email,telephone from customer")
    column_names = [description[0] for description in c.description]
    print(" | ".join(column_names))
    customers = c.fetchall()
    pprint(customers)

def show_sales_record():
    print("\nSales record:")
    c.execute("""select c.description,cu.name as customer_name, sale_date, sale_price from sale s
              join car c on s.car_id = c.id
              join customer cu on s.customer_id = cu.id
              """)
    column_names = [description[0] for description in c.description]
    print(" | ".join(column_names))
    sales = c.fetchall()
    pprint(sales)

def show_average_sold():
    print("\nAverage sales in dollars:")
    c.execute("select round(avg(sale_price),2) as average_sales from sale")
    column_names = [description[0] for description in c.description]
    print(" | ".join(column_names))
    sales = c.fetchall()
    pprint(sales)

def show_cars_with_mileage(mileage):
    print(f"\nCars with mileage less than {mileage} miles: ")
    c.execute("select description, mileage from car where mileage <= :mile", {'mile':mileage})
    column_names = [description[0] for description in c.description]
    print(" | ".join(column_names))
    cars = c.fetchall()
    pprint(cars)

def show_sellers_total():
    print("\nSeller's total: $")
    c.execute("""select s.name, sum(sale_price) as total from sale sa
              join car c on car_id = c.id
              join seller s on c.seller_id = s.id
              group by s.name""")
    column_names = [description[0] for description in c.description]
    print(" | ".join(column_names))
    total = c.fetchall()
    pprint(total)

def manufacturer_total_cars():
    print("\nTotal cars for each manufacturer: ")
    c.execute("""select count(*) as total, m.name from car
              join manufacturer m on m.id = manufacturer_id
              group by m.name""")
    column_names = [description[0] for description in c.description]
    print(" | ".join(column_names))
    total = c.fetchall()
    pprint(total)

def country_total_cars():
    print("\nTotal cars for each country: ")
    c.execute("""select count(*) as total, m.country from car
              join manufacturer m on m.id = manufacturer_id
              group by m.country""")
    column_names = [description[0] for description in c.description]
    print(" | ".join(column_names))
    total = c.fetchall()
    pprint(total)    

add_seller("iso","iso@gmail.com","beirut","71 52 42 32")
add_seller("john","john@gmail.com","new york","0002 324 43")
add_seller("sza","sza@hotmai.com","berlin","2132 43534 23")
add_seller("peter","peter@gmail.com","new york","23 4332 3431")


add_customer("jess","re@gmail.com","2343 54")
add_customer("abdo","ab@gmail.com","23 34 1232")
add_customer("rodi","rod@gmail.com","324 2134 21")
add_customer("brock","sim@hotmail.com","213 43 2298")

add_manuf("bmw","germany")
add_manuf("volvo","sweden")
add_manuf("audi","germany")
add_manuf("mercedes","germany")
add_manuf("ford","usa")
add_manuf("honda","japan")
add_manuf("toyota","japan")
add_manuf("nissan","japan")
add_manuf("hyundai","south korea")

add_car("m4",1900,1,1,"no")
add_car("m8",1000,1,1,"no")
add_car("accent",7000,9,2,"no")
add_car("xc90",4000,2,1,"no")
add_car("activa",0,5,3,"no")
add_car("A5",0,3,1,"no")
add_car("Q7",12000,3,1,"no")
add_car("c197 amg",20000,4,4,"no")
add_car("mustang",0,5,3,"no")
add_car("accord",300,6,4,"no")
add_car("R8",300,3,2,"no")

sell_car(1,1,"12/5/2025","7000$")
sell_car(3,2,"12/5/2025","2100$")
sell_car(4,2,"12/5/2025","9000$")
sell_car(5,4,"12/5/2025","4500$")
sell_car(9,3,"12/5/2025","2500$")

list_unsold_cars()
show_cars_by("audi")
show_customers()
show_sales_record()
show_average_sold()

show_cars_with_mileage(2000)
show_sellers_total()

manufacturer_total_cars()
country_total_cars()

conn.close()