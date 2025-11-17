from connect_with_db import get_cursor
from flask import jsonify

def start():
    print("Het is gelukt!")

    myconn, mycursor = get_cursor()
    mycursor.execute("""SELECT Eigenaar_of_huurder, Perioden, `Tevredenheid met de huidige woning (%)`, `Tevredenheid met de huidige woonomgeving (%)`
FROM urbanmythdb.woontevredenheid""")
    rows = mycursor.fetchall()
    keys = [i[0] for i in mycursor.description]
    data = [dict(zip(keys, row)) for row in rows]

    return jsonify(data)