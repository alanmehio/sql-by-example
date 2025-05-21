# This file has already been runned and the data base was created inside the folder /database
# No need to run this file again.

import sqlite3

import os.path
from pathlib import Path

s = os.path.dirname(__file__)
p = Path(s).parent.parent.joinpath("database")
db_detail_path = str(p) + os.path.sep + "dealer.db" # dealer database

conn = sqlite3.connect(db_detail_path)
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

conn.close()