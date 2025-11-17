from connect_with_db import get_cursor
from flask import jsonify

def start():
    print("Het is gelukt!")

    myconn, mycursor = get_cursor()
    mycursor.execute("""SELECT Eigenaar_of_huurder, Perioden, `Tevredenheid met de huidige woning (%)`, `Tevredenheid met de huidige woonomgeving (%)`
FROM urbanmythdb.woontevredenheid""")
    data = mycursor.fetchall()

    return jsonify(data)