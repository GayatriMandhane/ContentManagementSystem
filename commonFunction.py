
import json
import re

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
password_regex = r'^(?=.*[a-z])(?=.*[A-Z]).{8,}$'
phone_regex = r'^\d{10}$'
pincode_regex = r'^\d{6}$'


def validateRegex(data,type): 
    if type == 'email':
        if(re.fullmatch(email_regex, data)):
            return 1
    elif type == 'password': 
        if(re.fullmatch(password_regex, data)):
            return 1   
    elif type == 'phone':
        if(re.fullmatch(phone_regex, data)):
            return 1
    elif type == 'pincode':
        if(re.fullmatch(pincode_regex, data)):
            return 1
    else:
        return 0

def required_validation(request,array):
    body = json.loads(request.body)
    check = True
    not_available = []
    for i in array:
        if not body.get(i):
            not_available.append(i)
            check = False

    not_aval = str(not_available)[1:-1]

    return check, not_aval

def validate_len(strr,length):
            if len(strr)<= length:
                return True
            else:
                return False

