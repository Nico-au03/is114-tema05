from flask import Flask
from flask import url_for
from flask import render_template
from flask import request
from flask import redirect
from flask import session
import pandas as pd
from kgmodel import (Foresatt, Barn, Soknad, Barnehage)
from kgcontroller import (form_to_object_soknad, insert_soknad, commit_all, select_alle_barnehager, select_alle_soknad, select_alle_barn, select_alle_foresatt)

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY' # nødvendig for session

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/barnehager')
def barnehager():
    information = select_alle_barnehager()
    return render_template('barnehager.html', data=information)

@app.route('/behandle', methods=['GET', 'POST'])
def behandle():
    if request.method == 'POST':
        sd = request.form
        print(sd)
        log = insert_soknad(form_to_object_soknad(sd))
        print(log)
        session['information'] = sd
        return redirect(url_for('svar')) #[1]
    else:
        information = select_alle_barnehager()
        return render_template('soknad.html', data=information)

@app.route('/svar')
def svar():
    information = session['information']

    barnehager = select_alle_barnehager()

    ledige_barnehage_plasser = []
    ikke_ledige_barnehage_plasser = []

    for barnehage in barnehager:
      if barnehage.barnehage_ledige_plasser > 0:
        ledige_barnehage_plasser.append(barnehage)
      else:
        ikke_ledige_barnehage_plasser.append(barnehage)

    return render_template('svar.html', data=information, ledige_barnehage_plasser=ledige_barnehage_plasser, ikke_ledige_barnehage_plasser=ikke_ledige_barnehage_plasser)

@app.route('/commit')
def commit():
    commit_all()

    kgdata = pd.ExcelFile('kgdata.xlsx', engine='openpyxl')
    barnehager = pd.read_excel(kgdata, 'barnehage', index_col=0).to_dict()
    foresatt = pd.read_excel(kgdata, 'foresatt', index_col=0).to_dict()
    barn = pd.read_excel(kgdata, 'barn', index_col=0).to_dict()
    soknad = pd.read_excel(kgdata, 'soknad', index_col=0).to_dict()

    return render_template('commit.html', barnehager=barnehager, soknad=soknad, barn=barn, foresatt=foresatt)

@app.route('/alle_soknader')
def alle_soknader():
    soknader = select_alle_soknad()
    return render_template('alle_soknader.html', data=soknader) 

if __name__ == "__main__":
    app.run(debug=True)




"""
Referanser
[1] https://stackoverflow.com/questions/21668481/difference-between-render-template-and-redirect
"""

"""
Søkeuttrykk

"""