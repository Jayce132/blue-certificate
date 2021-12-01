import math

from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():
    r = requests.get(f"https://covid-api.mmediagroup.fr/v1/vaccines")
    data = r.json()

    # wrong api data for these
    # countries = [country for country in list(data.keys()) if
    #              country != "US (Aggregate)"
    #              and country != "Korea, South"
    #              and country != "Timor-Leste"
    #              and country[0:4] != "Cote"
    #              and country != "Congo (Brazzaville)"
    #              and country != "Congo (Kinshasa)"
    #              and country != ""]

    countries = [country for country in list(data.keys()) if data[country]["All"].get('population') if
                 data[country]["All"].get('people_vaccinated')]

    if request.method == 'GET':
        return render_template('index.html', people_vaccinated=0, countries=countries)

    if request.method == 'POST':
        country = request.form['country']
        if country[0:2] != "US":
            country = country.lower().title().replace("And", "and").replace("The", "the")
        r = requests.get(f"https://covid-api.mmediagroup.fr/v1/vaccines?country={country}")
        data = r.json()

        try:
            people_vaccinated = data["All"]["people_vaccinated"]
            pvformat = f"{people_vaccinated:,}"
            population = data["All"]["population"]
            percentage_vaccinated = math.floor(people_vaccinated / population * 100)
        except KeyError:
            return render_template('index.html', people_vaccinated=-1, countries=countries)

        return render_template('index.html', country_selected=country, people_vaccinated=people_vaccinated,
                               percent=percentage_vaccinated, countries=countries, format_vaccinated=pvformat)


app.run(debug=True, port=8080)
