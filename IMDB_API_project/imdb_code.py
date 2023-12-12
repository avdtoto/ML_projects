from urllib.parse import urljoin


def get_movies_by_actor_soup(actor_page_soup, num_of_movies_limit=None):

    url = 'https://www.imdb.com'

    try:
        actor_element = actor_page_soup.find(class_='filmo-section-actor')
        actor_element_parent = actor_element.parent
    except:
        actor_element = actor_page_soup.find(class_='filmo-section-actress')
        actor_element_parent = actor_element.parent

    actor_element_parent.find_all(class_='ipc-metadata-list-summary-item__t')

    exclude_list = [
        'TV Series', 'Short', 'Video Game', 'Video short', 'Video', 'TV Movie',
        'TV Mini Series', 'TV Mini-Series', 'TV Series short', 'TV Special', 'Music Video']

    results = {}
    # exclude with filters
    for row in actor_element_parent.find_all('div', class_='ipc-metadata-list-summary-item__tc'):
        spans = row.find_all('span')
        should_be_excluded = False
        for span in spans:
            text = span.text.strip()
            if text in exclude_list:
                should_be_excluded = True
                break

        if should_be_excluded:
            continue

        link = row.find('a')
        # skip
        if not link['href'].endswith('_act'):
            continue

        title = link.text
        href = link['href']

        # skip unreleased movies
        if 'unrel' in href:
            continue

        movie_url = urljoin(url, href)

        if title != '':
            results[title] = movie_url

    # checking of num_of_movies_limit
    if num_of_movies_limit is not None:
        return list(results.items())[:num_of_movies_limit]
    if num_of_movies_limit is None or num_of_movies_limit > len(results):
        return list(results.items())


def get_actors_by_movie_soup(cast_page_soup, num_of_actors_limit=None):
    url = 'https://www.imdb.com'
    actors = {}
    titles = cast_page_soup.find_all('td', class_='primary_photo')

    for row in titles:
        actor_name = row.find('img')['alt']
        actor_url = row.find('a')['href']
        act_url = urljoin(url, actor_url)
        actors[actor_name] = act_url

    if num_of_actors_limit is not None:
        return list(actors.items())[:num_of_actors_limit]
    if num_of_actors_limit is None or num_of_actors_limit > len(actors):
        return list(actors.items())

