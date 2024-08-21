from core.mongo import DataService


class MainDataService(DataService):
    """
    MainDataService extends the DataService class to provide functionality for 
    cleaning and inserting multiple documents into a MongoDB collection.

    This class is designed to handle operations related to `MainData` data, 
    specifically for cleaning input data and batch inserting documents 
    into a specified MongoDB collection.
    """

    def cleaned_data(self, _data: list) -> list[dict]:
        """
        Cleans and standardizes a list of raw data dictionaries for insertion into MongoDB.

        This method processes a list of dictionaries, extracting relevant fields 
        and ensuring that required fields are present with default values where necessary.

        Args:
            _data (list): A list of dictionaries containing raw data.

        Returns:
            list[dict]: A list of cleaned dictionaries ready for insertion into MongoDB.
        """

        return [
            {
                "_id": i.get('_id'),
                "id": i.get('id'),
                "branch": i.get('branch', {}),
                "feedback_rate": i.get('feedback_rate', []),
            } for i in _data
        ]

    def add_multiple_document(self, collection_name, _data):
        """
        Inserts multiple cleaned documents into a specified MongoDB collection.

        This method uses the `cleaned_data` method to prepare raw data and then 
        inserts the cleaned documents into the specified MongoDB collection.

        Args:
            collection_name (str): The name of the MongoDB collection where the data will be inserted.
            _data (list): A list of raw data dictionaries to be cleaned and inserted.

        Returns:
            list: A list of IDs of the inserted documents.
        """

        return self.db_client.insert_many(collection_name, self.cleaned_data(_data))
