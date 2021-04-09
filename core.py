import pandas as pd
from bs4 import BeautifulSoup
import requests
import json


def load_subcategories():
    url_categories = "https://cursos.alura.com.br/api/categorias"
    response = do_request(url_categories)

    categories = json.loads(response.text)
    subcategories = pd.DataFrame(columns=['cat', 'subcat', 'slug', 'cor', 'posts'])
    i = 0

    for category in categories:
        for sub_cat in category['subcategorias']:
            posts = count_posts(sub_cat['slug'], filter='sem-resposta')
            subcategories.loc[i] = [category['nome'], sub_cat['nome'], sub_cat['slug'], category['cor'], posts]
            i += 1

    subcategories.to_csv("posts_by_subcategories.csv")
    return subcategories


def count_posts(slug, per_page=20, filter='todos'):
    url = f"https://cursos.alura.com.br/forum/subcategoria-{slug}/{filter}/1"
    response = do_request(url)
    soup = BeautifulSoup(response.text)

    pages = 1
    last_link = soup.select('nav.busca-paginacao a.paginationLink')
    if last_link:
        pages = int(last_link[-1].get_text())

    if pages == 1:
        count = len(soup.find_all('li', {'class': 'forumList-item'}))
    else:
        url_last_page = f"https://cursos.alura.com.br/forum/subcategoria-{slug}/{filter}/{pages}"
        response = do_request(url_last_page)
        soup = BeautifulSoup(response.text)
        count = len(soup.find_all('li', {'class': 'forumList-item'}))

    total_count = ((pages - 1) * per_page) + count

    return total_count


def do_request(url):
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception('error {}'.format(response.status_code))

    return response
