import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

url = "https://www.billboard.com/charts/hot-100/2018-09-09"
response = requests.get(url, headers=headers)
#response = requests.get(url)

print(response)  # Check the response status
print(response.text)  # Print the page content if successful
