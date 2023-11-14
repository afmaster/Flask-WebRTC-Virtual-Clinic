import sqlite3
from prettytable import from_db_cursor
import base64

from typing import List, Union, Tuple
from datetime import datetime

""" FUNCTIONS: """

"""
db_tricks.search_db(db_file, db, field, criteria)
db_tricks.search_entire_db(db_file, db, field, criteria)
db_tricks.search_db_with_two_criteria(db_file, db, field1, criteria1, field2, criteria2)
db_tricks.search_row(db_file, db, field, criteria)
db_tricks.fetch_column_names(db_file, db)
db_tricks.search_cell(db_file, db, field, criteria, column)
db_tricks.search_simple_table_cell(db_file, db, column)
db_tricks.return_pair_field_value(db_file, db, field, criteria)
db_tricks.search_row_with_two_criteria(db_file, db, field1, criteria1, field2, criteria2)
db_tricks.fetch_entire_table(db_file, db)
db_tricks.fetch_ordered_table(db_file, db, field)
db_tricks.fetch_all_col(db_file, db, field)
db_tricks.add_new_col(db_file, db, field)
db_tricks.add_new_populated_col(db_file, db, field, fill)
db_tricks.delete_entry(db_file, db, field, criteria)
db_tricks.delete_entry_with_two_criteria(db_file, db, field1, criteria1, field2, criteria2)
db_tricks.delete_all_rows(db_file, db)
db_tricks.delete_column(db_file, db, field)
db_tricks.delete_table(db_file, db)
db_tricks.create_db(db_file, db, dic)
db_tricks.create_db_with_id(db_file, db, id_name, dic)
db_tricks.update_db(db_file, db, field, criteria, dic)
db_tricks.add_entry(db_file, db, dic)
insert_into_single_column_table(db_file, db, field, new_value)
db_tricks.change_row(db_file, db, field, criteria, dic)
db_tricks.change_row_with_two_criteria(db_file, db, field1, criteria1, field2, criteria2, dic)
db_tricks.update_cell(db_file, db, field, criteria, column_name, new_value)
db_tricks.update_or_create_empty_row(db_file, db, field, criteria, column_name, new_value)
db_tricks.check_or_create_empty_row(db_file, db, field, criteria)
db_tricks.create_empty_table(db_file, db, fields_list)
db_tricks.create_filled_row(db_file, db, field, criteria, cells_value)
db_tricks.update_or_create_column(db_file,db,field,criteria,new_field,new_value)
db_tricks.update_or_create_column_for_complex_table(db_file, db, field, criteria, column_name, new_value)
update_cell_in_simple_table(db_file, db, field, criteria, new_value)
visualize_db(db_file, db)

"""


# Ajust dict to be used in sqlite functions

def ajust_to_sql(par):
    str_par = str(par)
    parsed_par = str_par.replace("'", '"')
    return parsed_par


def search_db(db_file: str, db: str, field: str, criteria: str) -> str or None:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    try:
        c.execute(f"SELECT destination FROM {db} WHERE {field}='{criteria}'")
        results = c.fetchone()
        item = results[0]

        c.close()
        conn.close()
        return item
    except Exception as err:
        c.close()
        conn.close()
        return None


# RETRIEVE ALL THE LINES CONTAINING A CRITERIA INSIDE A COLUMN

def search_entire_db(db_file: str, db: str, field: str, criteria: str) -> list or None:
    """
    Searches an entire SQLite database for records where a specific field matches a specific criterion.

    Args:
        db_file (str): The path to the SQLite database file.
        db (str): The name of the database to search.
        field (str): The name of the field to search in each record.
        criteria (str): The criterion to match in the field. The function will return any record where the field
        contains this string.

    Returns:
        list or None: A list of tuples representing the matching records. Each tuple corresponds to a record, and each
        element in a tuple corresponds to a field in the record.
        If an error occurs, the function will return None.

    This function uses the LIKE keyword in the SQL query to perform a case-insensitive search in the specified field.
    The '%' symbols before and after the criterion mean that the function will match any field that contains the
    criterion anywhere in its text.

    The function connects to the SQLite database using the sqlite3 module, sends the SQL query, and fetches all results.
    It then closes the connection and returns the results.
    If any error occurs during this process, the function will close the connection and return None.
    """
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    try:
        c.execute(f"SELECT * FROM {db} WHERE {field} LIKE '%{criteria}%'")
        results = c.fetchall()
        # item = results[0]
        c.close()
        conn.close()
        return results
    except:
        c.close()
        conn.close()
        return None


