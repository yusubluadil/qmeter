import os

from django.shortcuts import render
from django.views import View

from core.mongo import MongoDBClient

from feedback.pipelines import TASK_PIPELINE


class MainDataView(View):
    def get(self, request):
        mongo_client = MongoDBClient(os.getenv('MONGO_DB_NAME'), os.getenv('MONGO_DB_URI'))
        result = mongo_client.get_collection('main_data', apply_pipeline=True, pipeline=TASK_PIPELINE)
        mongo_client.close()

        data = {
            'result': result
        }

        return render(request, 'base.html', data)
