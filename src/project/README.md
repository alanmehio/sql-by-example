# Project

This project is seperated into two files (create_tables.py, sql_module.py). 

1- create_tables.py is a script that creates the database named dealer.db. It creates it inside the folder named "database" which is at the same level as "src". There is no need to run this file as it already created the database and you will get an error. Unless you want to create a new data base with empty tables, you can delete the old data base and run this file again. 

This file also creates the tables with the relations between them using foreign keys.

2- sql_module.py is a script that contain a class called "DetailDataBaseManager" which is responsible for opening the database "dealer.db" in the database folder. It also contain methods for adding into the tables, selling cars, doing several complex queries like show_cars_by("audi") which shows all cars by this brand, you can try any brand you want. 

You can run the file to see the result for all the different queries I added.
I also commented out the code that I used to add data into the tables. The members are going to add data through the app and not in code.

## Required

The requirements from the members are:

1- Create a branch after your name so we can keep track of each member. So for example "git checkout -b ISO-branch" and then start working on the bellow.

2- Use sqlitebrowser that you installed to open the "dealer.db" database and manipulate the data. Which means you have to add several data into all the tables. Using the application itself. 

3- After changing and saving into the database, you have to add several more methods into the "DetailDatabaseManager" inside the file sql_module.py file.
The methods should do the following queries:
    1- Calculate the total sold cars for each brand.
    2- Calculate the average sales for each country.
    3- Show the cars that are new (not used) so it should have 0 miles.
    4- Calculate the average price of cars for a given brand. 

    Those methods add them inside the class under the other methods and if you need any hint for them, ask for hints.