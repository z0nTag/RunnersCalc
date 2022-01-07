import hashlib
import sqlite3
import stdiomask

conn = sqlite3.connect('runners.db')
c = conn.cursor()


class Database:

    def __init__(self, username, password):
        self.username = username
        self.password = password


def register():
    while True:
        username = input("User name: ").encode('utf-8')
        c.execute("select username from users where username = ?", (username,))
        row = c.fetchone()
        try:
            db_username = row[0]
        except Exception as e:
            db_username = ""
            break
        break

    while db_username == username:
        print("Username is already taken. Please choose a new username:\n")
        username = input("User name: ").encode('utf-8')
        c.execute("select username from users where username = ?", (username,))
        row = c.fetchone()
        try:
            db_username = row[0]
        except Exception as e:
            db_username = ""
            break

    txt_password = stdiomask.getpass()
    txt_password2 = stdiomask.getpass("Re-enter password: ")

    while txt_password2 != txt_password:
        print("Passwords did not match. Please re-enter passwords.\n")
        txt_password = stdiomask.getpass()
        txt_password2 = stdiomask.getpass()

    txt_password = txt_password.encode('utf-8')
    password = hashlib.sha256(txt_password).hexdigest()

    c.execute("insert into users (username, password) values (?, ?)", (username, password))
    conn.commit()
    conn.close()


def login():
    count = 5
    while True and count > 0:
        typed_user = input("Login: ").encode('utf-8')
        typed_pass = stdiomask.getpass().encode('utf-8')
        typed_hash = hashlib.sha256(typed_pass).hexdigest()

        c.execute('SELECT username, password FROM users WHERE Username = ?', (typed_user,))

        row = c.fetchone()
        if row is None:
            print("Account not found. Please try again\n")
            count -= 1
            print(count, " numbers of login attempts remaining", sep='')
            continue
        else:
            fetched_hash = row[1]

            if fetched_hash == typed_hash:
                print("Login Success")
                break
            else:
                print("Login Failed. Please try again")
                count -= 1
                print(count, " numbers of login attempts remaining", sep='')

                continue

    if count <= 0:
        print("Maximum number of login attempts exceeded")
        exit()
    else:
        return True


def delete_user():

    while True:
        typed_user = input("Enter name of user to delete: ").encode('utf-8')
        c.execute("select username from users where username = ?", (typed_user,))
        row = c.fetchone()
        try:
            fetched_hash = row[0]
        except Exception as e:
            print("User ", str(typed_user).removeprefix("b"), " not found", sep='')
            exit()
        break

    c.execute('SELECT id, username, password FROM users WHERE Username = ?', (typed_user,))
    row = c.fetchone()
    fetched_hash = row[2]
    fetched_id = row[0]

    typed_pass = stdiomask.getpass().encode('utf-8')
    typed_pass2 = stdiomask.getpass().encode('utf-8')

    while typed_pass != typed_pass2:
        print("Passwords did not match. Please re-enter passwords.\n")
        typed_pass = stdiomask.getpass().encode('utf-8')
        typed_pass2 = stdiomask.getpass().encode('utf-8')

    typed_hash = hashlib.sha256(typed_pass).hexdigest()

    count = 4
    while count > 0:

        if fetched_hash == typed_hash:
            # delete user
            try:
                c.execute('DELETE FROM users WHERE id =?', (fetched_id,))
                conn.commit()
                conn.close()
            except Exception as e:
                print("Could not delete user. Error: ", e, sep='', end='\n')
                break
            print("User ", typed_user, " deleted", sep='', end='\n')
            break

        else:
            print("Incorrect password or ")
            print(count, " numbers of attempts remaining", sep='')
            count -= 1

        typed_pass = stdiomask.getpass().encode('utf-8')
        typed_pass2 = stdiomask.getpass().encode('utf-8')
        while typed_pass != typed_pass2:
            print("Passwords did not match. Please re-enter passwords.\n")
            typed_pass = stdiomask.getpass().encode('utf-8')
            typed_pass2 = stdiomask.getpass().encode('utf-8')
        typed_hash = hashlib.sha256(typed_pass).hexdigest()

    if count <= 0:
        print("Maximum number of attempts exceeded")
        exit()

    return True
