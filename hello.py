from flask import Flask, render_template, url_for, request
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import requests
from datetime import date, time, datetime

# Create Flask instance
app = Flask(__name__)

hist = []

# Create a route decorator
@app.route('/')
def index():
	return render_template("index.html")

@app.route('/converter')
def converter():
	return render_template("converter.html")

@app.route("/calculate", methods=["post"])
def calculate():
	frm = request.form["convFrom"]
	to = request.form["convTo"]
	val = int(request.form["convAmount"])
	rate = get_conversion_rate(frm, to)
	date = datetime.now()
	date = date.strftime("%Y-%m-%d %H:%M")
	if rate != 0:
		res = str(multiply_round(rate, val))
		message = f"1 {frm} = {rate} {to}"
		hist.append((frm, to, val, res, message, date))

	else:
		res = "ERROR"
		message = "An error occurred, please make sure the currencies are valid."
	return render_template("converter.html", result=res, fromVal=frm, toVal=to, amountVal=val, message=message)

@app.route("/history")
def history():
	return render_template("history.html", hist=hist)

@app.route("/historytest")
def historytest():
	return hist


# Scraping and calculating
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0'
}
url1 = "https://www.google.com/search?q="
CONVERSION_CLASS = "DFlfde SwHCTb"

def get_conversion_rate(frm, to):
    url = f'{url1}{frm}+to+{to}'
    request_site = requests.get(url, headers=headers)
    soup = BeautifulSoup(request_site.text, "html.parser")
    span = soup.find(class_=CONVERSION_CLASS)
    if span is not None:
    	span = span['data-value']
    	rate = float(span)
    	return rate
    else:
    	return 0

def multiply_round(rate, value):
    res = rate * value
    res = round(res, 2)
    return res

def get_and_calculate(frm, to, value):
	rate = get_conversion_rate(frm, to)
	return multiply_round(rate, value)

