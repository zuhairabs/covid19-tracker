from flask import Flask , render_template
import requests
from datetime import datetime

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def dashboard():
	overAll = requests.get("https://corona.lmao.ninja/all").json()
	countries = requests.get("https://corona.lmao.ninja/countries").json()
	countries = list(reversed(sorted(countries,key = lambda i : i['cases'] - i['recovered'] -i['deaths'])))
	

	dataset = requests.get('https://pomber.github.io/covid19/timeseries.json').json()
	countriesList = list(dataset.keys())
	countriesList.sort()
	deaths = {}
	recovered = {}
	infected = {}

	for country in countriesList:
	    countryData = dataset[country]
	    for item in countryData:
	        day = item['date']
	        if day in deaths.keys():
	            deaths[day] = deaths[day] + item['deaths']
	            recovered[day] = recovered[day] + item['recovered']
	            infected[day] = infected[day] + item['confirmed'] - item['deaths'] - item['recovered']
	        else:
	            deaths[day] = item['deaths']
	            recovered[day] = item['recovered']
	            infected[day] = item['confirmed'] - item['deaths'] - item['recovered']

	xd = list(deaths.keys())
	yd = list(deaths.values())
	xi = list(infected.keys())
	yi = list(infected.values())
	xr = list(recovered.keys())
	yr = list(recovered.values())

	return render_template('dashboard.html',overAll = overAll,countries=countries,xd=xd,yd=yd,xi=xi,yi=yi,xr=xr,yr=yr)
	
if __name__ == "__main__":
    app.run(debug=True)