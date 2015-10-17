__author__ = 'e36'

from sqlalchemy import create_engine



def connect_to_db(dbsettings):

    """
    Connects to a database.
    :param dbsettings: a configparser dict with all necessary connection information
    :return: a sqlalchemy.engine object
    """

    # build connection string
    # engine://user:pass@host/database
    connection_string = dbsettings['engine'] + "://" + dbsettings['username'] + ":" + dbsettings['password'] + "@" + dbsettings['hostname'] + ":" + dbsettings['port'] + "/" + dbsettings['dbname']
    print(connection_string)

    # create engine object
    engine = create_engine(connection_string)

    return engine