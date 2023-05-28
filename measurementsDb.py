import connection

# create Measurements table
def create_measurements_table():
    conn = connection.get_connection()
    try:
        cursor = conn.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS Measurements 
        (id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, 
        sensor_id INTEGER, value FLOAT, date_time VARCHAR(20),
        FOREIGN KEY (sensor_id) REFERENCES Sensors (id) ON DELETE CASCADE) 
        """
        cursor.execute(query)
        conn.commit()
    finally:
        conn.close()

# insert measurement of sensor to Measurements table
def insert_to_measurements_table(sensor_id, value, date_time):
    conn = connection.get_connection()
    cursor = conn.cursor()
    query = """
            INSERT INTO Measurements (sensor_id, value, date_time) 
            VALUES(%s, %s, %s) 
            """
    val = (sensor_id, value, date_time)
    cursor.execute(query, val)
    conn.commit()

# select measurements` data of specific sensor
def select_specific_measurements_from_measurements_table(sensor_id):
    conn = connection.get_connection()
    cursor = conn.cursor()
    query = """
            SELECT id, sensor_id, value, date_time FROM Measurements 
            WHERE sensor_id = %s
            """
    val = sensor_id
    cursor.execute(query, val)
    results = cursor.fetchall()
    return results

# select all measurements of sensor from datetime_1 to datetime_2
def select_measurements_in_interval(sensor_id, datetime_1, datetime_2):
    conn = connection.get_connection()
    cursor = conn.cursor()
    query = """
            SELECT id, sensor_id, value, date_time FROM Measurements 
            WHERE sensor_id = %s AND date_time
            BETWEEN %s AND %s
            """
    val = (sensor_id, datetime_1, datetime_2)
    cursor.execute(query, val)
    results = cursor.fetchall()
    return results

# select actual measurements
def select_actual_measurements(room_id, limit):
    conn = connection.get_connection()
    cursor = conn.cursor()
    query = """
            SELECT id, sensor_id, value, date_time FROM Measurements 
            WHERE sensor_id IN 
            (SELECT id FROM Sensors WHERE room_id = %s) 
            ORDER BY date_time DESC LIMIT %s
            """
    val = (room_id, limit)
    cursor.execute(query, val)
    results = cursor.fetchall()
    return results