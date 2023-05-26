import connection

# create rooms table
def create_rooms_table():
    conn = connection.get_connection()
    try:
        cursor = conn.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS Rooms (id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, 
        name VARCHAR(20), width FLOAT, length FLOAT, height FLOAT, square FLOAT, device_ip VARCHAR(17), device VARCHAR(20)) 
        """
        cursor.execute(query)
        conn.commit()
    finally:
        conn.close()

# insert new room to rooms table
def insert_to_rooms_table(name, width, length, height, square, device_ip, device):
    conn = connection.get_connection()

    cursor = conn.cursor()
    query = """
           INSERT INTO Rooms (name, width, length, height, square, device_ip, device) VALUES (%s, %s, %s, %s, %s, %s, %s) 
           """
    val = (name, width, length, height, square, device_ip, device)
    cursor.execute(query, val)
    conn.commit()
    return cursor.lastrowid

# select id of the room with specific IP-ADDRESS
def select_devices_from_room_table():
    conn = connection.get_connection()

    cursor = conn.cursor()
    query = """
            SELECT id, device_ip FROM Rooms
            """
    cursor.execute(query)
    results = cursor.fetchall()

    return results

# select id, device_name, device_ip from Rooms table
# select id of the room with specific IP-ADDRESS
def select_all_devices_from_room_table():
    conn = connection.get_connection()

    cursor = conn.cursor()
    query = """
            SELECT id, name, device_ip, device FROM Rooms
            """
    cursor.execute(query)
    results = cursor.fetchall()

    return results

def delete_from_rooms_table(id):
    conn = connection.get_connection()
    try:
        cursor = conn.cursor()
        query = """
               DELETE FROM Rooms WHERE id = %s
               """
        cursor.execute(query, id)
        conn.commit()
    finally:
        conn.close()


# update sensor info in sensors table
def update_in_rooms_table(id, name, width, length, height, square, device_ip, device):
    conn = connection.get_connection()
    try:
        cursor = conn.cursor()
        query = """
               UPDATE Rooms SET name=%s, width=%s, length=%s, height=%s, square=%s, device_ip=%s, device=%s WHERE id=%s 
               """
        val = (name, width, length, height, square, device_ip, device, id)
        cursor.execute(query, val)
        conn.commit()
    finally:
        conn.close()

def select_all_id_from_rooms_table():
    conn = connection.get_connection()

    cursor = conn.cursor()
    query = """
                SELECT id FROM Rooms 
                """
    cursor.execute(query)
    results = cursor.fetchall()
    return results