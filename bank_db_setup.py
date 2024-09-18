import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

# Create CUSTOMER table
cursor.execute('''
CREATE TABLE IF NOT EXISTS CUSTOMER (
    CUST_ID INTEGER NOT NULL PRIMARY KEY,
    ADDRESS TEXT,
    CITY TEXT,
    CUST_TYPE_CD TEXT NOT NULL,
    FED_ID TEXT NOT NULL,
    POSTAL_CODE TEXT,
    STATE TEXT
)
''')

# Create BRANCH table
cursor.execute('''
CREATE TABLE IF NOT EXISTS BRANCH (
    BRANCH_ID INTEGER NOT NULL PRIMARY KEY,
    ADDRESS TEXT,
    CITY TEXT,
    NAME TEXT NOT NULL,
    STATE TEXT,
    ZIP_CODE TEXT
)
''')

# Create DEPARTMENT table
cursor.execute('''
CREATE TABLE IF NOT EXISTS DEPARTMENT (
    DEPT_ID INTEGER NOT NULL PRIMARY KEY,
    NAME TEXT NOT NULL
)
''')

# Create EMPLOYEE table
cursor.execute('''
CREATE TABLE IF NOT EXISTS EMPLOYEE (
    EMP_ID INTEGER NOT NULL PRIMARY KEY,
    END_DATE DATE,
    FIRST_NAME TEXT NOT NULL,
    LAST_NAME TEXT NOT NULL,
    START_DATE DATE NOT NULL,
    TITLE TEXT,
    ASSIGNED_BRANCH_ID INTEGER,
    DEPT_ID INTEGER,
    SUPERIOR_EMP_ID INTEGER,
    FOREIGN KEY (ASSIGNED_BRANCH_ID) REFERENCES BRANCH (BRANCH_ID),
    FOREIGN KEY (DEPT_ID) REFERENCES DEPARTMENT (DEPT_ID),
    FOREIGN KEY (SUPERIOR_EMP_ID) REFERENCES EMPLOYEE (EMP_ID)
)
''')

# Create PRODUCT_TYPE table
cursor.execute('''
CREATE TABLE IF NOT EXISTS PRODUCT_TYPE (
    PRODUCT_TYPE_CD TEXT NOT NULL PRIMARY KEY,
    NAME TEXT
)
''')

# Create PRODUCT table
cursor.execute('''
CREATE TABLE IF NOT EXISTS PRODUCT (
    PRODUCT_CD TEXT NOT NULL PRIMARY KEY,
    DATE_OFFERED DATE,
    DATE_RETIRED DATE,
    NAME TEXT NOT NULL,
    PRODUCT_TYPE_CD TEXT,
    FOREIGN KEY (PRODUCT_TYPE_CD) REFERENCES PRODUCT_TYPE (PRODUCT_TYPE_CD)
)
''')

# Create ACCOUNT table
cursor.execute('''
CREATE TABLE IF NOT EXISTS ACCOUNT (
    ACCOUNT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    AVAIL_BALANCE NUMERIC(14, 2),
    CLOSE_DATE DATE,
    LAST_ACTIVITY_DATE DATE,
    OPEN_DATE DATE NOT NULL,
    PENDING_BALANCE NUMERIC(14, 2),
    STATUS TEXT,
    CUST_ID INTEGER,
    OPEN_BRANCH_ID INTEGER NOT NULL,
    OPEN_EMP_ID INTEGER NOT NULL,
    PRODUCT_CD TEXT NOT NULL,
    FOREIGN KEY (CUST_ID) REFERENCES CUSTOMER (CUST_ID),
    FOREIGN KEY (OPEN_BRANCH_ID) REFERENCES BRANCH (BRANCH_ID),
    FOREIGN KEY (OPEN_EMP_ID) REFERENCES EMPLOYEE (EMP_ID),
    FOREIGN KEY (PRODUCT_CD) REFERENCES PRODUCT (PRODUCT_CD)
)
''')

# Create ACC_TRANSACTION table
cursor.execute('''
CREATE TABLE IF NOT EXISTS ACC_TRANSACTION (
    TXN_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    AMOUNT NUMERIC(14, 2) NOT NULL,
    FUNDS_AVAIL_DATE TIMESTAMP NOT NULL,
    TXN_DATE TIMESTAMP NOT NULL,
    TXN_TYPE_CD TEXT,
    ACCOUNT_ID INTEGER,
    EXECUTION_BRANCH_ID INTEGER,
    TELLER_EMP_ID INTEGER,
    FOREIGN KEY (ACCOUNT_ID) REFERENCES ACCOUNT (ACCOUNT_ID),
    FOREIGN KEY (EXECUTION_BRANCH_ID) REFERENCES BRANCH (BRANCH_ID),
    FOREIGN KEY (TELLER_EMP_ID) REFERENCES EMPLOYEE (EMP_ID)
)
''')

