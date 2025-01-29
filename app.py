from flask import Flask, render_template, request 
import random
from database import logg_inn, opprett_bruker, bokbestillinger, sebokbestillinger

app = Flask(__name__)


bruker = None
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/logginn')
def logginn():
    return render_template("logginn.html")

@app.route('/bestillinger')
def bestillinger():
    return render_template("bestillinger.html")

@app.route('/sebestillinger')
def sebestillinger():
    try:
        bokbestillingliste = sebokbestillinger()
        lengde = len(bokbestillingliste["boknavn"][0])
        print(lengde)
        return render_template("sebestillinger.html", bokbestillingliste=bokbestillingliste, lengde=lengde)
    except TypeError:
        return "Logg inn for å se bestillinger"

@app.route('/registrer')
def registrer():
    liste = []
    for i in range(100):
        tall = random.randint(0, 100)
        liste.append(tall)
    return render_template("registrer.html", tall_liste=liste)

@app.route('/registrer', methods=['GET', 'POST'])
def hent_registrering():
    if request.method == 'POST':
        navn = request.form['navn']
        etternavn = request.form['etternavn']
        email = request.form['email']
        passord = request.form['passord'] 
        tilbakemelding_registrering = opprett_bruker(navn, etternavn, email, passord)
        
        
        return render_template("registrer.html", tilbakemelding_registrering=tilbakemelding_registrering)
       

@app.route('/logginn', methods=['GET', 'POST'])
def hent_logginn():
    global bruker
    if request.method == 'POST':
        email = request.form['email']
        passord = request.form['passord']
        tilbakemelding_registrering = logg_inn(email, passord)
        bruker = tilbakemelding_registrering
        if bruker == "Feil email eller passord.":
            return render_template("logginn.html", tilbakemelding_registrering=tilbakemelding_registrering)
        else:
            tilbakemelding_registrering = "Innlogging vellyket"
            return render_template("logginn.html", tilbakemelding_registrering=tilbakemelding_registrering)
        
@app.route('/bestillinger', methods=['GET', 'POST'])
def bok_bestillinger():
    if request.method == 'POST':
        Boknavn = request.form['Boknavn']
        Sider = request.form['Sider']
        Ord = request.form['Ord']
        Beskrivelse = request.form['Beskrivelse'] 
        bok_bestilling = bokbestillinger(bruker, Boknavn, Sider, Ord, Beskrivelse) 
        return render_template("bestillinger.html", bok_bestilling=bok_bestilling)
       




if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)
