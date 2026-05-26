from connexiondb import get_db_connection

def exec(req):
    dictionnaire = {}

    conn = get_db_connection()

    if conn is None:
        return {"error": "Database connection failed"}

    cursor = conn.cursor()

    for cle, valeur in req.items():
        sql = valeur.strip()
        cursor.execute(sql)
        result = cursor.fetchall()
        dictionnaire[cle] = result

    cursor.close()
    conn.close()

    return dictionnaire