# Create BUSINESS table
cursor.execute('''
CREATE TABLE IF NOT EXISTS BUSINESS (
    INCORP_DATE DATE,
    NAME TEXT NOT NULL,
    STATE_ID TEXT NOT NULL,
    CUST_ID INTEGER NOT NULL,
    PRIMARY KEY (CUST_ID),
    FOREIGN KEY (CUST_ID) REFERENCES CUSTOMER (CUST_ID)
)
''')

# Create INDIVIDUAL table
cursor.execute('''
CREATE TABLE IF NOT EXISTS INDIVIDUAL (
    BIRTH_DATE DATE,
    FIRST_NAME TEXT NOT NULL,
    LAST_NAME TEXT NOT NULL,
    CUST_ID INTEGER NOT NULL,
    PRIMARY KEY (CUST_ID),
    FOREIGN KEY (CUST_ID) REFERENCES CUSTOMER (CUST_ID)
)
''')

# Create OFFICER table
cursor.execute('''
CREATE TABLE IF NOT EXISTS OFFICER (
    OFFICER_ID INTEGER NOT NULL PRIMARY KEY,
    END_DATE DATE,
    FIRST_NAME TEXT NOT NULL,
    LAST_NAME TEXT NOT NULL,
    START_DATE DATE NOT NULL,
    TITLE TEXT,
    CUST_ID INTEGER,
    FOREIGN KEY (CUST_ID) REFERENCES CUSTOMER (CUST_ID)
)
''')

# Insert data into DEPARTMENT table
departments = [
    (1, 'Operations'),
    (2, 'Loans'),
    (3, 'Administration'),
    (4, 'IT')
]

cursor.executemany('INSERT INTO department (dept_id, name) VALUES (?, ?)', departments)

# Insert data into BRANCH table
branches = [
    (1, 'Headquarters', '3882 Main St.', 'Waltham', 'MA', '02451'),
    (2, 'Woburn Branch', '422 Maple St.', 'Woburn', 'MA', '01801'),
    (3, 'Quincy Branch', '125 Presidential Way', 'Quincy', 'MA', '02169'),
    (4, 'So. NH Branch', '378 Maynard Ln.', 'Salem', 'NH', '03079')
]

cursor.executemany('''
INSERT INTO branch (branch_id, name, address, city, state, zip_code) 
VALUES (?, ?, ?, ?, ?, ?)''', branches)

# Insert data into EMPLOYEE table
employees = [
    (1, 'Michael', 'Smith', '2001-06-22', 'Administration', 'President', 'Headquarters'),
    (2, 'Susan', 'Barker', '2002-09-12', 'Administration', 'Vice President', 'Headquarters'),
    (3, 'Robert', 'Tyler', '2002-02-09', 'Administration', 'Treasurer', 'Headquarters'),
    (4, 'Susan', 'Hawthorne', '2004-04-24', 'Operations', 'Operations Manager', 'Headquarters'),
    (5, 'John', 'Gooding', '2003-11-14', 'Loans', 'Loan Manager', 'Headquarters'),
    (6, 'Helen', 'Fleming', '2004-03-17', 'Operations', 'Head Teller', 'Headquarters'),
    (7, 'Chris', 'Tucker', '2004-09-15', 'Operations', 'Teller', 'Headquarters'),
    (8, 'Sarah', 'Parker', '2002-12-02', 'Operations', 'Teller', 'Headquarters'),
    (9, 'Jane', 'Grossman', '2002-05-03', 'Operations', 'Teller', 'Headquarters'),
    (10, 'Paula', 'Roberts', '2002-07-27', 'Operations', 'Head Teller', 'Woburn Branch'),
    (11, 'Thomas', 'Ziegler', '2000-10-23', 'Operations', 'Teller', 'Woburn Branch'),
    (12, 'Samantha', 'Jameson', '2003-01-08', 'Operations', 'Teller', 'Woburn Branch'),
    (13, 'John', 'Blake', '2011-05-11', 'Operations', 'Head Teller', 'Quincy Branch'),
    (14, 'Cindy', 'Mason', '2002-08-09', 'Operations', 'Teller', 'Quincy Branch'),
    (15, 'Frank', 'Portman', '2003-04-01', 'Operations', 'Teller', 'Quincy Branch'),
    (16, 'Theresa', 'Markham', '2001-03-15', 'Operations', 'Head Teller', 'So. NH Branch'),
    (17, 'Beth', 'Fowler', '2002-06-29', 'Operations', 'Teller', 'So. NH Branch'),
    (18, 'Rick', 'Tulman', '2002-12-12', 'Operations', 'Teller', 'So. NH Branch')
]

