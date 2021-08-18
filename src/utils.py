from flaskext.mysql import MySQL

mysql = MySQL()


def clean(val):
    return None if val == '' else val

def fetch(query):
    conn = mysql.get_db()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def execute(query):
    conn = mysql.get_db()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()

def fetch_proc(proc, args):
    conn = mysql.get_db()
    cursor = conn.cursor()
    cursor.callproc(proc, args)
    result = cursor.fetchall()
    cursor.close()
    return result

def execute_proc(proc, args):
    conn = mysql.get_db()
    cursor = conn.cursor()
    cursor.callproc(proc, args)
    conn.commit()
    cursor.close()


def get_cities():
    return fetch('select distinct thCity from Theater order by thCity')


def get_states():
    return fetch('select distinct thState from Theater order by thState')

def get_companies():
    sql = 'select distinct comName from Theater order by comName'
    return fetch(sql)

def get_companies2():
    sql="select distinct comName from company order by comName"
    return fetch(sql)

def get_movies():
    return fetch('select distinct movName, movReleaseDate from Movie order by movName')

def get_credit_cards(username):
    return fetch(f'select creditCardNum from CustomerCreditCard where username="{username}"')

def update_user(username, status):
    execute_proc('admin_approve_user' if status == 'Approved' else 'admin_decline_user', (username,))

def get_theaters():
    cursor = mysql.get_db().cursor()
    cursor.execute('select distinct movName from Movie order by movName') # 
    result = cursor.fetchall()
    cursor.close()
    return result
    
def get_managers():
    cursor = mysql.get_db().cursor()
    cursor.execute('select concat(firstname," ",lastname) as "manager", user.username, comName from user right join Employee on  user.username = Employee.username where thName IS NULL OR thName = "" and employeeType = "Manager";' )
    result = cursor.fetchall()
    cursor.close()
    return result

def filter_companies(name, minCityNumber, maxCityNumber, minTheaterNumber, maxTheaterNumber, minEmployee, maxEmployee):
    sql = '''select * from 
    (SELECT distinct 
    Theater.comName, 
    count(distinct Theater.thCity) as numCityCovered,
    count(distinct Theater.thName) as numTheater, 
    count(distinct username) as numEmployee
    FROM Theater join Employee on Theater.comName = Employee.comName group by Theater.comName) as temp'''
    para = []
    if name and name != '--ALL--':
        para.append(f'comName = "{name}"')
    if minCityNumber:
        para.append(f'numCityCovered >= {minCityNumber}')
    if maxCityNumber:
        para.append(f'numCityCovered <= {maxCityNumber}')
    if minTheaterNumber:
        para.append(f'numTheater >= {minTheaterNumber}')
    if maxTheaterNumber:
        para.append(f'numTheater <= {maxTheaterNumber}')
    if minEmployee:
        para.append(f'numEmployee >= {minEmployee}')
    if maxEmployee:
        para.append(f'numEmployee <= {maxEmployee}')
    length = len(para)
    if len(para) == 0:
        return fetch(sql)
    else:
        sql += ' where '
        for i in range(length):
            if i != length - 1:
                sql += para[i]
                sql += ' and '
            else:
                sql += para[i]
        return fetch(sql)
  

def one_company(comName):
    sql = f'''select Theater.thName, concat(firstname," ",lastname) as "manager", 
            thCity, thState, capacity from Theater natural join Employee join user on Employee.username = user.username 
            where Theater.comName = "{comName}"
        '''
    return fetch(sql)
def certain_employee(comName):
    cursor = mysql.get_db().cursor()
    cursor.execute(f'select concat(firstname," ",lastname) as "manager" from user where username in (SELECT username FROM Employee where employeeType = "Manager" and comName = "{comName}");' )
    result = cursor.fetchall()
    cursor.close()
    return result