#!/usr/bin/env python3
import mysql.connector, config
from mysql.connector import errorcode

TABLES = {}
TABLES['rssbot2_feeds'] = (
    "CREATE TABLE `rssbot2_feeds` ("
    "  `emp_no` int(11) NOT NULL,"
    "  `salary` int(11) NOT NULL,"
    "  `from_date` date NOT NULL,"
    "  `to_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`,`from_date`), KEY `emp_no` (`emp_no`),"
    "  CONSTRAINT `salaries_ibfk_1` FOREIGN KEY (`emp_no`) "
    "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['rssbot2_archive'] = (
    "CREATE TABLE `rssbot2_archive` ("
    "  `emp_no` int(11) NOT NULL,"
    "  `salary` int(11) NOT NULL,"
    "  `from_date` date NOT NULL,"
    "  `to_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`,`from_date`), KEY `emp_no` (`emp_no`),"
    "  CONSTRAINT `salaries_ibfk_1` FOREIGN KEY (`emp_no`) "
    "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

class setup:
    def __init__(self):
        self.conn = mysql.connector.connect(**config)

    def create_database(self,cursor):
        cursor = self.conn.cursor()
        try:
            cursor.execute("CREATE DATABASE ". config.database ." IF NOT EXISTS")
        except mysql.connector.Error as err:
            print("Failed creating database: ". config.database .") 
            print ("Error output: ". format(err))
            exit(1)