def search_db_with_two_criteria(db_file: str, db: str, field1: str, criteria1: str, field2: str,
                                criteria2: str) -> str or None:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    try:
        c.execute(f"SELECT * FROM {db} WHERE {field1}='{criteria1}' AND {field2}='{criteria2}'")
        results = c.fetchone()
        item = results[0]
        c.close()
        conn.close()
        return item
    except:
        c.close()
        conn.close()
        return None


# return an entire row

def search_row(db_file: str, db: str, field: str, criteria: str) -> str or None:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    try:
        table = list(c.execute(f"SELECT * FROM {db}").description)
        # print('table')
        # print(table)

        c.execute(f"SELECT * FROM {db}")
        results = c.fetchall()
        # print('results')
        # print(results)

        for col in table:
            if col[0] == field:
                i = table.index(col)
                for row in results:
                    if row[i] == criteria:
                        c.close()
                        conn.close()
                        return row
                    else:
                        continue
            else:
                continue
        return None
    except:
        c.close()
        conn.close()
        return None


def fetch_column_names(db_file: str, db: str) -> list or str:
    """ Return the name of the columns """

    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        fetch_column_names = f'PRAGMA table_info({db})'
        c.execute(fetch_column_names)
        column_names_info = c.fetchall()
        c.close()
        conn.close()

        # column_names = []
        # for info in column_names_info:
        #     column_names.append(info[1])

        column_names = [info[1] for info in column_names_info]

        return column_names
    except Exception as err:
        print(err)
        return str(err)


def search_cell(db_file: str, db: str, field: str, criteria: str, column: str) -> str or None:
    """searche for a cell based on the row (field and criteria) and teh intended column"""
    try:
        column_names = fetch_column_names(db_file, db)
        column_index = column_names.index(column)

        result = search_row(db_file, db, field, criteria)[column_index]
    except:
        result = None
    return result


def search_simple_table_cell(db_file: str, db: str, column: str) -> str:
    return search_cell(db_file, db, field='id', criteria='a', column=column)


def return_pair_field_value(db_file: str, db: str, field: str, criteria: str) -> list or str:
    """ Search a row and return a list containing tuples: (field name, value) """

    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        fetch_column_names = f'PRAGMA table_info({db})'
        c.execute(fetch_column_names)
        column_names_info = c.fetchall()
        c.close()
        conn.close()

        # column_names = []
        # for info in column_names_info:
        #     column_names.append(info[1])

        column_names = [info[1] for info in column_names_info]
        values = search_row(db_file, db, field, criteria)
        merged_list = [(column_names[i], values[i]) for i in range(0, len(column_names))]
        return merged_list
    except Exception as err:
        print(err)
        return str(err)


def return_dict_of_a_row(db_file: str, db: str, field: str, criteria: str) -> dict or str:
    """ Search a row and return a dictionary with field names as keys and their values as values """

    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        fetch_column_names = f'PRAGMA table_info({db})'
        c.execute(fetch_column_names)
        column_names_info = c.fetchall()
        c.close()
        conn.close()

        column_names = [info[1] for info in column_names_info]
        values = search_row(db_file, db, field, criteria)

        # Using dictionary comprehension to merge column_names and values into a dictionary
        merged_dict = {column_names[i]: values[i] for i in range(0, len(column_names))}

        return merged_dict
    except Exception as err:
        print(err)
        return str(err)


# Return an entire row with two criteria

