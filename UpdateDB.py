import mysql.connector
from mysql.connector import Error
import Constants


def getExpenseSum(message_text, context):
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


def getExpenseReason(message_text, context):
    context.user_data['expense']['reason'] = message_text
    # updating state after adding data to DB (in main)


def addExpense(user_id, chat_id, message_id, amount, reason, timestamp):
    ret = ""
    try:
        connection = mysql.connector.connect(host=Constants.MYSQL_DB['host'],
                                             database=Constants.MYSQL_DB['database'],
                                             user=Constants.MYSQL_DB['user'],
                                             password=Constants.MYSQL_DB['password'])
        if connection.is_connected():
            mySql_insert_query = """INSERT INTO distributions (UserID, ChatID, Amount, Reason, MessageID, Timestamp) 
                                      VALUES 
                                      (%s ,%s, %s, %s, %s, %s)"""
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

def get_calculation():
    ret = ""
    try:
        connection = mysql.connector.connect(host=Constants.MYSQL_DB['host'],
                                             database=Constants.MYSQL_DB['database'],
                                             user=Constants.MYSQL_DB['user'],
                                             password=Constants.MYSQL_DB['password'])
        if connection.is_connected():
            # need to add code here
            pass
    except Error as e:
        print("Error while connecting to MySQL", e)
        ret = 'an error occurred!'
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")