from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/")
def hello():
    return render_template("search.html")

@app.route("/render")
def render():
    return render_template("js.html")

# @app.route("/search/<search_query>")
# def search(search_query):
#     url = "https://api.github.com/search/repositories?q=" + search_query
#     responseJSON = requests.get(url).json()
#     return jsonify(parse_response(responseJSON))

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        if request.form["user_search"] == "":
            return render_template("search.html", msg = "Please enter a search request!")
        else: 
            url = "https://api.github.com/search/repositories?q=" + request.form["user_search"]
            try:
                response_dict = requests.get(url).json()
            except: #connection error
                return render_template("search.html", msg = "Please enter your search request!")
            else:
                # if not response_dict["items"]: #error response
                #     print response_dict
                #     return render_template("search.html", msg = "No results found! Enter another search request: ")
                # # return jsonify(parse_response(response_dict))
                # else: 
                    return render_template("results.html", user_search = request.form["user_search"], gh_data = response_dict)
    else: # request.method == "GET"
        return render_template("search.html")

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