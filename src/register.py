from utils import execute_proc, fetch

def check_username(username):
    result = fetch(f'select * from user where username="{username}"')
    return len(result) > 0

def check_password(passwd1, passwd2):
    return passwd1 != passwd2

def check_password_length(passwd1):
    return len(passwd1) < 8

def check_creditcard(creditcard):
    print(creditcard)
    if isinstance(creditcard, list):
        for x in creditcard:
            if len(x) != 16:
                return True
    else:
        if len(creditcard) != 16:
                return True
    return False

def check_zipcode(zipcode):
    return len(zipcode) != 5

def register_user(form_data):
    error = None
    error = check_password(form_data['password'], form_data['password1'])
    if error:
        return 'Passwords do not match'
    if check_password_length(form_data['password']):
        return 'Password must be at least 8 characters'
    error = check_username(form_data['username'])
    if error:
        return 'User already exists'
    execute_proc('user_register', (form_data['username'], form_data['password'],form_data['first_name'], form_data['last_name']))
    return error

def register_customer(form_data):
    error = None
    error = check_password(form_data['password'], form_data['password1'])
    if error:
        return 'Passwords do not match'
    if check_password_length(form_data['password']):
        return 'Password must be at least 8 characters'
    error = check_username(form_data['username'])
    if error:
        return 'User already exists'
    error = check_creditcard(form_data.getlist('creditcard[]'))
    if error:
        return 'Credit card number cannot exceed 16 digits'
    execute_proc('customer_only_register', (form_data['username'], form_data['password'], form_data['first_name'], form_data['last_name']))
    for credictcard_num in form_data.getlist('creditcard[]'):
        if credictcard_num:
            execute_proc('customer_add_creditcard', (form_data['username'], credictcard_num))
    
def register_manager(form_data):
    error = None
    error = check_password(form_data['password'], form_data['password1'])
    if error:
        return 'Passwords do not match'
    error = check_username(form_data['username'])
    if check_password_length(form_data['password']):
        return 'Password must be at least 8 characters'
    if error:
        return 'User already exists'
    error = check_zipcode(form_data['zipcode'])
    if error:
        return 'Zipcode needs to be 5 digits'
    execute_proc('manager_only_register', (form_data['username'],form_data['password'],form_data['first_name'], form_data['last_name'], form_data['company'], form_data['streetaddress'], form_data['city'], form_data['state'], form_data['zipcode']))


def register_customermanager(form_data):
    error = None
    error = check_password(form_data['password'], form_data['password1'])
    if error:
        return 'Passwords do not match'
    if check_password_length(form_data['password']):
        return 'Password must be at least 8 characters'
    error = check_username(form_data['username'])
    if error:
        return 'User already exists'
    error = check_creditcard(form_data['creditcard[]'])
    if error:
        return 'Credit card number cannot exceed 16 digits'
    error = check_zipcode(form_data['zipcode'])
    if error:
        return 'Zipcode needs to be 5 digits'
    execute_proc('manager_customer_register', (form_data['username'],form_data['password'],form_data['first_name'], form_data['last_name'], form_data['company'], form_data['streetaddress'], form_data['city'], form_data['state'], form_data['zipcode']))
    for credictcard_num in form_data.getlist('creditcard[]'):
        if credictcard_num:
            execute_proc('customer_add_creditcard', (form_data['username'], credictcard_num))