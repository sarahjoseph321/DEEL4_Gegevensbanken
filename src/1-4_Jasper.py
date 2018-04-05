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
    query = SELECT t.name, t.yearID, SUM(t.HR)
            FROM teams as t
            ORDER BY SUM(t.HR)


    # make_connection_databank()

    df = execute_plot_query(connection, query, column_names)
    #TODO het is oke
    return df


def query_02(connection, column_names, datum='1980-01-16'):
    # Het resultaat van deze functie is een Pandas dataframe met:
    # de voornaam, achternaam, geboortejaar, geboortemaand, geboortedag van
    # spelers die hun eerste major league appearance maakten na een gegeven datum.
    # De tabel is oplopend alfabetisch gesorteerd op achternaam.

    query = SELECT m.nameFirst, m.nameLast, m.birthYear, m.birthMonth, m.birthDay,
            FROM master as m
            WHERE m.debut > datum
            ORDER BY m.nameLast DESC

    # make_connection_databank()

    df = execute_plot_query(connection, query, column_names)
    #TODO het is oke
    return df


def query_03(connection, column_names):
    # Het resultaat van deze functie is een Pandas dataframe dat per club:
    # de clubnaam en de voor- en achternaam van alle managers weergeeft,
    # die ooit voor de club gewerkt hebben als niet-playermanager.
    # Per club mag een welbepaalde manager slechts 1 keer in het resultaat voorkomen.
    # Sorteer oplopend alfabetisch op clubnaam.

    query = SELECT DISTINCT t.name, ma.nameFirst, ma.nameLast
            FROM Managers as m
                JOIN MASTER as ma ON m.playerID =  ma.playerID
                JOIN Teams as t ON m.teamID = t.teamID
            WHERE m.plyrMgr = 'N';
            ORDER t.name
    make_connection_databank()
    #TODO het is oke
    # df = execute_plot_query(connection, query, column_names)

    return df


def query_04(connection, column_names, datum_x='1980-01-01', datum_y='1980-01-01'):
    # Het resultaat van deze functie is een Pandas dataframe met gegevens van teams:
    # (teamnaam, rang, aantal wins en losses) en van managers:
    # (voor- en achternaam) zodanig dat

    # de desbetreffende manager is opgenomen in de hall of fame na datum x
    # de manager in kwestie was ooit, na datum y, manager van het team in kwestie
    # De tabel moet gesorteerd zijn op teamnaam en rang (alfabetisch oplopend).
    query = SELECT t.name, t.Rank, t.W, t.L, ma.nameFirst, ma.nameLast
            FROM Managers as m
                JOIN HallOfFame as h ON m.playerID = h.playerID
                JOIN Teams as t ON m.teamID = t.teamID
                JOIN MASTER as ma ON m.playerID = ma.playerID
            WHERE h.YearID > datum_x AND t.yearID > datum_y
    make_connection_databank()

    #TODO het is oke
    # df = execute_plot_query(connection, query, column_names)

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
