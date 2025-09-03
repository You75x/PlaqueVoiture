from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

html_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Recherche Véhicule</title>
</head>
<body>
    <h2>Identification véhicule par plaque</h2>
    <form method="POST">
        <input type="text" name="plaque" placeholder="Ex: AB123CD">
        <input type="submit" value="Chercher">
    </form>
    {% if result %}
        <h3>Résultat :</h3>
        <pre>{{ result }}</pre>
    {% endif %}
</body>
</html>
"""

def get_car_info_oscaro(plaque):
    url = "https://www.oscaro.com/identification"
    session = requests.Session()
    payload = {"plate": plaque}
    try:
        response = session.post(url, data=payload, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            car_info = soup.find("div", class_="car-infos")
            if car_info:
                return "Oscaro → " + car_info.get_text(strip=True)
            else:
                return None
        return None
    except Exception:
        return None

def get_car_info_api(plaque):
    api_url = f"https://api.api-ninjas.com/v1/vinlookup?vin={plaque}"
    headers = {"X-Api-Key": "TA_CLE_API"}  # <-- remplace par ta clé API gratuite
    try:
        response = requests.get(api_url, headers=headers, timeout=5)
        if response.status_code == 200:
            return "API → " + response.text
        return f"Erreur API ({response.status_code})"
    except Exception as e:
        return f"Erreur API : {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        plaque = request.form.get("plaque")
        if plaque:
            result = get_car_info_oscaro(plaque)
            if not result:
                result = get_car_info_api(plaque)
    return render_template_string(html_page, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
