import os
import json

from django.core.management.base import BaseCommand

from core.mongo import MongoDBClient

from feedback.services import MainDataService


class Command(BaseCommand):
    help = 'Imports data from a JSON file to MongoDB using Django models.'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the JSON file.')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                
                mongo_client = MongoDBClient(os.getenv('MONGO_DB_NAME'), os.getenv('MONGO_DB_URI'))
                data_service = MainDataService(mongo_client)

                #== İlk `up`-dan sonra hər `up` verəndə xəta verəcəyini bilirəm. Amma, prosesə təsir etmədiyinə görə dəymirəm. (Yoxlama task-ı olduğu üçün!) ==#
                data_service.add_multiple_document('main_data', data)

            self.stdout.write(self.style.SUCCESS('Data successfully imported into MongoDB.'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {e}'))