def search_row_with_two_criteria(db_file: str, db: str, field1: str, criteria1: str, field2: str,
                                 criteria2: str) -> str or None:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    try:
        table = list(c.execute(f"SELECT * FROM {db}").description)

        c.execute(f"SELECT * FROM {db}")
        results = c.fetchall()
        table_criteria_1 = []
        for col in table:
            if col[0] == field1:
                i = table.index(col)
                for row in results:
                    if row[i] == criteria1:
                        table_criteria_1.append(row)
                    else:
                        continue
            else:
                continue

        for col in table:
            if col[0] == field2:
                i = table.index(col)
                for item in table_criteria_1:
                    if item[i] == criteria2:
                        return item
                    else:
                        continue
            else:
                continue
        return None
    except:
        c.close()
        conn.close()
        return None


import sqlite3


def get_table_names(db_file):
    # Lista para armazenar os nomes das tabelas
    table_names = []

    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect(db_file)

        # Criar um cursor para executar consultas SQL
        cursor = conn.cursor()

        # Consulta para obter todos os nomes de tabelas no banco de dados SQLite
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        # Recuperar todos os resultados da consulta
        tables = cursor.fetchall()

        # Adicionar os nomes das tabelas à lista table_names
        for table in tables:
            table_names.append(table[0])

        # Fechar a conexão com o banco de dados
        conn.close()

    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados {db_file}: {e}")

    return table_names


# FETCH ENTIRE TABLE

def fetch_entire_table(db_file: str, db: str) -> str or None:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    try:
        c.execute(f'SELECT * FROM {db}')
        output = c.fetchall()
        c.close()
        conn.close()
        return output
    except:
        c.close()
        conn.close()
        return None


# FETCH ENTIRE TABLE ORDER BY column

def fetch_ordered_table(db_file: str, db: str, field: str) -> str or None:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    try:
        c.execute(f'SELECT * FROM {db} ORDER BY {field} ASC')
        output = c.fetchall()
        c.close()
        conn.close()
        return output
    except:
        c.close()
        conn.close()
        return None


def fetch_all_col(db_file: str, db: str, field: str) -> str or None:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    try:
        c.execute(f'SELECT {field} FROM {db}')
        itens = c.fetchall()
        c.close()
        conn.close()
        return itens
    except:
        c.close()
        conn.close()
        return None


def calculate_table_size(db_file: str, db: str) -> int or None:
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute(f"SELECT COUNT(*) FROM {db}")

        result = c.fetchone()
        conn.close()
        return result[0]

    except sqlite3.Error as e:
        print(f"Ocorreu um erro: {e}")
        return None



def return_column_index(db_file: str, db: str, column):
    all_entries_column = fetch_column_names(db_file, db)
    index = all_entries_column.index(column)
    return index



def add_new_col(db_file: str, db: str, field: str) -> None:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    try:
        c.execute(f'ALTER TABLE {db} ADD {field} TEXT')
    except:
        c.execute(f'CREATE TABLE IF NOT EXISTS {db} ({field} TEXT)')
    c.close()
    conn.close()


def add_new_populated_col(db_file: str, db: str, field: str, fill: str) -> None:
    """ Create a new column and populate all the cells with the same string entry """
    add_new_col(db_file, db, field)
    column_names = fetch_column_names(db_file, db)
    first_column = column_names[0]
    touple_elements_of_first_column = fetch_all_col(db_file, db, first_column)
    elements_of_first_column = [item[0] for item in touple_elements_of_first_column]
    for element in elements_of_first_column:
        update_cell(
            db_file,
            db,
            first_column,
            criteria=element,
            column_name=field,
            new_value=fill)


# Delete entry with one criteria

def delete_entry(db_file: str, db: str, field: str, criteria: str or int) -> None:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    try:
        # c.execute(f"SELECT * FROM destination WHERE id='{chat_id}'")
        # results = cur.fetchone()
        c.execute(f"DELETE from {db} where {field}= ?", (criteria,))
    except:
        pass
    conn.commit()
    c.close()
    conn.close()


import sqlite3


