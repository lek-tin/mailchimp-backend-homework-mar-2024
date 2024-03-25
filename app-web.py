from flask import Flask, request
import json
from markdown_to_html import convert_markdown_to_html

app = Flask(__name__)

@app.route('/')
def hello_world():
  return "Hello from Flask Docker container!"

# Controller to convert markdown to html as a POST request
@app.route('/convert-markdown-to-html', methods=['POST'])
def markdown_to_html():
  print("/convert-markdown-to-html, method: POST")
  markdown_text = ""
  try:
    data = request.get_json()
    if data:
      markdown_text = data.get('markdown_text')
      # ignore empty input
      if (not markdown_text or len(markdown_text) == 0):
        return ""
      else:
        html_text = convert_markdown_to_html(markdown_text)
        return html_text
  except (TypeError, json.JSONDecodeError):
    return "Invalid JSON data provided."
  
#  Default handler for /convert-markdown-to-html route
@app.route('/convert-markdown-to-html')
def markdown_to_html_not_allowed():
  return "If you'd like to convert markdown to html, please use POST method"

# Flask app initialization
if __name__ == '__main__':
  app.run(debug=True)