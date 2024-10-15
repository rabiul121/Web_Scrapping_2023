import requests
from bs4 import BeautifulSoup

# main urls
base_url = 'https://subslikescript.com'
movie_list_url = f'{base_url}/movies_letter-A'

# step 1: fetch the main  page
response = requests.get(movie_list_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # step 2: extract the list of movie links
    movie_links = []
    movie_list = soup.find('article', class_='main-article')
    for link in movie_list.find_all('a', href=True):
        movie_links.append(base_url + link['href'])  # full url for each movie\

    # step 3: visit each movie page and extract the title and script
    for movie_url in movie_links:
        movie_response = requests.get(movie_url)
        if movie_response.status_code == 200:
            movie_soup = BeautifulSoup(movie_url, 'html.parser')

            # extract movie title
            title = movie_soup.find('h1').get_text()

            # extract movie script
            script = movie_soup.find('div', class_='full-script')
            if script:
                script_text = script.get_text(separator='\n').strip()
            else:
                print("Script not found")
            with open(f'{title}.txt', 'w') as file:
                file.write(script_text, encoding='utf-8')
        else:
            print(f"Failed to fetch {movie_url}")
else:
    print("Failed to fetch the main page")
