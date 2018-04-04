# Uitwerking van queries 1-4
# add commit pull push
# author Jasper Vanmeerbeeck

import json
import getpass
# import mysql.connector
import numpy as np
import os
import pandas as pd
import sys


def query_01(connection, column_names):
    # Het resultaat van deze functie is een Pandas dataframe met:
    # de teamnaam, het jaar, en het aantal homeruns per team,
    # en dit voor alle teams,
    # gesorteerd op aantal homeruns van hoog naar laag.
    query = SELECT b.TeamName, b.year, SUM(b.HR)
            FROM batting as b
            ORDER BY SUM(b.HR)


    # make_connection_databank()

    df = execute_plot_query(connection, query, column_names)

    return df


def query_02(connection, column_names, datum='1980-01-16'):
    # Het resultaat van deze functie is een Pandas dataframe met:
    # de voornaam, achternaam, geboortejaar, geboortemaand, geboortedag van
    # spelers die hun eerste major league appearance maakten na een gegeven datum.

    # De tabel is oplopend alfabetisch gesorteerd op achternaam.
    query = SELECT a.playerID, a.yearID
            FROM allstarfull as a
            WHERE
            ORDER BY

    # make_connection_databank()

    df = execute_plot_query(connection, query, column_names)

    return df


def query_03(connection, column_names):
    # Bouw je query
    query = """
    MAAK QUERY HIER
    """
    make_connection_databank()

    # df = execute_plot_query(connection, query, column_names)

    return df


def query_04(connection, column_names, datum_x='1980-01-01', datum_y='1980-01-01'):
    # Bouw je query
    query = """
    MAAK QUERY HIER
    """
    make_connection_databank()

    df = execute_plot_query(connection, query, column_names)

    return df




def execute_plot_query(connection,query,column_names):
    # Stap 2 & 3
    res = run_query(connection, query)  # Query uitvoeren
    df = res_to_df(res, column_names)  # Query in DataFrame brengen
    return df

def make_connection_databank():
    # Eerst verbinding maken met de databank
    username = 'root'
    hostname = 'localhost'
    db = 'lahman2016'
    c = verbind_met_GB(username, hostname, db)





### mag weg zelle gewoon effe voor mijn eigen
def verbind_met_GB(username, hostname, gegevensbanknaam):
    password = getpass.getpass() # Genereer vakje voor wachtwoord in te geven

    connection = mysql.connector.connect(host=hostname,
                                         user=username,
                                         passwd=password,
                                         db=gegevensbanknaam)
    return connection


def run_query(connection, query):
    # Making a cursor and executing the query
    cursor = connection.cursor()
    cursor.execute(query)

    # Collecting the result and casting it in a pd.DataFrame
    res = cursor.fetchall()

    return res


def res_to_df(query_result, column_names):

    df = pd.DataFrame(query_result, columns=column_names)
    return df