# Insert into employee using SELECT for dept_id and branch_id
for emp_id, first_name, last_name, start_date, dept_name, title, branch_name in employees:
    cursor.execute('''
    INSERT INTO employee (emp_id, first_name, last_name, start_date, dept_id, title, assigned_branch_id)
    VALUES (?, ?, ?, ?, 
        (SELECT dept_id FROM department WHERE name = ?),
        ?,
        (SELECT branch_id FROM branch WHERE name = ?))
    ''', (emp_id, first_name, last_name, start_date, dept_name, title, branch_name))

# Step 1: Create emp_tmp table
cursor.execute("""
    CREATE TABLE emp_tmp AS 
    SELECT emp_id, First_Name, Last_Name FROM employee;
""")

# # Step 2: Update employee with superior_emp_id for multiple cases
cursor.execute("""
    UPDATE employee
    SET superior_emp_id = (
        SELECT emp_id FROM emp_tmp
        WHERE Last_Name = 'Smith' AND First_Name = 'Michael'
    )
    WHERE ( (Last_Name = 'Barker' AND First_Name = 'Susan') OR
            (Last_Name = 'Tyler' AND First_Name = 'Robert') );
""")

cursor.execute("""
    UPDATE employee
    SET superior_emp_id = (
        SELECT emp_id FROM emp_tmp
        WHERE Last_Name = 'Tyler' AND First_Name = 'Robert'
    )
    WHERE Last_Name = 'Hawthorne' AND First_Name = 'Susan';
""")

cursor.execute("""
    UPDATE employee
    SET superior_emp_id = (
        SELECT emp_id FROM emp_tmp
        WHERE Last_Name = 'Hawthorne' AND First_Name = 'Susan'
    )
    WHERE ( (Last_Name = 'Gooding' AND First_Name = 'John') OR
            (Last_Name = 'Fleming' AND First_Name = 'Helen') OR
            (Last_Name = 'Roberts' AND First_Name = 'Paula') OR
            (Last_Name = 'Blake' AND First_Name = 'John') OR
            (Last_Name = 'Markham' AND First_Name = 'Theresa') );
""")

cursor.execute("""
    UPDATE employee
    SET superior_emp_id = (
        SELECT emp_id FROM emp_tmp
        WHERE Last_Name = 'Fleming' AND First_Name = 'Helen'
    )
    WHERE ( (Last_Name = 'Tucker' AND First_Name = 'Chris') OR
            (Last_Name = 'Parker' AND First_Name = 'Sarah') OR
            (Last_Name = 'Grossman' AND First_Name = 'Jane') );
""")

cursor.execute("""
    UPDATE employee
    SET superior_emp_id = (
        SELECT emp_id FROM emp_tmp
        WHERE Last_Name = 'Roberts' AND First_Name = 'Paula'
    )
    WHERE ( (Last_Name = 'Ziegler' AND First_Name = 'Thomas') OR
            (Last_Name = 'Jameson' AND First_Name = 'Samantha') );
""")

cursor.execute("""
    UPDATE employee
    SET superior_emp_id = (
        SELECT emp_id FROM emp_tmp
        WHERE Last_Name = 'Blake' AND First_Name = 'John'
    )
    WHERE ( (Last_Name = 'Mason' AND First_Name = 'Cindy') OR
            (Last_Name = 'Portman' AND First_Name = 'Frank') );
""")

cursor.execute("""
    UPDATE employee
    SET superior_emp_id = (
        SELECT emp_id FROM emp_tmp
        WHERE Last_Name = 'Markham' AND First_Name = 'Theresa'
    )
    WHERE ( (Last_Name = 'Fowler' AND First_Name = 'Beth') OR
            (Last_Name = 'Tulman' AND First_Name = 'Rick') );
""")

