# Chocolate Production
Accounting of material and financial resources of a private enterprise for the production of chocolate products.

The course project was developed as part of the academic year on the subject of DBMS in the third year of the 2nd semester. After implementing this work, I used various technologies, such as the `Python programming language` and the framework `Django`, `Html`, `Css`, `Bootstrap`, `T-SQL`, `Microsoft SQL Server`. 

In the database, I used objects such as `tables`, `triggers`, `stored procedures`. 

In general, the development of an accounting system for a private enterprise has brought me valuable experience and skills that can be applied in future projects and contribute to professional development in the field of programming and software development.

## Setup

1. Installing Python, Microsoft SQL Server: 

If you don't have `Python` installed, `Microsoft SQL Server`. 
Go to their official websites and install

2. Clone the repository:

```sh
$ git clone https://github.com/Nurlis03/course_work.git
$ cd course_work
```

3. Create a virtual environment to install dependencies in and activate it:

```sh
$ python -m venv env
$ env/Scripts/activate
```

4. Then install dependencies:

```sh
(env)$ pip install -r requirements.txt
```

Note `(env)` in front of the promt. This indicates that this terminal
session operates in a virtual envirounment set up  by `python -m venv`.

Once `pip` has finished downloading the dependencies:

5. Configuring the database:

- Open the `database_files` folder, import the `PPO3-2-version.bak`, or `PPO3-2-version.bacpac` one of them in Microsoft SQL Server Management Studio.
- Open  SQL Server Configuration Manager and follow these steps:
    - Enable TCP/IP protocol.
    - Set the port for TCP/IP protocol (port 1433 is usually used).
- Configure database access for your Django project in a file settings.py
  Specify the following parameters:
```python
     DATABASES = {
        'default': {
            'ENGINE': 'mssql',
            'NAME': 'PPO3-2-version',
            'USER': 'sa',
            'PASSWORD': 'Nurlis2003',
            'HOST': 'DESKTOP-VNGU8OG\\SQLEXPRESS',
            'PORT': '1433',

            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',
            },
        },
    }
 ```

6. Run the project:

```sh
(env)$ cd chocolate_production
(env)$ python manage.py runserver
```

## Functionality
1. CRUD operations of 7 tables(Budget, Employee, Finished_products, Ingredients, Positions, Raw_material, Units)
2. Purchase of raw materials
3. Produce products
4. Sale of products
5. Showing the ingredients of the selected product

## Project structure
I have created separate applications for each table.

Each application has views that render templates. 

In view, I mainly used stored procedures that perform the corresponding operations in the database. 

I also used pagination for 10 records, which allows for effective interaction with data.

## Design of database

![image](https://github.com/Nurlis03/course_work/assets/99631295/2ff846d7-a983-4275-be30-7680473894ca)

## Author 

**------------------------------Kimbiletov Nurlis Muratovich*-----------------------------*
