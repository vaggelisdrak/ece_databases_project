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
        INSERT INTO ΠΑΙΚΤΗΣ (Ονοματεπώνυμο, "Αριθμός Φανέλας", Ύψος, id_team, id_player)
        VALUES (?, ?, ?, ?, ?)
    ''', ('Jusuf Nurkic', 20, 2.08, 16, 112))

    # Commit the changes
    conn.commit()

except sqlite3.Error as e:
    print(f"An error occurred: {e}")

finally:
    # Close the connection
    if conn:
        conn.close()