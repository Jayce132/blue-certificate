import math

from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():
    r = requests.get(f"https://covid-api.mmediagroup.fr/v1/vaccines")
    data = r.json()
    countries = list(data.keys())
    if request.method == 'GET':
        return render_template('index.html', people_vaccinated=0, countries=countries)

    if request.method == 'POST':
        country = request.form['country']
        if len(country) > 2:
            country = country.lower().title().replace("And", "and")
        else:
            country = country.upper()
        r = requests.get(f"https://covid-api.mmediagroup.fr/v1/vaccines?country={country}")
        data = r.json()
        try:
            people_vaccinated = data["All"]["people_vaccinated"]
            population = data["All"]["population"]
            percentage_vaccinated = math.floor(people_vaccinated / population * 100)
        except KeyError:
            return render_template('index.html', people_vaccinated=-1, countries=countries)
        return render_template('index.html', country_selected=country, people_vaccinated=people_vaccinated, percent=percentage_vaccinated, countries=countries)


# app.run(debug=True, port=8080)
