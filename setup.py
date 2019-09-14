#!/usr/bin/env python3
import mysql.connector, sys
from mysql.connector import errorcode

DB_TABLES = {}
DB_TABLES['rssbot2_feeds'] = (
    "CREATE TABLE IF NOT EXISTS `rssbot2_feeds` ("
    "  `id` int(11) PRIMARY KEY AUTO_INCREMENT,"
    "  `title` varchar(255) NOT NULL,"
    "  `link` varchar(255) NOT NULL,"
    "  `active` char(1) DEFAULT 'N',"
    "  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,"
    "  CONSTRAINT unique_link UNIQUE (link)"
    ") ENGINE=InnoDB")

DB_TABLES['rssbot2_archive'] = (
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
        for table_name in DB_TABLES:
            table_description = DB_TABLES[table_name]
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
opts, args = getopt.getopt(argv,"h:d:u:p:",["host=","username=","password=","database=","--help"])
for opt, arg in opts:
    if opt == '--help':
        print('For user-guided install, run:')
        print('setup.py')
        print('For user-directed install, run:')
        print('setup.py -h <hostname> -u <username> -p <password> -d <database>')
        sys.exit()
    elif opt in ("-u", "--username"):
        username = arg
    elif opt in ("-p", "--password"):
        password = arg
    elif opt in ("-h", "--hostname"):
        hostname = arg
    elif opt in ("-d", "--database"):
        database = arg

if hostname == None:
    hostname = input("Enter your database hostname/ip: ")

if username == None:
    username = input("Enter your database user name: ")

if password == None:
    password = input("Enter your database user password: ")

if database == None:
    database = input("Enter your database schema name to create, or use existing: ")

# write config.py file programmaticlly
# old-school string type handler. need to modernize this using format() or json encoding.
config_file = open("config.py","w+")
config_file.write("db = {\n\t'user': '%s',\n\t'password': '%s',\n\t'host': '%s',\n\t'database': '%s',\n\t'raise_on_warnings': True\n}\n" % (username, password, hostname, database))
config_file.close()

# @todo add sanity checks before proceeding to setup class procedures.
# run setup class.
setup = setup({"host": hostname, "database": database, "user": username, "password": password})
setup.create_database(database)
setup.create_tables()
