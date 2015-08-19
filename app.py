from flask import Flask, jsonify
import requests

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/search/<search_query>")
def search(search_query):
    url = "https://api.github.com/search/repositories?q=" + search_query
    responseJSON = requests.get(url).json()
    return jsonify(parse_response(responseJSON))

def parse_response(response_dict):
    clean_dict = {
        "total_count": response_dict["total_count"],
        "items":[]
    }
    for repo in response_dict["items"]:
        clean_repo = {
            "name": repo["name"],
            "owner": {
                "login": repo["owner"]["login"],
                "avatar_url": repo["owner"]["avatar_url"],
                "html_url": repo["owner"]["html_url"]
            },
            "html_url": repo["html_url"],
            "description": repo["description"]
        }
        clean_dict["items"].append(clean_repo)
    return clean_dict

@app.errorhandler(404)
def page_not_found(error):
    return "Sorry, this page was not found.", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0")