# # Step 3: Drop emp_tmp table
cursor.execute("DROP TABLE emp_tmp;")

# Step 4: Insert data into product_type
product_types = [
    ('ACCOUNT', 'Customer Accounts'),
    ('LOAN', 'Individual and Business Loans'),
    ('INSURANCE', 'Insurance Offerings')
]
cursor.executemany("""
    INSERT INTO product_type (product_type_cd, name) VALUES (?, ?);
""", product_types)

# Step 5: Insert data into product
products = [
    ('CHK', 'checking account', 'ACCOUNT', '2000-01-01'),
    ('SAV', 'savings account', 'ACCOUNT', '2000-01-01'),
    ('MM', 'money market account', 'ACCOUNT', '2000-01-01'),
    ('CD', 'certificate of deposit', 'ACCOUNT', '2000-01-01'),
    ('MRT', 'home mortgage', 'LOAN', '2000-01-01'),
    ('AUT', 'auto loan', 'LOAN', '2000-01-01'),
    ('BUS', 'business line of credit', 'LOAN', '2000-01-01'),
    ('SBL', 'small business loan', 'LOAN', '2000-01-01')
]
cursor.executemany("""
    INSERT INTO product (product_cd, name, product_type_cd, date_offered) 
    VALUES (?, ?, ?, ?);
""", products)

# Step 1: Insert customer data and related individual or business and officer data

# Insert individual customer with customer and individual details
customers = [
    (1, '111-11-1111', 'I', '47 Mockingbird Ln', 'Lynnfield', 'MA', '01940'),
    (2, '222-22-2222', 'I', '372 Clearwater Blvd', 'Woburn', 'MA', '01801'),
    (3, '333-33-3333', 'I', '18 Jessup Rd', 'Quincy', 'MA', '02169'),
    (4, '444-44-4444', 'I', '12 Buchanan Ln', 'Waltham', 'MA', '02451'),
    (5, '555-55-5555', 'I', '2341 Main St', 'Salem', 'NH', '03079'),
    (6, '666-66-6666', 'I', '12 Blaylock Ln', 'Waltham', 'MA', '02451'),
    (7, '777-77-7777', 'I', '29 Admiral Ln', 'Wilmington', 'MA', '01887'),
    (8, '888-88-8888', 'I', '472 Freedom Rd', 'Salem', 'NH', '03079'),
    (9, '999-99-9999', 'I', '29 Maple St', 'Newton', 'MA', '02458')
]
cursor.executemany("""
    INSERT INTO customer (cust_id, fed_id, cust_type_cd, address, city, state, postal_code)
    VALUES (?, ?, ?, ?, ?, ?, ?);
""", customers)

# Insert related individual data
individuals = [
    ('111-11-1111', 'James', 'Hadley', '1972-04-22'),
    ('222-22-2222', 'Susan', 'Tingley', '1968-08-15'),
    ('333-33-3333', 'Frank', 'Tucker', '1958-02-06'),
    ('444-44-4444', 'John', 'Hayward', '1966-12-22'),
    ('555-55-5555', 'Charles', 'Frasier', '1971-08-25'),
    ('666-66-6666', 'John', 'Spencer', '1962-09-14'),
    ('777-77-7777', 'Margaret', 'Young', '1947-03-19'),
    ('888-88-8888', 'Louis', 'Blake', '1977-07-01'),
    ('999-99-9999', 'Richard', 'Farley', '1968-06-16')
]

for fed_id, first_name, last_name, birth_date in individuals:
    cursor.execute("""
        INSERT INTO individual (cust_id, First_Name, Last_Name, birth_date)
        SELECT cust_id, ?, ?, ? FROM customer WHERE fed_id = ?;
    """, (first_name, last_name, birth_date, fed_id))

# Insert business customers and related data
business_customers = [
    (10, '04-1111111', 'B', '7 Industrial Way', 'Salem', 'NH', '03079'),
    (11, '04-2222222', 'B', '287A Corporate Ave', 'Wilmington', 'MA', '01887'),
    (12, '04-3333333', 'B', '789 Main St', 'Salem', 'NH', '03079'),
    (13, '04-4444444', 'B', '4772 Presidential Way', 'Quincy', 'MA', '02169')
]
cursor.executemany("""
    INSERT INTO customer (cust_id, fed_id, cust_type_cd, address, city, state, postal_code)
    VALUES (?, ?, ?, ?, ?, ?, ?);
""", business_customers)