def delete_all_entries_matching_criteria(db_file: str, db: str, field: str, criteria: str or int) -> None:
    """
    Deletes all rows from a table in an SQLite database that match a criterion in a specific column.

    Args:
    - db_file (str): Path to the SQLite database file.
    - db (str): Name of the table.
    - field (str): Name of the column where the criterion will be applied.
    - criteria (str or int): Criterion for selecting the rows to be deleted.

    Returns:
    - None
    """

    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    try:
        c.execute(f"DELETE FROM {db} WHERE {field} = ?", (criteria,))
    except Exception as e:
        print(f"Erro ao deletar entradas: {e}")

    conn.commit()
    c.close()
    conn.close()


# Delete one entry with two criteria

def delete_entry_with_two_criteria(db_file: str, db: str, field1: str, criteria1: str, field2: str,
                                   criteria2: str) -> None:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    try:
        # c.execute(f"SELECT * FROM destination WHERE id='{chat_id}'")
        # results = cur.fetchone()
        c.execute(f"DELETE from {db} where {field1}= ? AND {field2}= ?", (criteria1, criteria2))
    except:
        pass
    conn.commit()
    c.close()
    conn.close()


def delete_all_rows(db_file: str, db: str) -> None:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    try:
        c.execute(f"DELETE from {db}")
    except:
        pass
    conn.commit()
    c.close()
    conn.close()


def delete_column(db_file: str, db: str, field: str) -> None:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    try:
        c.execute(f"ALTER TABLE {db} DROP COLUMN {field}")
    except:
        pass
    conn.commit()
    c.close()
    conn.close()


# DELETE ENTIRE TABLE
def delete_table(db_file: str, db: str) -> None:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    try:
        c.execute(f"DROP TABLE IF EXISTS {db}")
    except:
        pass
    conn.commit()
    c.close()
    conn.close()


def create_db(db_file: str, db: str, dic: dict) -> None:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # define columns
    columns_length = len(list(dic.items()))

    # Creating string for sql command for creating bd
    part_1_create_table_sql = f"CREATE TABLE IF NOT EXISTS {db} ("
    for r in range(0, columns_length):
        part_1_create_table_sql = part_1_create_table_sql + str(list(dic.keys())[r]) + " TEXT"
        if r < (columns_length - 1):
            part_1_create_table_sql = part_1_create_table_sql + ", "

    create_table_sql = part_1_create_table_sql + ");"

    # criar BD
    c.execute(create_table_sql)

    # Inserir linha

    sqlite_insert_row = f"INSERT INTO {db} VALUES ("
    for r in range(0, columns_length):
        sqlite_insert_row = sqlite_insert_row + "?"
        if r < (columns_length - 1):
            sqlite_insert_row = sqlite_insert_row + ", "
    sqlite_insert_row = sqlite_insert_row + ")"

    params = tuple(dic.values())
    c.execute(sqlite_insert_row, params)
    conn.commit()
    c.close()
    conn.close()


def create_empty_table(db_file: str, db: str, fields_list: list) -> str:
    """
        Creates an empty table in a given database with specified fields.

        This function creates an empty table by creating a database with an initial
        dummy entry, then deleting that entry. If any exception occurs, it will return 'error'.

        Args:
            db_file (str): The name or path of the database file.
            db (str): The name of the database where the table will be created.
            fields_list (list): A list of strings representing the fields to be created in the table.

        Returns:
            str: Returns 'success' if the operation completes successfully.
            str: Returns 'error' if any error or exception occurs during the operation.
        """
    try:
        dic = {}
        for field in fields_list:
            dic[field] = "x"
        create_db(db_file, db, dic)
        delete_entry(db_file, db, fields_list[0], "x")
        return "success"
    except:
        return "error"


