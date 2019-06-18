import logging
import uuid
import boto3
from boto3.dynamodb.conditions import Attr, Key

logger = logging.getLogger()
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('sw_planets')

class DBConnection:
    def insert_planet(self, planet):
        planet['planet_id'] = str(uuid.uuid4())

        try:
            table.put_item(Item=planet)
        except Exception as e:
            logger.exception("DBConnection::insert_planet")
            raise Exception('Error to insert a new planet')


    def retrieve_planet(self, search_by, value):
        try:
            result = table.scan(FilterExpression=Attr(search_by).eq(value))
            if result['Count'] < 1:
                return {}
            return result['Items'][0]
        except Exception as e:
            logger.exception("DBConnection::retrieve_planet")
            raise Exception('Error to retrieve planet with {} = {}'.format(search_by, value))


    def retrieve_all_planets(self):
        try:
            items = table.scan()
            return items['Items']
        except Exception as e:
            logger.exception("DBConnection::retrieve_all_planets")
            raise Exception('Error to retrieve all planets')


    def delete_planet(self, planet_id):
        try:
            response = table.query(KeyConditionExpression=Key('planet_id').eq(planet_id))
            items = response['Items']
            if not items:
                return False

            table.delete_item(Key={'planet_id': planet_id})
            return True
        except Exception as e:
            logger.exception("DBConnection::delete_planet")
            raise Exception('Error to delete planet id={}'.format(planet_id))