# Insert business data
businesses = [
    ('04-1111111', 'Chilton Engineering', '12-345-678', '1995-05-01'),
    ('04-2222222', 'Northeast Cooling Inc.', '23-456-789', '2001-01-01'),
    ('04-3333333', 'Superior Auto Body', '34-567-890', '2002-06-03'),
    ('04-4444444', 'AAA Insurance Inc.', '45-678-901', '1999-05-01')
]

for fed_id, name, state_id, incorp_date in businesses:
    cursor.execute("""
        INSERT INTO business (cust_id, name, state_id, incorp_date)
        SELECT cust_id, ?, ?, ? FROM customer WHERE fed_id = ?;
    """, (name, state_id, incorp_date, fed_id))

# Insert officer data
officers = [
    (1, '04-1111111', 'John', 'Chilton', 'President', '1995-05-01'),
    (2, '04-2222222', 'Paul', 'Hardy', 'President', '2001-01-01'),
    (3, '04-3333333', 'Carl', 'Lutz', 'President', '2002-06-03'),
    (4, '04-4444444', 'Stanley', 'Cheswick', 'President', '1999-05-01')
]

for officer_id, fed_id, first_name, last_name, title, start_date in officers:
    cursor.execute("""
        INSERT INTO officer (officer_id, cust_id, First_Name, Last_Name, title, start_date)
        SELECT ?, cust_id, ?, ?, ?, ? FROM customer WHERE fed_id = ?;
    """, (officer_id, first_name, last_name, title, start_date, fed_id))

# Create the 'dual' table and insert dummy data
cursor.execute("CREATE VIEW IF NOT EXISTS dual AS SELECT 'x' AS dummy;")

# Insert into 'account' for cust_id = '111-11-1111'
cursor.execute("""
INSERT INTO account (
    product_cd,
    cust_id,
    open_date,
    last_activity_date,
    status,
    open_branch_id,
    open_emp_id,
    avail_balance,
    pending_balance
)
SELECT a.prod_cd,
       c.cust_id,
       a.open_date,
       a.last_date,
       'ACTIVE',
       e.branch_id,
       e.emp_id,
       a.avail,
       a.pend
FROM customer c
CROSS JOIN (
    SELECT b.branch_id,
           e.emp_id
    FROM branch b
    INNER JOIN employee e ON e.assigned_branch_id = b.branch_id
    WHERE b.city = 'Woburn' AND e.emp_id = 10
) e
CROSS JOIN (
    SELECT 'CHK' prod_cd,
           '2000-01-15' open_date,
           '2005-01-04' last_date,
           1057.75 avail,
           1057.75 pend
    FROM dual
    UNION ALL
    SELECT 'SAV' prod_cd,
           '2000-01-15' open_date,
           '2004-12-19' last_date,
           500.0 avail,
           500.0 pend
    FROM dual
    UNION ALL
    SELECT 'CD' prod_cd,
           '2004-06-30' open_date,
           '2004-06-30' last_date,
           3000.0 avail,
           3000.0 pend
    FROM dual
) a
WHERE c.fed_id = '111-11-1111';
""")

# Insert into 'account' for cust_id = '222-22-2222'
cursor.execute("""
INSERT INTO account (
    product_cd,
    cust_id,
    open_date,
    last_activity_date,
    status,
    open_branch_id,
    open_emp_id,
    avail_balance,
    pending_balance
)
SELECT a.prod_cd,
       c.cust_id,
       a.open_date,
       a.last_date,
       'ACTIVE',
       e.branch_id,
       e.emp_id,
       a.avail,
       a.pend
FROM customer c
CROSS JOIN (
    SELECT b.branch_id,
           e.emp_id
    FROM branch b
    INNER JOIN employee e ON e.assigned_branch_id = b.branch_id
    WHERE b.city = 'Woburn' AND e.emp_id = 11
) e
CROSS JOIN (
    SELECT 'CHK' prod_cd,
           '2001-03-12' open_date,
           '2004-12-27' last_date,
           2258.02 avail,
           2258.02 pend
    FROM dual
    UNION ALL
    SELECT 'SAV' prod_cd,
           '2001-03-12' open_date,
           '2004-12-11' last_date,
           200.0 avail,
           200.0 pend
    FROM dual
) a
WHERE c.fed_id = '222-22-2222';
""")