def create_db_with_id(db_file: str, db: str, id_name: str, dic: dict) -> None:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # define columns
    columns_length = len(list(dic.items()))

    # Creating string for sql command for creating bd
    part_1_create_table_sql = f"CREATE TABLE IF NOT EXISTS {db} ({id_name} INTEGER PRIMARY KEY AUTOINCREMENT,"
    for r in range(0, columns_length):
        part_1_create_table_sql = part_1_create_table_sql + str(list(dic.keys())[r]) + " TEXT"
        if r < (columns_length - 1):
            part_1_create_table_sql = part_1_create_table_sql + ", "

    create_table_sql = part_1_create_table_sql + ");"

    # criar BD
    c.execute(create_table_sql)

    # Inserir linha
    keys = str(tuple(dic.keys())).replace("'", "")
    sqlite_insert_row = f"INSERT INTO {db}{keys} VALUES ("
    for r in range(0, columns_length):
        sqlite_insert_row = sqlite_insert_row + "?"
        if r < (columns_length - 1):
            sqlite_insert_row = sqlite_insert_row + ", "
    sqlite_insert_row = sqlite_insert_row + ")"

    params = tuple(dic.values())
    c.execute(sqlite_insert_row, params)
    conn.commit()
    c.close()
    conn.close()


def update_db(db_file: str, db: str, field: str, criteria: str, dic: dict) -> None:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    try:
        # c.execute(f"SELECT * FROM destination WHERE id='{chat_id}'")
        # results = cur.fetchone()
        c.execute(f"DELETE from {db} where {field}= ?", (criteria,))
        conn.commit()
    except:
        pass

    # define columns
    columns_length = len(list(dic.items()))

    # Creating string for sql command for creating bd
    part_1_create_table_sql = f"CREATE TABLE IF NOT EXISTS {db} ("
    for r in range(0, columns_length):
        part_1_create_table_sql = part_1_create_table_sql + str(list(dic.keys())[r]) + " TEXT"
        if r < (columns_length - 1):
            part_1_create_table_sql = part_1_create_table_sql + ", "

    create_table_sql = part_1_create_table_sql + ");"

    # criar BD
    c.execute(create_table_sql)

    # Inserir linha
    sqlite_insert_row = f"INSERT INTO {db} VALUES ("
    for r in range(0, columns_length):
        sqlite_insert_row = sqlite_insert_row + "?"
        if r < (columns_length - 1):
            sqlite_insert_row = sqlite_insert_row + ", "
    sqlite_insert_row = sqlite_insert_row + ")"

    params = tuple(dic.values())
    c.execute(sqlite_insert_row, params)
    conn.commit()
    c.close()
    conn.close()


# The 'dic' variable is a dictionary with title of the column and the variable to be stored


def add_entry(db_file: str, db: str, dic: dict) -> None:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    # define columns
    columns_length = len(list(dic.items()))

    # Creating string for sql command for creating bd
    part_1_create_table_sql = f"CREATE TABLE IF NOT EXISTS {db} ("
    for r in range(0, columns_length):
        part_1_create_table_sql = part_1_create_table_sql + str(list(dic.keys())[r]) + " TEXT"
        if r < (columns_length - 1):
            part_1_create_table_sql = part_1_create_table_sql + ", "

    create_table_sql = part_1_create_table_sql + ");"
    print('###################### create_table_sql ###############################', create_table_sql)
    # criar BD
    c.execute(create_table_sql)

    # Inserir linha
    sqlite_insert_row = f"INSERT INTO {db} VALUES ("
    for r in range(0, columns_length):
        sqlite_insert_row = sqlite_insert_row + "?"
        if r < (columns_length - 1):
            sqlite_insert_row = sqlite_insert_row + ", "
    sqlite_insert_row = sqlite_insert_row + ")"
    params = tuple(dic.values())
    c.execute(sqlite_insert_row, params)
    conn.commit()
    c.close()
    conn.close()


import sqlite3


def insert_into_single_column_table(db_file: str, db: str, field: str, new_value: str) -> str:
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        # Create the table and the column if they do not exist
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {db} ({field} TEXT UNIQUE)")
        # Insert a new value into the table
        cursor.execute(f"INSERT INTO {db} ({field}) VALUES (?)", (new_value,))
        # Commit the transaction
        conn.commit()
        # Close the connection
        conn.close()
        return 'success'
    except sqlite3.IntegrityError:
        # In case the value already exists in the table
        return 'error'
    except Exception as e:
        print(e)
        return 'error'


