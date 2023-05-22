import connection


# create measurements table
def create_measurements_table():
    conn = connection.get_connection()
    try:
        cursor = conn.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS Measurements (id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, 
        sensor_id INTEGER, value FLOAT, date_time VARCHAR(20),
        FOREIGN KEY (sensor_id) REFERENCES Sensors (id)) 
        """
        cursor.execute(query)
        conn.commit()
    finally:
        conn.close()


# insert measurement from sensor to measurements table
def insert_to_measurements_table(sensor_id, value, date_time):
    conn = connection.get_connection()
    cursor = conn.cursor()
    query = """
            INSERT INTO Measurements (sensor_id, value, date_time) VALUES(%s, %s, %s) 
            """
    val = (sensor_id, value, date_time)
    cursor.execute(query, val)
    conn.commit()

def select_specific_measurements(sensor_id, datetime_1, datetime_2):
    conn = connection.get_connection()

    cursor = conn.cursor()
    query = """
            SELECT id, sensor_id, value, date_time FROM Measurements WHERE sensor_id = %s AND date_time
            BETWEEN %s AND %s
            """
    val = (sensor_id, datetime_1, datetime_2)
    cursor.execute(query, val)
    results = cursor.fetchall()

    return results