# Insert into 'account' for cust_id = '333-33-3333'
cursor.execute("""
INSERT INTO account (
    product_cd,
    cust_id,
    open_date,
    last_activity_date,
    status,
    open_branch_id,
    open_emp_id,
    avail_balance,
    pending_balance
)
SELECT a.prod_cd,
       c.cust_id,
       a.open_date,
       a.last_date,
       'ACTIVE',
       e.branch_id,
       e.emp_id,
       a.avail,
       a.pend
FROM customer c
CROSS JOIN (
    SELECT b.branch_id,
           e.emp_id
    FROM branch b
    INNER JOIN employee e ON e.assigned_branch_id = b.branch_id
    WHERE b.city = 'Quincy' AND e.emp_id = 14
) e
CROSS JOIN (
    SELECT 'CHK' prod_cd,
           '2002-11-23' open_date,
           '2004-11-30' last_date,
           1057.75 avail,
           1057.75 pend
    FROM dual
    UNION ALL
    SELECT 'MM' prod_cd,
           '2002-12-15' open_date,
           '2004-12-05' last_date,
           2212.5 avail,
           2212.5 pend
    FROM dual
) a
WHERE c.fed_id = '333-33-3333';
""")

# Insert into 'account' for cust_id = '444-44-4444'
cursor.execute("""
INSERT INTO account (
    product_cd,
    cust_id,
    open_date,
    last_activity_date,
    status,
    open_branch_id,
    open_emp_id,
    avail_balance,
    pending_balance
)
SELECT a.prod_cd,
       c.cust_id,
       a.open_date,
       a.last_date,
       'ACTIVE',
       e.branch_id,
       e.emp_id,
       a.avail,
       a.pend
FROM customer c
CROSS JOIN (
    SELECT b.branch_id,
           e.emp_id
    FROM branch b
    INNER JOIN employee e ON e.assigned_branch_id = b.branch_id
    WHERE b.city = 'Waltham' AND e.emp_id = 8
) e
CROSS JOIN (
    SELECT 'CHK' prod_cd,
           '2003-09-12' open_date,
           '2005-01-03' last_date,
           534.12 avail,
           534.12 pend
    FROM dual
    UNION ALL
    SELECT 'SAV' prod_cd,
           '2000-01-15' open_date,
           '2004-10-24' last_date,
           767.77 avail,
           767.77 pend
    FROM dual
    UNION ALL
    SELECT 'MM' prod_cd,
           '2004-09-30' open_date,
           '2004-11-11' last_date,
           5487.09 avail,
           5487.09 pend
    FROM dual
) a
WHERE c.fed_id = '444-44-4444';
""")

# Insert into 'account' for cust_id = '555-55-5555'
cursor.execute("""
INSERT INTO account (
    product_cd,
    cust_id,
    open_date,
    last_activity_date,
    status,
    open_branch_id,
    open_emp_id,
    avail_balance,
    pending_balance
)
SELECT a.prod_cd,
       c.cust_id,
       a.open_date,
       a.last_date,
       'ACTIVE',
       e.branch_id,
       e.emp_id,
       a.avail,
       a.pend
FROM customer c
CROSS JOIN (
    SELECT b.branch_id,
           e.emp_id
    FROM branch b
    INNER JOIN employee e ON e.assigned_branch_id = b.branch_id
    WHERE b.city = 'Salem' AND e.emp_id = 17
) e
CROSS JOIN (
    SELECT 'CHK' prod_cd,
           '2004-01-27' open_date,
           '2005-01-05' last_date,
           2237.97 avail,
           2897.97 pend
    FROM dual
) a
WHERE c.fed_id = '555-55-5555';
""")

# Insert into 'account' for cust_id = '666-66-6666'
cursor.execute("""
INSERT INTO account (
    product_cd,
    cust_id,
    open_date,
    last_activity_date,
    status,
    open_branch_id,
    open_emp_id,
    avail_balance,
    pending_balance
)
SELECT a.prod_cd,
       c.cust_id,
       a.open_date,
       a.last_date,
       'ACTIVE',
       e.branch_id,
       e.emp_id,
       a.avail,
       a.pend
FROM customer c
CROSS JOIN (
    SELECT b.branch_id,
           e.emp_id
    FROM branch b
    INNER JOIN employee e ON e.assigned_branch_id = b.branch_id
    WHERE b.city = 'Waltham' AND e.emp_id = 7
) e
CROSS JOIN (
    SELECT 'CHK' prod_cd,
           '2002-08-24' open_date,
           '2004-11-29' last_date,
           122.37 avail,
           122.37 pend
    FROM dual
    UNION ALL
    SELECT 'CD' prod_cd,
           '2004-12-28' open_date,
           '2004-12-28' last_date,
           10000.0 avail,
           10000.0 pend
    FROM dual
) a
WHERE c.fed_id = '666-66-6666';
""")