def insert_into_table(db_file: str, db: str, dic: dict) -> str:
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {db} (id INTEGER PRIMARY KEY)")

        # Fetch all column names in the table
        cursor.execute(f"PRAGMA table_info({db})")
        columns_info = cursor.fetchall()
        existing_columns = [column[1] for column in columns_info]

        # Add the columns from the dictionary if they do not exist
        for column in dic.keys():
            if column not in existing_columns:
                cursor.execute(f"ALTER TABLE {db} ADD {column} TEXT")

        # Prepare the insert statement
        columns = ', '.join(dic.keys())
        placeholders = ', '.join('?' * len(dic))
        sql = f"INSERT INTO {db} ({columns}) VALUES ({placeholders})"

        # Insert a new row with the values from the dictionary
        cursor.execute(sql, tuple(dic.values()))
        conn.commit()
        conn.close()

        return 'success'
    except Exception as e:
        print(e)
        return 'error'


def insert_object_into_table(db_file: str, db: str, obj: object) -> str:
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {db} (id INTEGER PRIMARY KEY)")

        # Fetch all column names in the table
        cursor.execute(f"PRAGMA table_info({db})")
        columns_info = cursor.fetchall()
        existing_columns = [column[1] for column in columns_info]

        # Convert object to a dictionary of attributes
        dic = vars(obj)

        # Add the columns from the object if they do not exist
        for column in dic.keys():
            if column not in existing_columns:
                cursor.execute(f"ALTER TABLE {db} ADD {column} TEXT")

        # Prepare the insert statement
        columns = ', '.join(dic.keys())
        placeholders = ', '.join('?' * len(dic))
        sql = f"INSERT INTO {db} ({columns}) VALUES ({placeholders})"

        # Insert a new row with the values from the object
        cursor.execute(sql, tuple(dic.values()))
        conn.commit()
        conn.close()

        return 'success'
    except Exception as e:
        print(e)
        return 'error'


# Change an entire row
def change_row(db_file: str, db: str, field: str, criteria: str, dic: dict) -> None:
    try:
        delete_entry(db_file, db, field, criteria)
    except:
        pass
    add_entry(db_file, db, dic)


# Change an entire row based on two criteria
def change_row_with_two_criteria(db_file: str, db: str, field1: str, criteria1: str, field2: str, criteria2: str,
                                 dic: dict) -> None:
    try:
        delete_entry_with_two_criteria(db_file, db, field1, criteria1, field2, criteria2)
    except:
        pass
    add_entry(db_file, db, dic)


# CHANGE ROW BASED ON ID

def change_row_with_id(db_file: str, db: str, id_field: str, id_num: int, dic: dict) -> None:
    try:
        delete_entry(db_file, db, id_field, id_num)
    except:
        pass
    create_db_with_id(db_file, db, id_field, dic)


# UPDATE VALUE OF A CELL

def update_cell(db_file: str, db: str, field: str, criteria: str, column_name: str, new_value: str) -> bool:
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        sql_query = f"Update {db} set {column_name} = '{new_value}' where {field} = '{criteria}'"
        print(sql_query)
        c.execute(sql_query)
        conn.commit()
        c.close()
        return True
    except sqlite3.Error as err:
        print("Error in sqlite: ", err)
        return False
    finally:
        if conn:
            conn.close()


