import sqlite3

try:
    # Connect to the database
    conn = sqlite3.connect('project_db.db')

    # Create a cursor object
    c = conn.cursor()

    # Execute a SQL INSERT INTO query to add a new row to the 'ΟΜΑΔΑ' table
    # c.execute('''
    #     INSERT INTO ΟΜΑΔΑ (Όνομα, Περιοχή, Νίκες, Ήττες, id_group, id_team)
    #     VALUES (?, ?, ?, ?, ?, ?)
    # ''', ('SUNS', 'PHOENIX', 13, 10, 2, 16))
    
    # Execute a SQL INSERT INTO query to add a new row to the 'ΠΑΙΚΤΗΣ' table
    c.execute('''
        INSERT INTO ΑΓΩΝΑΣ (Νικητής, Ηττημένος, Ημερομηνία, "KNOCK OUT GAME", Είδος, id_game)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('WARRIORS', 'CLIPPERS', '12/11/2023', 0, 'REGULAR SEASON',6))

    # Commit the changes
    conn.commit()

except sqlite3.Error as e:
    print(f"An error occurred: {e}")

finally:
    # Close the connection
    if conn:
        conn.close()