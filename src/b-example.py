'''
In this module, we will create the below two tables and populate them and query them 

BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Frequency" (
	"id"	INTEGER,
	"frequency"	INTEGER NOT NULL,
	"power"	REAL NOT NULL,
	"datetime "	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "FrequencySamples" (
	"id"	INTEGER,
	"fk"	INTEGER,
	"real"	REAL,
	"imag"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("fk") REFERENCES "Frequency"
);
COMMIT;

'''
# User sqlitebrowser client to create the above table use below database name 
# "database/detail.db" 
# so the database file is under the database folder and called "detail.db"


import sqlite3
import os.path
from pathlib import Path

s = os.path.dirname(__file__)
p = Path(s).parent.parent.parent.joinpath("database")


class DetailDataBaseManager():
    db_detail_path = str(p) + os.path.sep + "detail.db" # detail database

    def __init__(self)->None:
        pass

    @classmethod
    def insert_frequency_samples(cls,frequency:int, power:float, date_time:str, samples:list[complex])->None:
        # power, frequency and samples for the center frequency
        con = sqlite3.connect(cls.db_detail_path)
        cur = con.cursor()
        cur.execute("INSERT INTO Frequency VALUES(NULL,?,?,?)", (frequency,power, date_time))
        primary_key = cur.lastrowid 
        data = cls.__convert__(primary_key=primary_key,samples=samples)
        cur.executemany("INSERT INTO FrequencySamples VALUES(NULL,?,?,?)",data)
        con.commit()
        con.close()


    @classmethod
    def __convert__(cls, primary_key:int, samples:list[complex])->list[tuple[int,float,float]]:
        lst = []
        for x in samples:
           var = (primary_key,x.real,x.imag)
           lst.append(var)

        return lst
    
    @classmethod
    def insert_power_frequencies(cls, power: float, date_time:str, frequencies: list[int]):
        con = sqlite3.Connection(cls.db_detail_path)
        cur = con.cursor()
        cur.execute("INSERT INTO Power VALUES(NULL,?,?)",(power,date_time))
        primary_key = cur.lastrowid
        lst = []
        for x in frequencies:
            var = (primary_key,x) # tuple or database record 
            lst.append(var)
        
        cur.executemany("INSERT INTO PowerFrequencies VALUES(NULL,?,?)",lst)
        con.commit()
        con.close()
         


       


if __name__ == '__main__':
    power:float = 50.55
    frequency = 105
    lst = []
    c:complex = complex(2.0,1.333)
    lst.append(c)
    date_time="25-05-04 13:33:10"
    DetailDataBaseManager.insert_frequency_samples(frequency=frequency,power=power, 
                                                   date_time=date_time,
                                                   samples=lst)
    frequencies = [105,106,107,108]
    DetailDataBaseManager.insert_power_frequencies(power,date_time,frequencies)