def update_or_create_empty_row(db_file: str, db: str, field: str, criteria: str, column_name: str,
                               new_value: str) -> str:
    """
        Search for a field entry, if it exists, then it updates one cell
        If it does not exist, then it creates a row and updates the desired cell
    """
    if criteria == new_value:
        response = check_or_create_empty_row(db_file, db, field, criteria)
    else:
        response = update_cell(db_file, db, field, criteria, column_name, new_value)
    if not response:
        try:
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            fetch_column_names = f'PRAGMA table_info({db})'
            c.execute(fetch_column_names)
            column_names_info = c.fetchall()

            column_names = []
            for info in column_names_info:
                column_names.append(info[1])

            new_dic = {}
            for retrieved_column_name in column_names:
                if retrieved_column_name == field:
                    new_dic[field] = criteria
                if retrieved_column_name == column_name:
                    new_dic[column_name] = new_value
                else:
                    new_dic[column_name] = ""
            conn.commit()
            c.close()
            conn.close()

            if new_dic == {}:
                new_dic = {column_name: new_value}

            change_row(db_file, db, field=field, criteria=criteria, dic=new_dic)
            return 'success'
        except Exception as err:
            print('err na função db_tricks')
            print(err)
            return str(err)
    else:
        return 'success'


def create_filled_row(db_file: str, db: str, field: str, criteria: str, cells_value: str):
    # create a database connection
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # check if the criteria is already in the database
    c.execute(f'SELECT * FROM {db} WHERE {field} = ?', (criteria,))
    result = c.fetchone()

    # if the criteria is not in the database, insert a new row
    if result is None:
        # get the number of columns in the table
        c.execute(f'PRAGMA table_info({db})')
        num_columns = len(c.fetchall())

        # create a string of '?' placeholders for the SQL query
        placeholders = ', '.join(['?'] * num_columns)

        # create a list of values for the new row
        # the criteria will be the first value, and all other values will be the empty_value
        values = [criteria] + [cells_value] * (num_columns - 1)

        # insert the new row
        c.execute(f'INSERT INTO {db} VALUES ({placeholders})', values)

        # commit the changes and close the connection
        conn.commit()
    conn.close()


def check_or_create_empty_row(db_file: str, db: str, field: str, criteria: str) -> str:
    """
        Search for a field entry, if it exists
        If it does not exist, then creates a row and updates the desired cell
    """
    response = search_row(db_file, db, field, criteria)
    if response is None:
        try:
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            fetch_column_names = f'PRAGMA table_info({db})'
            c.execute(fetch_column_names)
            column_names_info = c.fetchall()
            column_names = [info[1] for info in column_names_info]
            new_dic = {}
            for retrieved_column_name in column_names:
                if retrieved_column_name == field:
                    new_dic[field] = criteria
                else:
                    new_dic[retrieved_column_name] = ""
            conn.commit()
            c.close()
            conn.close()

            change_row(db_file, db, field=field, criteria=criteria, dic=new_dic)
            return 'success'
        except Exception as err:
            print(err)
            return str(err)


def update_first_cell(db_file, db):
    import sqlite3
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(f"UPDATE {db} SET identifier = 1 WHERE rowid = 1")
    conn.commit()
    conn.close()


# Create columns or update it in columns with one row and imutable first column
def update_or_create_column_checking_identifier(db_file: str,
                                                db: str,
                                                field: str,
                                                criteria: str,
                                                new_field: str,
                                                new_value: str) -> None:
    """ Create columns or update it in columns with one row and imutable first column """
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    fetch_column_names = f'PRAGMA table_info({db})'
    c.execute(fetch_column_names)
    column_names_info = c.fetchall()

    column_names = []
    for info in column_names_info:
        column_names.append(info[1])

    if len(column_names) == 0:
        sql_create_table = f""" CREATE TABLE IF NOT EXISTS {db} (
                                                {field} text,
                                                {new_field} text
                                            ); """
        c.execute(sql_create_table)

        sqlite_insert_row = f"INSERT INTO {db} ({field, new_field}) VALUES (?, ?)"
        params = (criteria, new_value)
        c.execute(sqlite_insert_row, params)
        update_first_cell(db_file, db)
    else:
        if new_field in column_names:
            update_first_cell(db_file, db)
            update_sql_cell = f"UPDATE {db} set {new_field} = '{new_value}' where {field} = '{criteria}'"
            c.execute(update_sql_cell)
        else:
            update_first_cell(db_file, db)
            c.execute(f'ALTER TABLE {db} ADD {new_field} TEXT')
            update_sql_cell = f"UPDATE {db} set {new_field} = '{new_value}' where {new_field} IS NULL"
            c.execute(update_sql_cell)
    conn.commit()
    c.close()
    conn.close()


