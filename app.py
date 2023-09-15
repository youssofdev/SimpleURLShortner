from flask import Flask, render_template, request, redirect, url_for, flash
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
app.secret_key = 'YoussofS20)%'  # Replace with a strong secret key

# In-memory URL mapping (replace with a database in a production environment)
url_mappings = {}

# Function to generate a short URL (you can implement your own logic)
def generate_short_url():
    # Implement your logic here
    return 'abc123'

# Function to fetch metadata from a URL
def fetch_url_metadata(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text.strip()
        description = soup.find('meta', attrs={'name': 'description'})['content']
        thumbnail = soup.find('meta', attrs={'property': 'og:image'})['content']
        return {'title': title, 'description': description, 'thumbnail': thumbnail}
    except Exception as e:
        print("Error fetching metadata:", str(e))
        return None

# Routes

@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None  # Initialize short_url as None

    if request.method == 'POST':
        long_url = request.form['long_url']

        short_url = generate_short_url()
        url_mappings[short_url] = {'url': long_url, 'metadata': fetch_url_metadata(long_url)}

        flash("URL shortened successfully!", 'success')

    return render_template('index.html', short_url=short_url)  # Pass short_url to the template

@app.route('/<short_url>')
def redirect_to_original(short_url):
    if short_url in url_mappings:
        original_url = url_mappings[short_url]['url']
        return redirect(original_url)
    else:
        flash("Shortened URL not found.", 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
