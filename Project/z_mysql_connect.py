# -*- coding: utf-8 -*-
import mysql.connector 
import pandas as pd
import sys
import os
import json
import sqlalchemy
# Establish a connection to the MySQL server

def connection(config):

    cnx = mysql.connector.connect(
    host=config["host"],
    port = config["port"],
    user=config["user"],
    password=config["password"],
    database=config["database"],
    # multi=True  # Add the multi=True parameter
    )

    return cnx

if __name__=="__main__":
    with open("RULE_ENGINE\config.json") as f:
        config = json.load(f)
    cnx = connection(config)

