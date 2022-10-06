import sqlite3
import hashlib
import random
import string
import json


try:
    f = open('config.json')
    data = json.load(f)

    public_key = data['public_key']
    salt_len = data['salt_len']

    f.close()
except:
    #default settings in case of any failure during reading the config file.
    public_key = "SDKAFHJSDAKLHSDAJKFHASJKFHASDJKFHASDK"
    salt_len = 8
    print("default settings are applied")

#intiating connection to the db
con = sqlite3.connect('passwords.db')
cur = con.cursor()

def create_table():
    try:
        cur.execute("CREATE TABLE USERS(id INTEGER PRIMARY KEY, username, password)")
    except:
        print('Table already exists')

def insert(username, password):
    to_be_inserted = "INSERT INTO USERS (username, password) VALUES ('{}','{}')".format(username, password)
    cur.execute(to_be_inserted)
    con.commit()


# Just to examine the encryption. Not used.
def decrypt(encrypted):
    if( type(encrypted) == str):
        encrypted = encrypted.encode('utf-8')
    key = public_key.encode('utf-8')
    decrypted = ""
    i = 0
    for byte in encrypted:
        xor_result = (byte-33) ^ key[i]
        decrypted += chr(xor_result)
        i += 1
    return decrypted


def encrypt(text):
    #Using block encryption. 8 bits per time
    key = public_key
    #Make sure that the key length is bigger than the text
    while(len(key) <= len(text)):
        key += key
    
    #converting the strings to bytes so that we can iterate over them and XOR the bytes.
    text = (text.encode('utf-8'))
    key = public_key.encode('utf-8')
    encrypted = ""
    i = 0

    for byte in text:
        xor_result = byte ^ key[i]
        encrypted += chr(xor_result+33)
        i += 1

    return encrypted

def swapBounds(string):
    string = list(string)

    first_char = string[0]
    last_char = string[len(string) - 1]
    string[0] = last_char
    string[len(string) - 1] = first_char
    return "".join(string)

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def salt(encrypted_password):
    encrypted_password = swapBounds(encrypted_password)
    encrypted_password += get_random_string(salt_len)
    return encrypted_password

def remove_salt(salted_password):
    return swapBounds(salted_password[0: len(salted_password) - salt_len])

def user_exists(username):
    if(len (cur.execute("select * from USERS where username = '{}' ".format(username)).fetchall()) > 0):
        return True
    return False

def compare_passwords(username, inputted_password):
    res = cur.execute("select password from USERS where username = '{}' ".format(username))
    encrypted_password = res.fetchall()[0][0]
    if(encrypt(inputted_password) == remove_salt(encrypted_password)):
        print("Welcome To Your Account !")
    else:
        print("Wrong Password")


def viewUsers():
    cur.execute("select * from USERS")
    users = cur.fetchall()
    for user in users:
        print(user)


def startApp():
    create_table()


    gonna_do = input('Press anything except ENTER to sign in/up')
    if(gonna_do == ''):
        viewUsers()

    else:
        username = input("Username: ")
        while(username == ''):
            username = input("Username: ")


        password = input("Password: ")
        while(password == ''):   
            password = input("Password: ")


    
        if(user_exists(username)):
            print("User exists")
            compare_passwords(username, password)

        else:
            encrypted_password = salt(encrypt(password))

            insert(username, encrypted_password)

    con.close()

startApp()