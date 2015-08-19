import requests

url = "https://api.github.com/search/repositories?q=Space%20Invaders%20HTML5+language:JavaScript"
response = requests.get(url)
responseJSON = response.json()

print responseJSON