import connection


# create sensors table
def create_sensors_table():
    conn = connection.get_connection()
    try:
        cursor = conn.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS Sensors 
        (id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, 
        room_id INTEGER, name VARCHAR(15), measure VARCHAR(20), measure_unit VARCHAR(5), 
        range_min FLOAT, range_max FLOAT,
        FOREIGN KEY (room_id) REFERENCES Rooms (id)) 
        """
        cursor.execute(query)
        conn.commit()
    finally:
        conn.close()


# insert new sensor to sensors table
def insert_to_sensors_table(room_id, name, measure, measure_unit, range_min, range_max):
    conn = connection.get_connection()

    cursor = conn.cursor()
    query = """
            INSERT INTO Sensors (room_id, name, measure, measure_unit, range_min, range_max) VALUES(%s, %s, %s, %s, %s, %s) 
            """
    val = (room_id, name, measure, measure_unit, range_min, range_max)
    cursor.execute(query, val)
    conn.commit()
    return cursor

# select sensors from specific room
def select_sensors_from_sensors_table(room_id):
    conn = connection.get_connection()

    cursor = conn.cursor()
    query = """
            SELECT id FROM Sensors WHERE room_id = %s
            """
    val = room_id
    cursor.execute(query, val)
    results = cursor.fetchall()
    return results

def select_specific_sensors_from_sensors_table(room_id):
    conn = connection.get_connection()

    cursor = conn.cursor()
    query = """
            SELECT id, room_id, name, measure, measure_unit, range_min, range_max FROM Sensors WHERE room_id = %s
            """
    val = room_id
    cursor.execute(query, val)
    results = cursor.fetchall()
    return results

def select_all_sensors_from_sensors_table():
    conn = connection.get_connection()

    cursor = conn.cursor()
    query = """
                SELECT id, room_id, name, measure, measure_unit FROM Sensors
                """
    cursor.execute(query)
    results = cursor.fetchall()
    return results

# delete sensor from sensors table
def delete_from_sensors_table(id):
    conn = connection.get_connection()
    try:
        cursor = conn.cursor()
        query = """
               DELETE FROM Sensors WHERE id = %s
               """
        cursor.execute(query, id)
        conn.commit()
    finally:
        conn.close()

# update sensor info in sensors table
def update_in_sensors_table(id, name, measure, measure_unit, range_min, range_max):
    conn = connection.get_connection()
    try:
        cursor = conn.cursor()
        query = """
               UPDATE Sensors SET name=%s, measure=%s, measure_unit=%s, range_min=%s, range_max=%s WHERE id=%s 
               """
        val = (name, measure, measure_unit, range_min, range_max, id)
        cursor.execute(query, val)
        conn.commit()
    finally:
        conn.close()

def select_all_id_from_sensors_table():
    conn = connection.get_connection()

    cursor = conn.cursor()
    query = """
                SELECT id FROM Sensors 
                """
    cursor.execute(query)
    results = cursor.fetchall()
    return results