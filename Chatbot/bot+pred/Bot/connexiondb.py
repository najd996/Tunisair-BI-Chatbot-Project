import oracledb
import os
import dotenv

dotenv.load_dotenv()

def get_db_connection():
    try:
        return oracledb.connect(
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            dsn=os.getenv("DSN")
        )
    except oracledb.Error as e:
        print("Connexion échouée:", e)
        return None