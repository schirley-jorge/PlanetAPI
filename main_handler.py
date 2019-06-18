import tornado.ioloop
import tornado.web
import logging
import sys
import tornado.httpserver
import tornado.log
import tornado.options
import json
from swapi_connection import StarWarsAPIConnection
from db_connection import DBConnection

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

tornado.options.define("access_to_stdout", default=False, help="Log tornado.access to stdout")

class Planets(tornado.web.RequestHandler):
    def get(self):
        try:
            db = DBConnection()
            planets = db.retrieve_all_planets()

            for planet in planets:
                planet['films'] = fetch_films(planet['planet_name'])

            self.write({'planets': planets})
        except Exception as e:
            logger.exception("Planets::get")
            raise Exception('Error to get all planets')


class AddPlanet(tornado.web.RequestHandler):
    def post(self):
        planet = json.loads(self.request.body)

        if 'planet_name' and 'climate' and 'terrain' not in planet:
            raise Exception('Missing body arguments')

        db = DBConnection()
        db.insert_planet(planet)
        self.write({'planet': planet})


class SearchPlanet(tornado.web.RequestHandler):
    def get(self):
        try:
            search_by = self.get_argument("search_by")
            value = self.get_argument("value")

            db = DBConnection()
            planet = db.retrieve_planet(search_by, value)

            if not planet:
                self.finish("Planet not found")
                return

            planet['films'] = fetch_films(planet['planet_name'])
            self.write({'planet': planet})
        except Exception as e:
            logger.exception("SearchPlanet::get")
            raise Exception('Error to search planet')


class DeletePlanet(tornado.web.RequestHandler):
    def delete(self, planet_id):
        try:
            db = DBConnection()
            result = db.delete_planet(planet_id)

            if not result:
                self.finish("Planet not found")
                return

            self.write({'message': 'Planet with id={} was deleted'.format(planet_id)})
        except Exception as e:
            logger.exception("DeletePlanet::delete")
            raise Exception('Error to delete planet')


def fetch_films(planet_name):
    swapi = StarWarsAPIConnection()
    films = swapi.fetch_films(planet_name)
    return films


def init_logging(access_to_stdout=False):
    if access_to_stdout:
        access_log = logging.getLogger('tornado.access')
        access_log.propagate = False
        access_log.setLevel(logging.DEBUG)
        stdout_handler = logging.StreamHandler(sys.stdout)
        access_log.addHandler(stdout_handler)


def bootstrap():
    tornado.options.parse_command_line(final=True)
    init_logging(tornado.options.options.access_to_stdout)


def start_server():
    urls = [
        ("/api/planets/", Planets),
        ("/api/add_planet", AddPlanet),
        ("/api/planet", SearchPlanet),
        (r"/api/delete_planet/([^/]+)?", DeletePlanet)
    ]
    application = tornado.web.Application(urls, debug=True)
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    bootstrap()
    logger.info("API STARTED")
    start_server()
