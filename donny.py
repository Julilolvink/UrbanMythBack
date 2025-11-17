from connect_with_db import get_cursor

def start():
    connection, cursor = get_cursor()
    cursor.execute("""  SELECT 
                        Randstad,
                        AVG(`Gemiddeld persoonlijk inkomen x 1000 euro`) AS avg_pers_inkomen,
                        AVG(`Mediaan persoonlijk inkomen x 1000 euro`)   AS median_pers_inkomen
                        FROM inkomen_van_personen_regio
                        GROUP BY Randstad;""")
    return cursor.fetchall()

def details(randstad_flag: int):
    connection, cursor = get_cursor()
    cursor.execute("""
        SELECT 
            Regios,
            `Gemiddeld persoonlijk inkomen x 1000 euro` AS avg_pers_inkomen,
            `Mediaan persoonlijk inkomen x 1000 euro`   AS median_pers_inkomen
        FROM inkomen_van_personen_regio
        WHERE Randstad = %s;
    """, (randstad_flag,))
    return cursor.fetchall()