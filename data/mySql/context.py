from contextlib import contextmanager


@contextmanager
def get_cursor(connection):
        try:
            connection.start_transaction()
            cursor = connection.cursor()
            yield cursor
        except Exception as err:
            print("Something went wrong: {}".format(err))
            connection.rollback()
        finally:
            connection.commit()
            cursor.close()
            connection.close()
