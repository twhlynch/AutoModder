import time, requests, webbrowser, os, shutil, subprocess, threading, argparse

def get_search_results(search_term):

    url = 'https://oculusdb.rui2015.me/api/v1/search/' + search_term + "?headsets=RIFT,LAGUNA,MONTEREY,HOLLYWOOD,SEACLIFF,GEARVR,PACIFIC"
    response = requests.get(url)

    return response.json()

def get_app_link(term):

    results = get_search_results(term)
    if len(results) == 0:
        return ""
    for i in range(len(results)):
        print(f'{i} | {results[i]["appName"]}: \u001B[32m{results[i]["packageName"]}\u001B[0m | {results[i]["id"]}')

    print('Select an app: ')
    selected = 0
    def selectInput():
        selected = int(input())
    input_thread = threading.Thread(target=selectInput)
    input_thread.daemon = True
    input_thread.start()
    input_thread.join(5)

    return f'https://www.oculus.com/experiences/quest/{results[selected]["id"]}'

def parse_list(list):
    apps = [app.strip() for app in list.split(',')]
    return apps

def main(list):
    links = []

    template = "https://www.oculus.com/experiences/quest/"
    template2 = "https://www.oculus.com/experiences/app/"
    for term in list:
        if term.startswith(template) or term.startswith(template2):
            links.append(term.split("?")[0])
        else:
            link = get_app_link(term)
            links.append(link)

    print(f'Opening {links} in 5s...')
    time.sleep(5)

    for link in links:
        webbrowser.open(link)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("app_list", type=parse_list, help="Comma-separated list of app names")
    args = parser.parse_args()

    main(args.app_list)