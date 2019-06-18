import logging
from botocore.vendored import requests

logger = logging.getLogger()

class StarWarsAPIConnection:
    def fetch_films(self, planet_name):
        url = 'https://swapi.co/api/planets/?search={}'.format(planet_name)

        try:
            response = requests.get(url)
            if response.json().get('count') < 1:
                return 0

            results = response.json().get('results')
            films = results[0].get('films')
            return len(films)
        except Exception as e:
            logger.exception("StarWarsAPIConnection::fetch_films")
            raise Exception('Error to fetch films from swapi')
