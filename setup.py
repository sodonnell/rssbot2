#!/usr/bin/env python3
import mysql.connector, config
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
    def __init__(self):
        self.conn = mysql.connector.connect(**config)

    def create_database(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("CREATE DATABASE IF NOT EXISTS ". config.database)
        except mysql.connector.Error as err:
            print("Failed creating database: ". config.database) 
            print("Error output: ". format(err))
            exit(1)

    def create_tables(self):
        cursor = self.conn.cursor()
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("The table already exists")
                else:
                    print(err.msg)
            else:
                print("OK")
        cursor.close()
        self.conn.close()

# let user define db credentials via input
config = []
config.host = input("Enter your database hostname/ip: ")
config.username = input("Enter your database user name: ")
config.password = input("Enter your database user password: ")
config.database = input("Enter your database schema name to create, or use existing: ")

# write config.py file programmaticlly
config_file = open("config.py","w+")
config_file.write("config = {\n\t'user': '%s',\n\t'password': '%s',\n\t'host': '%s',\n\t'database': '%s',\n'raise_on_warnings': True\n}" % config.username, config.password, config.host, config.database)
config_file.close()

# @todo add sanity checks before proceeding to setup class procedures.
# run setup class.
setup = setup()
setup.create_database()
setup.create_tables()