# Insert into 'account' for cust_id = '777-77-7777'
cursor.execute("""
INSERT INTO account (
    product_cd,
    cust_id,
    open_date,
    last_activity_date,
    status,
    open_branch_id,
    open_emp_id,
    avail_balance,
    pending_balance
)
SELECT a.prod_cd,
       c.cust_id,
       a.open_date,
       a.last_date,
       'ACTIVE',
       e.branch_id,
       e.emp_id,
       a.avail,
       a.pend
FROM customer c
CROSS JOIN (
    SELECT b.branch_id,
           e.emp_id
    FROM branch b
    INNER JOIN employee e ON e.assigned_branch_id = b.branch_id
    WHERE b.city = 'Woburn' AND e.emp_id = 12
) e
CROSS JOIN (
    SELECT 'CD' prod_cd,
           '2004-01-12' open_date,
           '2004-01-12' last_date,
           5000.0 avail,
           5000.0 pend
    FROM dual
) a
WHERE c.fed_id = '777-77-7777';
""")

# Insert into 'account' for cust_id = '888-88-8888'
cursor.execute("""
INSERT INTO account (
    product_cd,
    cust_id,
    open_date,
    last_activity_date,
    status,
    open_branch_id,
    open_emp_id,
    avail_balance,
    pending_balance
)
SELECT a.prod_cd,
       c.cust_id,
       a.open_date,
       a.last_date,
       'ACTIVE',
       e.branch_id,
       e.emp_id,
       a.avail,
       a.pend
FROM customer c
CROSS JOIN (
    SELECT b.branch_id,
           e.emp_id
    FROM branch b
    INNER JOIN employee e ON e.assigned_branch_id = b.branch_id
    WHERE b.city = 'Salem' AND e.emp_id = 18
) e
CROSS JOIN (
    SELECT 'CHK' prod_cd,
           '2001-05-23' open_date,
           '2005-01-03' last_date,
           3487.19 avail,
           3487.19 pend
    FROM dual
    UNION ALL
    SELECT 'SAV' prod_cd,
           '2001-05-23' open_date,
           '2004-10-12' last_date,
           387.99 avail,
           387.99 pend
    FROM dual
) a
WHERE c.fed_id = '888-88-8888';
""")

# Insert into 'account' for cust_id = '999-99-9999'
cursor.execute("""
INSERT INTO account (
    product_cd,
    cust_id,
    open_date,
    last_activity_date,
    status,
    open_branch_id,
    open_emp_id,
    avail_balance,
    pending_balance
)
SELECT a.prod_cd,
       c.cust_id,
       a.open_date,
       a.last_date,
       'ACTIVE',
       e.branch_id,
       e.emp_id,
       a.avail,
       a.pend
FROM customer c
CROSS JOIN (
    SELECT b.branch_id,
           e.emp_id
    FROM branch b
    INNER JOIN employee e ON e.assigned_branch_id = b.branch_id
    WHERE b.city = 'Waltham' AND e.emp_id = 9
) e
CROSS JOIN (
    SELECT 'CHK' prod_cd,
           '2003-07-30' open_date,
           '2004-12-15' last_date,
           125.67 avail,
           125.67 pend
    FROM dual
    UNION ALL
    SELECT 'MM' prod_cd,
           '2004-10-28' open_date,
           '2004-10-28' last_date,
           9345.55 avail,
           9845.55 pend
    FROM dual
    UNION ALL
    SELECT 'CD' prod_cd,
           '2004-06-30' open_date,
           '2004-06-30' last_date,
           1500.0 avail,
           1500.0 pend
    FROM dual
) a
WHERE c.fed_id = '999-99-9999';
""")