def update_or_create_column(db_file: str,
                            db: str,
                            field: str,
                            criteria: str,
                            new_field: str,
                            new_value: str) -> None:
    """ Create columns or update it in columns with one row and imutable first column """
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    fetch_column_names = f'PRAGMA table_info({db})'
    c.execute(fetch_column_names)
    column_names_info = c.fetchall()

    column_names = []
    for info in column_names_info:
        column_names.append(info[1])

    if len(column_names) == 0:
        sql_create_table = f""" CREATE TABLE IF NOT EXISTS {db} (
                                                {field} text,
                                                {new_field} text
                                            ); """
        c.execute(sql_create_table)

        sqlite_insert_row = f"INSERT INTO {db} ({field, new_field}) VALUES (?, ?)"
        params = (criteria, new_value)
        c.execute(sqlite_insert_row, params)

    else:
        if new_field in column_names:

            update_sql_cell = f"UPDATE {db} set {new_field} = '{new_value}' where {field} = '{criteria}'"
            c.execute(update_sql_cell)
        else:
            c.execute(f'ALTER TABLE {db} ADD {new_field} TEXT')
            update_sql_cell = f"UPDATE {db} set {new_field} = '{new_value}' where {new_field} IS NULL"
            c.execute(update_sql_cell)
    conn.commit()
    c.close()
    conn.close()


def update_or_create_column_for_complex_table(db_file: str, db: str, field: str, criteria: str, column_name: str,
                                              new_value: str) -> str:
    """
        Search for a field entry. If it exists, then it updates one cell
        If it does not exists, then it creates a row and updates the desired cell
        If cell does not exist, create a column and update this cell
    """
    column_names = fetch_column_names(db_file, db)
    if column_name not in column_names:
        add_new_col(db_file, db, column_name)
    check_or_create_empty_row(db_file, db, field, criteria)
    update_cell(db_file, db, field, criteria, column_name, new_value)


# Uptdate a single cell in a single row table (create a table if not exist and create columns if not exist)
def update_cell_in_simple_table(db_file: str, db: str, field: str, criteria: str, new_value: str) -> None:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    fetch_column_names = f'PRAGMA table_info({db})'
    c.execute(fetch_column_names)
    column_names_info = c.fetchall()

    column_names = []
    for info in column_names_info:
        column_names.append(info[1])

    if len(column_names) == 0:
        sql_create_table = f""" CREATE TABLE IF NOT EXISTS {db} (
                                                {field} text
                                            ); """
        c.execute(sql_create_table)

        sqlite_insert_row = f"INSERT INTO {db} ({field}) VALUES (?)"
        params = (new_value,)
        c.execute(sqlite_insert_row, params)
    else:
        if field in column_names:
            update_sql_cell = f"UPDATE {db} set {field} = '{new_value}' where {field} = '{criteria}'"
            c.execute(update_sql_cell)
        else:
            c.execute(f'ALTER TABLE {db} ADD {field} TEXT')
            update_sql_cell = f"UPDATE {db} set {field} = '{new_value}' where {field} IS NULL"
            c.execute(update_sql_cell)
    conn.commit()
    c.close()
    conn.close()


def create_or_update_column_in_on_line_table(db_file: str, db: str, column_name: str, new_value: str) -> str:
    """
        Search for a columns.
        If it not exists, create and update.
        If it exists, update it.
    """
    column_names = fetch_column_names(db_file, db)
    if 'id' not in column_names:
        dic = {
            'id': 'a'
        }
        add_entry(db_file, db, dic)
    if column_name not in column_names:
        add_new_col(db_file, db, column_name)
    update_cell(db_file, db, 'id', 'a', column_name, new_value)


# VISUALIZE DATA BASE AS PREATTY TABLE

def visualize_db(db_file: str, db: str) -> str:
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {db}")
    mytable = from_db_cursor(cursor)
    mystring = mytable.get_string()
    print(mystring)
    return mystring

