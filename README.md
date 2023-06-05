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

```sh
(env)$ cd chocolate_production
(env)$ python manage.py runserver
