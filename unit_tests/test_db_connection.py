import unittest
import boto3
from boto3.dynamodb.conditions import Attr, Key
from moto import mock_dynamodb2
from db_connection import DBConnection

class TestDBConnection(unittest.TestCase):
    def create_table(self):
        dynamodb = boto3.resource('dynamodb')

        table = dynamodb.create_table(
            TableName='sw_planets',
            KeySchema=[
                {
                    'AttributeName': 'planet_id',
                    'KeyType': 'HASH'  # primary key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'planet_id',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        return table


    @mock_dynamodb2
    def test_insert_planet(self):
        planet = {
        	"planet_name": "Marino",
        	"terrain": "blah",
        	"climate": "Seco"
        }

        table = self.create_table()
        db = DBConnection()
        db.insert_planet(planet)
        response = table.scan(FilterExpression=Attr('planet_name').eq('Marino'))
        if 'Items' in response:
            item = response['Items'][0]

        self.assertTrue('planet_id' in item)
        self.assertEquals(item['planet_name'], 'Marino')
        self.assertEquals(item['terrain'], 'blah')
        self.assertEquals(item['climate'], 'Seco')


    @mock_dynamodb2
    def test_retrieve_planet(self):
        planet_id = 'xxxxxxxxxxxx'
        planet = {
            "planet_id": planet_id,
        	"planet_name": "Renata",
        	"terrain": "Arenoso",
        	"climate": "Deserto"
        }

        table = self.create_table()
        table.put_item(Item=planet)
        db = DBConnection()
        response = db.retrieve_planet('planet_id', planet_id)

        self.assertEquals(response, planet)


    @mock_dynamodb2
    def test_retrieve_planet_not_found(self):
        planet_id = 'yyyyyyyyyyy'
        planet = {
            "planet_id": planet_id,
        	"planet_name": "Marcela",
        	"terrain": "Arenoso",
        	"climate": "Deserto"
        }

        self.create_table()
        db = DBConnection()
        response = db.retrieve_planet('planet_id', planet_id)

        self.assertEquals(response, {})

    @mock_dynamodb2
    def test_retrieve_all_planets(self):
        planet1 = {
            "planet_id": 'yyyyyyyyyyy',
        	"planet_name": "Marcela",
        	"terrain": "Arenoso",
        	"climate": "Deserto"
        }
        planet2 = {
            "planet_id": 'xxxxxxxxxxxx',
        	"planet_name": "Renata",
        	"terrain": "Arenoso",
        	"climate": "Deserto"
        }

        table = self.create_table()
        table.put_item(Item=planet1)
        table.put_item(Item=planet2)
        db = DBConnection()
        response = db.retrieve_all_planets()
        print(response)

        self.assertEquals(response[0], planet1)
        self.assertEquals(response[1], planet2)


    @mock_dynamodb2
    def test_delete_planet(self):
        planet_id = 'yyyyyyyyyyy'
        planet = {
            "planet_id": planet_id,
        	"planet_name": "Marcela",
        	"terrain": "Arenoso",
        	"climate": "Deserto"
        }

        table = self.create_table()
        table.put_item(Item=planet)
        db = DBConnection()
        response = db.delete_planet(planet_id)

        assert bool(response) == True


    @mock_dynamodb2
    def test_delete_planet_not_found(self):
        planet_id = 'xxxxxxxxxxxx'

        table = self.create_table()
        db = DBConnection()
        response = db.delete_planet(planet_id)

        assert bool(response) == False



if __name__ == '__main__':
    unittest.main()
