from flask import Flask, render_template, request
import requests
import re

ADDRESS = "127.0.0.1"
PORT = 8080

app = Flask(__name__)

def get_urls_from_json(data):
    url_pattern = re.compile(r'https?://\S+')

    def is_url(value):
        return isinstance(value, str) and bool(url_pattern.match(value))

    # Recursive function to search for a URL in the JSON data
    def find_urls(json_data):
        urls = []
        if isinstance(json_data, dict): #dictionary case
            for key, value in json_data.items():
                urls.extend(find_urls(value))
        elif isinstance(json_data, list): #list case
            for item in json_data:
                urls.extend(find_urls(item))
        elif is_url(json_data):
            urls.append(json_data)
        return urls

    return find_urls(data)

@app.route("/")
def home():

    return render_template("home.html", data1 = None)

@app.route("/publish1", methods=['POST'])
def publish1():

    list = []
    for i in range(1, 10):
        api_url = 'https://swapi.dev/api/people/?page=' + str(i)


        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            # Assuming the API returns JSON data
            json_data = response.json()
            list.append(json_data['results'])

        except requests.exceptions.RequestException as e:
            # Handle request errors (e.g., connection error, timeout)
            print(f"Error: {e}")
            list = []

    urls = get_urls_from_json(list)
    return render_template("home.html", data1=list, urls1 = urls)


@app.route("/publish2", methods=['POST'])
def publish2():



    text = request.form['fname']
    api_url = 'https://swapi.dev/api/people/' + text
    msg = ""

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Assuming the API returns JSON data
        json_data = response.json()
    except requests.exceptions.RequestException as e:
        # Handle request errors (e.g., connection error, timeout)
        print(f"Error: {e}")
        json_data = []
        msg = "Такой ID не существует. Введите обратно (от 1 до 16, от 18 до 83)"

    urls = get_urls_from_json(json_data)

    return render_template("home.html", data2=json_data, urls2 = urls, msg = msg)

if __name__ == "__main__":
    app.run(debug=True, host=ADDRESS, port=PORT)