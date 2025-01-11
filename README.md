Sure, I can help you create a simple SEO tool using Python for the backend with Flask, and HTML/CSS for the frontend. This tool will allow users to enter a URL, and will then analyze some basic SEO information of the site and present it in a table.

First, ensure you have Flask installed. You can install it using pip:

```sh
pip install flask
```

Next, create a file structure like this:

```
seo_tool/
│
├── app.py
├── templates/
│   └── index.html
└── static/
    └── style.css
```

Here is the content for each file:

### app.py

```python
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
```

### templates/index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Analyzer</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h1>SEO Analyzer Tool</h1>
        <form method="post">
            <input type="text" name="url" placeholder="Enter website URL" required>
            <button type="submit">Analyze</button>
        </form>
        {% if seo_data %}
            {% if seo_data.error %}
                <div class="error">{{ seo_data.error }}</div>
            {% else %}
                <table>
                    <tr>
                        <th>Title</th>
                        <td>{{ seo_data.title }}</td>
                    </tr>
                    <tr>
                        <th>Description</th>
                        <td>{{ seo_data.description }}</td>
                    </tr>
                    <tr>
                        <th>Word Count</th>
                        <td>{{ seo_data.word_count }}</td>
                    </tr>
                    <tr>
                        <th>Headings</th>
                        <td>
                            <ul>
                                {% for tag, count in seo_data.headings.items() %}
                                    <li>{{ tag }}: {{ count }}</li>
                                {% endfor %}
                            </ul>
                        </td>
                    </tr>
                </table>
            {% endif %}
        {% endif %}
    </div>
</body>
</html>
```

### static/style.css

```css
body {
    font-family: Arial, sans-serif;
    background-color: #f0f0f0;
    margin: 0;
    padding: 0;
}

.container {
    max-width: 800px;
    margin: 50px auto;
    padding: 20px;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    text-align: center;
}

h1 {
    margin-bottom: 20px;
}

form {
    margin-bottom: 20px;
}

input[type="text"] {
    width: 70%;
    padding: 10px;
    margin-right: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

button {
    padding: 10px 20px;
    border: none;
    background-color: #007BFF;
    color: #fff;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #0056b3;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th, td {
    padding: 10px;
    border: 1px solid #ccc;
    text-align: left;
}

th {
    background-color: #f8f8f8;
}

.error {
    color: red;
    margin-top: 20px;
}
```

### Running the Application

To run the application, navigate to the `seo_tool` directory and execute:

```sh
python app.py
```

This will start the Flask development server. Open your browser and navigate to `http://127.0.0.1:5000/` to see the SEO Analyzer Tool in action.

This basic SEO tool fetches the title, meta description, heading counts, and word count of the entered URL. For a more comprehensive tool, you could integrate additional SEO checks and third-party APIs.
