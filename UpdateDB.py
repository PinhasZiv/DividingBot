import mysql.connector
from mysql.connector import Error
import Constants


def get_expense_sum(message_text, context):
    ret = ''
    # validate that the user entered only integer or float.
    try:
        context.user_data['expense']['amount'] = float(message_text)
        context.user_data['state'] = 1
        ret = True
    except Error as e:
        print(e)
        ret = False
    finally:
        return ret


def get_expense_reason(message_text, context):
    context.user_data['expense']['reason'] = message_text
    # updating state after adding data to DB (in main)


def add_expense(user_id, chat_id, message_id, amount, reason, timestamp):
    ret = ""
    try:
        connection = mysql.connector.connect(host=Constants.MYSQL_DB['host'],
                                             database=Constants.MYSQL_DB['database'],
                                             user=Constants.MYSQL_DB['user'],
                                             password=Constants.MYSQL_DB['password'])
        if connection.is_connected():
            mySql_insert_query = """INSERT INTO distributions (UserID, ChatID, Amount, Reason, MessageID, Timestamp) 
                                      VALUES 
                                      (%s, %s, %s, %s, %s, %s)"""
            data_to_insert = (user_id, chat_id, amount, reason, message_id, timestamp)
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute(mySql_insert_query, data_to_insert)
            connection.commit()
            record = cursor.fetchone()
            print(cursor.rowcount)
            print("You're connected to database: ", record)
            ret = "added successfully!"
    except Error as e:
        print("Error while connecting to MySQL", e)
        ret = 'an error occurred!'
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        return ret


def get_expenses_list(context):
    ret = ""
    try:
        connection = mysql.connector.connect(host=Constants.MYSQL_DB['host'],
                                             database=Constants.MYSQL_DB['database'],
                                             user=Constants.MYSQL_DB['user'],
                                             password=Constants.MYSQL_DB['password'])
        if connection.is_connected():
            users_list = context.chat_data['users_list']
            users_sum = {}
            for user in users_list:
                print('user:', user)
                mySql_select_query = """SELECT UserID, Amount FROM distributions WHERE UserID = 190866836"""
                mySql_select_sum_query = """SELECT SUM(Amount) AS sum FROM distributions WHERE UserID = {user: d}""".format(user=user)
                print(mySql_select_sum_query.format(user=user))
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()
                cursor.execute(mySql_select_sum_query)
                result = cursor.fetchone()
                print("Result: ", result)
                users_sum[user] = result[0]
            ret = "calculated successfully!"
            print(users_sum)
    except Error as e:
        print("Error while connecting to MySQL", e)
        ret = 'an error occurred!'
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        if 'error' in ret:
            return ret
        return users_sum


# return dict of {userID -> balance}. positive balance = receiver, negative balance = debtor)
def get_members_balance(expenses_dict):
    sum_expenses = sum(expenses_dict.values())
    breakeven_point = sum_expenses / len(expenses_dict)
    balances_dict = {}

    for user in expenses_dict:
        balances_dict[user] = expenses_dict[user] - breakeven_point

    print('sum:', sum_expenses)
    print('breakpoint:', breakeven_point)
    print(balances_dict)

    return balances_dict

