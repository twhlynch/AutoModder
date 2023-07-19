import time, requests, webbrowser

def get_search_results(search_term):

    url = 'https://oculusdb.rui2015.me/api/v1/search/' + search_term + "?headsets=RIFT,LAGUNA,MONTEREY,HOLLYWOOD,SEACLIFF,GEARVR,PACIFIC"
    response = requests.get(url)

    return response.json()

def get_app_link(term):

    results = get_search_results(term)
    for i in range(len(results)):
        print(f'{i} | {results[i]["appName"]}: \u001B[32m{results[i]["packageName"]}\u001B[0m | {results[i]["id"]}')

    selected = int(input('Select an app: '))

    return f'https://www.oculus.com/experiences/quest/{results[selected]["id"]}'

links = []
list = input('List of apps: ').split(', ')

for term in list:
    links.append(get_app_link(term))

print(f'Opening {links} in 5s...')
time.sleep(5)

for link in links:
    webbrowser.open(link)