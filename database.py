import mysql.connector
import bcrypt
import hashlib

bruker = []
def connect_to_db():
    mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="Anders",
                password="Anders2018",
                database="bokbestilling"
                )
    # cursor = mydb.cursor()
    return mydb

def create_database():
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE if not exists brukere(
        bruker_id INT AUTO_INCREMENT PRIMARY KEY,
        navn VARCHAR(255) NOT NULL,
        etternavn VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        passord VARCHAR(255) NOT NULL, 
        role text NOT NULL default 'user',
        opprettet_tidspunkt TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        ''')
    cursor.execute('''
            CREATE TABLE if not exists bokbestillinger (
            bok_id INT AUTO_INCREMENT PRIMARY KEY,
            bruker_id INT NOT NULL,
            Boknavn VARCHAR(255) NOT NULL,
            Sider VARCHAR(255) NOT NULL,
            Ord VARCHAR(255) NOT NULL ,
            Beskrivelse VARCHAR(255) NOT NULL, 
            opprettet_tidspunkt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (bruker_id) REFERENCES brukere(bruker_id) ON DELETE CASCADE
        );''')
    db.commit()
    db.close()

create_database()

def hash_passord(passord):
    passord = passord.encode("utf-8" )
    passord_hashed = bcrypt.hashpw(passord, bcrypt.gensalt())
    return passord_hashed



def opprett_bruker(navn, etternavn, email, passord, role="user"):
    db = connect_to_db()
    cursor = db.cursor()

    passord_hash = hash_passord(passord)
    try:
        sql = "INSERT INTO brukere (navn, etternavn, email, passord, role) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (navn, etternavn, email, passord_hash, role))
        db.commit()
        db.close()
        return "Bruker opprettet!"
    except mysql.connector.IntegrityError:
        return "Email er allerede i bruk."
    
opprett_bruker("Anders", "Christenen", "andersmschristensen@icloud.com", "1234", "admin")

def logg_inn(email, passord):
    db = connect_to_db()
    cursor = db.cursor()

    global bruker, id_bruker
    try:
        sql = "SELECT bruker_id, passord, role, navn FROM brukere WHERE email = " + "'" + email + "'"
        cursor.execute(sql)
        bruker = cursor.fetchone()
        db.close()
        id_bruker = bruker
        if bcrypt.checkpw(passord.encode('utf-8'), bruker[1].encode('utf-8')):
            return bruker 
        else:
            return "Feil email eller passord."
    except TypeError:
        return "Feil email eller passord."

def bokbestillinger(bruker_id, Boknavn, Sider, Ord, Beskrivelse):
    db = connect_to_db()
    cursor = db.cursor()
    if bruker_id is not None:
        try:
            sql = "INSERT INTO bokbestillinger  (bruker_id, Boknavn, Sider, Ord, Beskrivelse) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (int(bruker_id), Boknavn, Sider, Ord, Beskrivelse))
            db.commit()
            db.close()
            return "Bokbestilling registrert!"
        except mysql.connector.Error as error:
            return str(error)
    else:
        return "Vennligst logg inn for å bestille bøker."
    

def sebokbestillinger():
    db = connect_to_db()
    cursor = db.cursor()
    try:
        bestilling = {"boknavn": [], "sider": [], "ord": [], "beskrivelse": []}
        sql = "SELECT Boknavn FROM bokbestillinger WHERE bruker_id = " + str(id_bruker[0])
        cursor.execute(sql)
        bestilling["boknavn"].append(cursor.fetchall())

        sql = "SELECT Sider FROM bokbestillinger WHERE bruker_id = " + str(id_bruker[0])
        cursor.execute(sql)
        bestilling["sider"].append(cursor.fetchall())

        sql = "SELECT Ord FROM bokbestillinger WHERE bruker_id = " + str(id_bruker[0]) 
        cursor.execute(sql)
        bestilling["ord"].append(cursor.fetchall())

        sql = "SELECT Beskrivelse FROM bokbestillinger WHERE bruker_id = " + str(id_bruker[0]) 
        cursor.execute(sql)
        bestilling["beskrivelse"].append(cursor.fetchall())
        db.close()
        return bestilling

    except NameError:
        return "Logg inn for å se bestillinger"
    except TypeError:
        return "Logg inn for å se bestillinger"
    except IndexError:
        return "Ingen bokbestilling registrert."