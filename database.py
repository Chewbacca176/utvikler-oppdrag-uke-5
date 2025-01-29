import mysql.connector
import hashlib

bruker = []
mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="Anders",
            password="Anders2018",
            database="bokbestilling"
            )
cursor = mydb.cursor()


cursor.execute('''
    CREATE TABLE if not exists brukere(
    bruker_id INT AUTO_INCREMENT PRIMARY KEY,
    navn VARCHAR(255) NOT NULL,
    etternavn VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    passord VARCHAR(255) NOT NULL, 
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

mydb.commit()

def opprett_bruker(navn, etternavn, email, passord):

    passord_hash = hashlib.md5(passord.encode()).hexdigest()

    try:
        sql = "INSERT INTO brukere (navn, etternavn, email, passord) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (navn, etternavn, email, passord_hash))
        mydb.commit()
        return "Bruker opprettet!"
    except mysql.connector.IntegrityError:
        return "Email er allerede i bruk."
    

def logg_inn(email, passord):
    global bruker, id_bruker
    try:
        sql = "SELECT bruker_id, passord FROM brukere WHERE email = " + "'" + email + "'"
        cursor.execute(sql)
        bruker = cursor.fetchone()
        id_bruker = bruker
        if hashlib.md5(passord.encode()).hexdigest() == bruker[1]:
            return bruker[0] 
        else:
            return "Feil email eller passord."
    except TypeError:
        return "Feil email eller passord."

def bokbestillinger(bruker_id, Boknavn, Sider, Ord, Beskrivelse):
    if bruker_id is not None:
        try:
            sql = "INSERT INTO bokbestillinger  (bruker_id, Boknavn, Sider, Ord, Beskrivelse) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (int(bruker_id), Boknavn, Sider, Ord, Beskrivelse))
            mydb.commit()
            return "Bokbestilling registrert!"
        except mysql.connector.Error as error:
            return str(error)
    else:
        return "Vennligst logg inn for å bestille bøker."
    

def sebokbestillinger():
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

        return bestilling

    except NameError:
        return "Logg inn for å se bestillinger"
    except TypeError:
        return "Logg inn for å se bestillinger"