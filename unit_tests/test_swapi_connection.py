import unittest
from unittest import mock
from swapi_connection import StarWarsAPIConnection

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    values = args[0].split('=')
    if values[1] == 'Alderaan':
        body = {
        	"count": 1,
        	"results": [
        		{
        			"name": "Alderaan",
        			"climate": "temperate",
        			"terrain": "grasslands, mountains",
        			"films": [
        				"https://swapi.co/api/films/6/",
        				"https://swapi.co/api/films/1/"
        			]
        		}
        	]
        }
        return MockResponse(body, 200)
    elif values[1] == 'Blah':
        body = {
        	"count": 0,
        	"results": []
        }
        return MockResponse(body, 200)

    return MockResponse({"count": 2}, 500)


class TestSWAPIConection(unittest.TestCase):
    @mock.patch('swapi_connection.requests.get', side_effect=mocked_requests_get)
    def test_fetch_films(self, mock_get):
        planet_name = 'Alderaan'
        expected_films = 2
        expected_url = 'https://swapi.co/api/planets/?search=Alderaan'
        swapi = StarWarsAPIConnection()
        films = swapi.fetch_films(planet_name)
        self.assertEqual(films, expected_films)
        self.assertIn(mock.call(expected_url), mock_get.call_args_list)

    @mock.patch('swapi_connection.requests.get', side_effect=mocked_requests_get)
    def test_fetch_films_planet_not_found(self, mock_get):
        planet_name = 'Blah'
        no_films = 0
        expected_url = 'https://swapi.co/api/planets/?search=Blah'
        swapi = StarWarsAPIConnection()
        films = swapi.fetch_films(planet_name)
        self.assertEqual(films, no_films)
        self.assertIn(mock.call(expected_url), mock_get.call_args_list)

    @mock.patch('swapi_connection.requests.get', side_effect=mocked_requests_get)
    def test_fetch_films_raise_exception(self, mock_get):
        with self.assertRaises(Exception) as context:
            swapi = StarWarsAPIConnection()
            films = swapi.fetch_films("Test")
        self.assertTrue('Error to fetch films from swapi' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
