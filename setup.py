#!/usr/bin/env python3
import mysql.connector
from mysql.connector import errorcode

TABLES = {}
TABLES['rssbot2_feeds'] = (
    "CREATE TABLE IF NOT EXISTS `rssbot2_feeds` ("
    "  `id` int(11) PRIMARY KEY AUTO_INCREMENT,"
    "  `title` varchar(255) NOT NULL,"
    "  `link` varchar(255) NOT NULL,"
    "  `active` char(1) DEFAULT 'N',"
    "  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,"
    "  CONSTRAINT unique_link UNIQUE (link)"
    ") ENGINE=InnoDB")

TABLES['rssbot2_archive'] = (
    "CREATE TABLE IF NOT EXISTS `rssbot2_archive` ("
    "  `id` int(11) PRIMARY KEY AUTO_INCREMENT,"
    "  `title` varchar(255) NOT NULL,"
    "  `link` varchar(255) NOT NULL,"
    "  `feed_id` int(11) NOT NULL,"
    "  `active` char(1) DEFAULT 'N',"
    "  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,"
    "  CONSTRAINT unique_link UNIQUE (link), KEY `feed_id` (`feed_id`)"
    ") ENGINE=InnoDB")

class setup:
    def __init__(self,creds):
        self.conn = mysql.connector.connect(**creds)

    def create_database(self,schema):
        cursor = self.conn.cursor()
        try:
            print("CREATE DATABASE IF NOT EXISTS {}\n". format(schema), end='')
            cursor.execute("CREATE DATABASE IF NOT EXISTS {} ". format(schema))
        except mysql.connector.Error as err:
            print("Failed creating database {}: ". format(schema), end='') 
            print("Error output {}: ". format(err.msg), end='')
            #exit(1)

    def create_tables(self):
        cursor = self.conn.cursor()
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("The table {} already exists".format(table_name), end='')
                else:
                    print(err.msg)
            else:
                print("OK")
        cursor.close()
        self.conn.close()

# let user define db credentials via input

host = input("Enter your database hostname/ip: ")
username = input("Enter your database user name: ")
password = input("Enter your database user password: ")
database = input("Enter your database schema name to create, or use existing: ")

# write config.py file programmaticlly
config_str = "config = {\n\t'user': '{0}',\n\t'password': '{1}',\n\t'host': '{2}',\n\t'database': '{3}',\n\t'raise_on_warnings': True\n}\n". format(username, password, host, database)
config_file = open("config.py","w+")
config_file.write(config_str)
config_file.close()

# @todo add sanity checks before proceeding to setup class procedures.
# run setup class.
setup = setup({"host": host, "database": database, "user": username, "password": password})
setup.create_database(database)
setup.create_tables()
