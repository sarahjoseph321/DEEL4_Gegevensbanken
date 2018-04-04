# Uitwerking van queries 5-7
import mysql.connector
import getpass      # Package om een paswoordveldje te genereren.
import pandas as pd # Populaire package voor data-verwerking


def verbind_met_GB(username, hostname, gegevensbanknaam):
    """
    Maak verbinding met een externe gegevensbank

    :param  username:          username van de gebruiker, string
    :param  hostname:          naam van de host, string.
                               Dit is in het geval van een lokale server gewoon 'localhost'
    :param  gegevensbanknaam:  naam van de gegevensbank, string.
    :return connection:        connection object, dit is wat teruggeven wordt
                               door connect() methods van packages die voldoen aan de DB-API
    """

    # password = getpass.getpass()  # Genereer vakje voor wachtwoord in te geven
    password = 'test'
    connection = mysql.connector.connect(host=hostname,
                                         user=username,
                                         passwd=password,
                                         db=gegevensbanknaam)

    return connection


def res_to_df(query_result, column_names):
    """
    Giet het resultaat van een uitgevoerde query in een 'pandas dataframe'
    met vooraf gespecifieerde kolomnamen.

    Let op: Het resultaat van de query moet dus exact evenveel kolommen bevatten
    als kolomnamen die je meegeeft. Als dit niet het geval is, is dit een indicatie
    dat je oplossing fout is. (Gezien wij de kolomnamen van de oplossing al cadeau doen)

    """

    ####  EXAMPLE QUERY BIJNA AF, MOET ENKEL DATA JUIST IN DE PANDAS DATAFRAME GIETEN ####
    df = pd.DataFrame(query_result, columns=column_names)


    # return df


def query_EX(connection, column_names, homeruns=20):
    # Bouw je query
    query = """
    select t.name, t.yearID, t.HR
    from Teams as t
    where t.HR > {};
    """.format(homeruns)  # TIP: Zo krijg je parameters in de string (samen met `{}` in de string)


    # Stap 2 & 3
    res = run_query(connection, query)  # Query uitvoeren
    df = res_to_df(res, column_names)  # Query in DataFrame brengen
    #
    return df

def run_query(connection, query):
    """
    Voer een query uit op een reeds gemaakte connectie, geeft het resultaat van de query terug
    """

    # Making a cursor and executing the query
    cursor = connection.cursor()
    cursor.execute(query)

    # Collecting the result and casting it in a pd.DataFrame
    res = cursor.fetchall()

    print(res)
    print(len(res))

    return res

def main():

    username = 'Sarah'      # Vervang dit als je via een andere user queries stuurt
    hostname = 'localhost' # Als je een databank lokaal draait, is dit localhost.
    db = 'lahman2016'      # Naam van de gegevensbank op je XAMPP Mysql server

    # We verbinden met de gegevensbank
    c = verbind_met_GB(username, hostname, db)
    query_EX(c, 'lahman2016', homeruns=260)

main()