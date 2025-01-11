from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def analyze_seo(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Title
        title = soup.title.string if soup.title else "No title found"
        
        # Meta Description
        description = ''
        if soup.find("meta", attrs={"name": "description"}):
            description = soup.find("meta", attrs={"name": "description"}).get("content")
        else:
            description = "No description found"
        
        # Headings
        headings = {f"h{i}": len(soup.find_all(f"h{i}")) for i in range(1, 7)}
        
        # Word Count
        words = soup.get_text().split()
        word_count = len(words)
        
        return {
            "title": title,
            "description": description,
            "headings": headings,
            "word_count": word_count
        }
    except Exception as e:
        return {"error": str(e)}

@app.route("/", methods=["GET", "POST"])
def index():
    seo_data = None
    if request.method == "POST":
        url = request.form.get("url")
        seo_data = analyze_seo(url)
    return render_template("index.html", seo_data=seo_data)

if __name__ == "__main__":
    app.run(debug=True)
