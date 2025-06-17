import psycopg2
from contextlib import contextmanager 

class PSQL_DB():
    """ Collection of helper methods to query the Postgres database.
    
    Example::
    
    	ms_db = MS_DB(username='my_user', password='my_secret', host='hostname')
		with ms_db.cursor() as cursor:
        	cursor.execute("SELECT @@version;")
        	print(cur.fetchall()) 
    """

    def __init__(self, username="postgres", password=None, host="localhost", port=5432, initial_db='rc_test'):
        self.username = username
        self._password = password
        self.host = host
        self.port = str(port)
        self.db = initial_db        
        self._connection = psycopg2.connect(
			host=host,
			database=initial_db,
			user=username,
			password=password,
		)
        print('INFO - Connected to DB:', self.__repr__)
        self._connection.autocommit = True

    def __repr__(self):
        return f"Postgres('{self.username}', <password hidden>, '{self.host}', '{self.port}', '{self.db}')"

    def __str__(self):
        return f"Postgres on {self.host}"

    def __del__(self):
        self._connection.close()
        print("Connection closed.")

    @contextmanager
    def cursor(self, commit: bool = False):
        """
        A context manager style of using a DB cursor for database operations. 
        This function should be used for any database queries or operations that 
        need to be done. 

        :param commit:
        A boolean value that says whether to commit any database changes to the database. Defaults to False.
        :type commit: bool
        """
        cursor = self._connection.cursor()
        try:
            yield cursor
        except psycopg2.DatabaseError as err:
            print(f"== ERROR - DatabaseError: {err} ")
            #print(f"{err.diag=} {err.pgcode=} {err.pgerror=}") 
            self._connection.rollback()
            raise err
        else:
            if commit:
                self._connection.commit()
        finally:
            cursor.close()
            print('== INFO - cursor and connection CLOSED.')
