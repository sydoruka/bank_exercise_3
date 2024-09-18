import sqlite3
from prettytable import PrettyTable


# Function to display fetched rows in a pretty table
def display_prettytable(cursor):
    rows = cursor.fetchall()
    if rows:
        # Get column names from cursor description
        column_names = [description[0] for description in cursor.description]

        # Create a PrettyTable object
        table = PrettyTable()
        table.field_names = column_names

        # Add rows to the table
        for row in rows:
            table.add_row(row)

        # Print the table
        print(table)

### Exercises: Write SQL queries to answer the following questions.
# --------------------------------------------------------------------------------
## 1. Produce a list of employees (emp ID, name) and the address of the branch they are located
def ex_1():
        with sqlite3.connect('bank.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT
                e.emp_id,
                e.first_name || ' ' || e.last_name as Name,
                b.address
            FROM employee e
            JOIN branch b ON e.assigned_branch_id = b.branch_id
            ''')
            display_prettytable(cursor)

# --------------------------------------------------------------------------------
## 2. Produce a list of Customers (ID, address, birthdate) and their account numbers
def ex_2():
        with sqlite3.connect('bank.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT
                c.cust_id,
                c.address,
                i.birth_date,
                a.account_id
            FROM customer c
            JOIN individual i
                ON c.cust_id = i.cust_id
            JOIN account a
                ON c.cust_id = a.cust_id
            ''')
            display_prettytable(cursor)

# --------------------------------------------------------------------------------
## 3. Your query should return as many rows as are in the CUSTOMER table
##    and output the following columns:
##    CUSTOMER (Cust_ID, FED_ID, STATE), OFFICER (Officer_ID, Start_Date, Title)
def ex_3():
        with sqlite3.connect('bank.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT
                c.cust_id,
                c.fed_id,
                c.state,
                o.officer_id,
                o.start_date,
                o.title
            FROM customer c
            LEFT JOIN officer o
                ON c.cust_id = o.cust_id
            ''')
            display_prettytable(cursor)

# --------------------------------------------------------------------------------
## 4. Output a list of customer names that have a total available balance > £5000
def ex_4():
        with sqlite3.connect('bank.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT 
                i.first_name || ' ' || i.last_name AS Name,
                ROUND(SUM(a.avail_balance), 2) as Total_Balance
            FROM 
                individual i
            JOIN 
                account a
                ON i.cust_id = a.cust_id
            GROUP BY 
                i.first_name || ' ' || i.last_name
            HAVING  
                SUM(a.avail_balance) > 5000

            UNION ALL

            SELECT 
                b.name AS name,
                ROUND(SUM(a.avail_balance), 2) as Total_Balance
            FROM   
                business b
            JOIN 
                account a
                ON b.cust_id = a.cust_id
            GROUP BY 
                b.name
            HAVING 
                SUM(a.avail_balance) > 5000
            ''')
            display_prettytable(cursor)

# --------------------------------------------------------------------------------
## 5. Produce a report of account details for Business customers that are based in the city of Salem.
def ex_5():
        with sqlite3.connect('bank.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT
                a.*,
                c.city
            FROM
                account a
            JOIN
                business b
                ON a.cust_id = b.cust_id
            JOIN
                customer c
                ON b.cust_id = c.cust_id
            WHERE
                c.city = 'Salem'
            ''')
            display_prettytable(cursor)

# --------------------------------------------------------------------------------
## 6. Return a list of department names and the number of employees that work in each.
def ex_6():
        with sqlite3.connect('bank.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT
                d.name AS name,
                COUNT(e.emp_id) AS employee_count
            FROM
                department d
            JOIN
                employee e
                ON d.dept_id = e.dept_id
            GROUP BY
                d.name
            ''')
            display_prettytable(cursor)

# --------------------------------------------------------------------------------
## 7. Return a list of department names and the number of employees
##    that work in each for all those based at Headquarters
def ex_7():
        with sqlite3.connect('bank.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT
                d.name AS name,
                COUNT(e.emp_id) AS employee_count,
                b.name AS branch_name
            FROM
                department d
            JOIN
                employee e
                ON d.dept_id = e.dept_id
            JOIN
                branch b
                ON e.assigned_branch_id = b.branch_id
            WHERE
                b.name = 'Headquarters'
            GROUP BY
                d.name
            ''')
            display_prettytable(cursor)

# --------------------------------------------------------------------------------
## 8. Write a nested subquery to show the ACCOUNT details
##    (account_id, open_date, product_cd, avail_balance) for Business customers only.

def ex_8():
        with sqlite3.connect('bank.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT
                a.*
            FROM
                account a
            WHERE
                a.cust_id IN 
                (SELECT b.cust_id
                FROM business b)
            ''')
            display_prettytable(cursor)

# --------------------------------------------------------------------------------
## 9. Write a subquery to show the CUSTOMER details (cust_id, address, fed_id)
##    and the total available account balance per customer.
##    Write the Subquery in FROM clause (inline view).
def ex_9():
        with sqlite3.connect('bank.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT *
            FROM
                (SELECT
                    c.cust_id,
                    c.address,
                    c.fed_id,
                    ROUND(SUM(a.avail_balance), 2) AS total_balance
                FROM customer c
                JOIN account a
                    ON c.cust_id = a.cust_id
                GROUP BY c.cust_id)
            ''')
            display_prettytable(cursor)

# --------------------------------------------------------------------------------
## 10. Rewrite the answer to the previous question as a subquery in the SELECT clause.
def ex_10():
        with sqlite3.connect('bank.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT
                c.cust_id,
                c.address,
                c.fed_id,
                (SELECT
                    ROUND(SUM(a.avail_balance), 2)
                FROM
                    account a
                WHERE c.cust_id = a.cust_id) AS total_balance
            FROM
                customer c
            ''')
            display_prettytable(cursor)

# --------------------------------------------------------------------------------
## 11. Calculate the average available balance for customers accounts
def ex_11():
        with sqlite3.connect('bank.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
        SELECT
            (SELECT AVG(avail_balance)
            FROM (SELECT SUM(avail_balance) 
                  FROM account 
                  GROUP BY cust_id)) AS avg_bal
        FROM
            account
            ''')
            display_prettytable(cursor)

# --------------------------------------------------------------------------------
## 12.  Find which Department currently has NO employees.
def ex_12():
        with sqlite3.connect('bank.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT
                d.name
            FROM
                department d
            LEFT JOIN
                employee e
                ON d.dept_id = e.dept_id
            WHERE
                e.dept_id IS NULL;
            ''')
            display_prettytable(cursor)
