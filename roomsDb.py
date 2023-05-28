import connection

# create Rooms table
def create_rooms_table():
    conn = connection.get_connection()
    try:
        cursor = conn.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS Rooms (id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, 
        name VARCHAR(20), width FLOAT, length FLOAT, height FLOAT, 
        square FLOAT, device_ip VARCHAR(17), device VARCHAR(20)) 
        """
        cursor.execute(query)
        conn.commit()
    finally:
        conn.close()

# insert new room to Rooms table
def insert_to_rooms_table(name, width, length, height, square, device_ip, device):
    conn = connection.get_connection()
    cursor = conn.cursor()
    query = """
           INSERT INTO Rooms (name, width, length, height, square, device_ip, device) 
           VALUES (%s, %s, %s, %s, %s, %s, %s) 
           """
    val = (name, width, length, height, square, device_ip, device)
    cursor.execute(query, val)
    conn.commit()
    return cursor.lastrowid

# delete room from Rooms table
def delete_from_rooms_table(id_param):
    conn = connection.get_connection()
    cursor = conn.cursor()
    query = """
            DELETE FROM Rooms WHERE id = %s
            """
    cursor.execute(query, id_param)
    conn.commit()

# update room info in Rooms table
def update_in_rooms_table(id_param, name, width, length, height, square, device_ip, device):
    conn = connection.get_connection()
    cursor = conn.cursor()
    query = """
            UPDATE Rooms SET name=%s, width=%s, length=%s, height=%s, square=%s, device_ip=%s, device=%s 
            WHERE id=%s 
            """
    val = (name, width, length, height, square, device_ip, device, id_param)
    cursor.execute(query, val)
    conn.commit()

# select id and ip from Rooms table
def select_id_and_ip_from_rooms_table():
    conn = connection.get_connection()
    cursor = conn.cursor()
    query = """
            SELECT id, device_ip FROM Rooms
            """
    cursor.execute(query)
    results = cursor.fetchall()
    return results

# select all data from Rooms table
def select_all_data_from_rooms_table():
    conn = connection.get_connection()
    cursor = conn.cursor()
    query = """
            SELECT * FROM Rooms
            """
    cursor.execute(query)
    results = cursor.fetchall()
    return results

# select id, device_name, device_ip and device from Rooms table
def select_all_devices_from_rooms_table():
    conn = connection.get_connection()
    cursor = conn.cursor()
    query = """
            SELECT id, name, device_ip, device FROM Rooms
            """
    cursor.execute(query)
    results = cursor.fetchall()
    return results

# select all id from Rooms table
def select_all_id_from_rooms_table():
    conn = connection.get_connection()
    cursor = conn.cursor()
    query = """
            SELECT id FROM Rooms 
            """
    cursor.execute(query)
    results = cursor.fetchall()
    return results