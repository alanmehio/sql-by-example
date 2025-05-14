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





add_seller("iso","iso@gmail.com","beirut","71 52 42 32")
add_customer("re","re@gmail.com","2343 54")

add_manuf("bmw","germany")
add_manuf("volvo","sweden")
add_manuf("audi","germany")

add_car("m4",1000,1,1,"no")
add_car("m8",1000,1,1,"no")
add_car("xc90",4000,2,1,"no")
add_car("A5",0,3,1,"no")


sell_car(1,1,"12/5/2025","7000$")
sell_car(3,1,"12/5/2025","2000$")
sell_car(4,1,"12/5/2025","9000$")


list_unsold_cars()
show_cars_by("audi")
show_customers()
show_sales_record()
show_average_sold()

conn.close()