# Insert into 'account' for cust_id = '04-1111111'
cursor.execute("""
INSERT INTO account (
    product_cd,
    cust_id,
    open_date,
    last_activity_date,
    status,
    open_branch_id,
    open_emp_id,
    avail_balance,
    pending_balance
)
SELECT a.prod_cd,
       c.cust_id,
       a.open_date,
       a.last_date,
       'ACTIVE',
       e.branch_id,
       e.emp_id,
       a.avail,
       a.pend
FROM customer c
CROSS JOIN (
    SELECT b.branch_id,
           e.emp_id
    FROM branch b
    INNER JOIN employee e ON e.assigned_branch_id = b.branch_id
    WHERE b.city = 'Salem' AND e.emp_id = 16
) e
CROSS JOIN (
    SELECT 'CHK' prod_cd,
           '2002-09-30' open_date,
           '2004-12-15' last_date,
           23575.12 avail,
           23575.12 pend
    FROM dual
    UNION ALL
    SELECT 'BUS' prod_cd,
           '2002-10-01' open_date,
           '2004-08-28' last_date,
           0 avail,
           0 pend
    FROM dual
) a
WHERE c.fed_id = '04-1111111';
""")

# Create the 'dual' view if not already created
cursor.execute("CREATE VIEW IF NOT EXISTS dual AS SELECT 'x' AS dummy;")

# Insert into 'account' for cust_id = '04-2222222'
cursor.execute("""
INSERT INTO account (
    product_cd,
    cust_id,
    open_date,
    last_activity_date,
    status,
    open_branch_id,
    open_emp_id,
    avail_balance,
    pending_balance
)
SELECT a.prod_cd,
       c.cust_id,
       a.open_date,
       a.last_date,
       'ACTIVE',
       e.branch_id,
       e.emp_id,
       a.avail,
       a.pend
FROM customer c
CROSS JOIN (
    SELECT b.branch_id,
           e.emp_id
    FROM branch b
    INNER JOIN employee e ON e.assigned_branch_id = b.branch_id
    WHERE b.city = 'Woburn' AND e.emp_id = 17
) e
CROSS JOIN (
    SELECT 'BUS' prod_cd,
           '2004-03-22' open_date,
           '2004-11-14' last_date,
           9345.55 avail,
           9345.55 pend
    FROM dual
) a
WHERE c.fed_id = '04-2222222';
""")

# Insert into 'account' for cust_id = '04-3333333'
cursor.execute("""
INSERT INTO account (
    product_cd,
    cust_id,
    open_date,
    last_activity_date,
    status,
    open_branch_id,
    open_emp_id,
    avail_balance,
    pending_balance
)
SELECT a.prod_cd,
       c.cust_id,
       a.open_date,
       a.last_date,
       'ACTIVE',
       e.branch_id,
       e.emp_id,
       a.avail,
       a.pend
FROM customer c
CROSS JOIN (
    SELECT b.branch_id,
           e.emp_id
    FROM branch b
    INNER JOIN employee e ON e.assigned_branch_id = b.branch_id
    WHERE b.city = 'Salem' AND e.emp_id = 16
) e
CROSS JOIN (
    SELECT 'CHK' prod_cd,
           '2003-07-30' open_date,
           '2004-12-15' last_date,
           38552.05 avail,
           38552.05 pend
    FROM dual
) a
WHERE c.fed_id = '04-3333333';
""")

# Insert into 'account' for cust_id = '04-4444444'
cursor.execute("""
INSERT INTO account (
    product_cd,
    cust_id,
    open_date,
    last_activity_date,
    status,
    open_branch_id,
    open_emp_id,
    avail_balance,
    pending_balance
)
SELECT a.prod_cd,
       c.cust_id,
       a.open_date,
       a.last_date,
       'ACTIVE',
       e.branch_id,
       e.emp_id,
       a.avail,
       a.pend
FROM customer c
CROSS JOIN (
    SELECT b.branch_id,
           e.emp_id
    FROM branch b
    INNER JOIN employee e ON e.assigned_branch_id = b.branch_id
    WHERE b.city = 'Quincy' AND e.emp_id = 15
) e
CROSS JOIN (
    SELECT 'SBL' prod_cd,
           '2004-04-22' open_date,
           '2004-12-17' last_date,
           50000.0 avail,
           50000.0 pend
    FROM dual
) a
WHERE c.fed_id = '04-4444444';
""")

# Insert into 'acc_transaction'
cursor.execute("""
INSERT INTO acc_transaction (
    txn_date,
    account_id,
    txn_type_cd,
    amount,
    funds_avail_date
)
SELECT a.open_date,
       a.account_id,
       'CDT',
       100,
       a.open_date
FROM account a
WHERE a.product_cd IN ('CHK', 'SAV', 'CD', 'MM');
""")

# Commit and close the connection
conn.commit()
conn.close()

print("Tables created successfully!")