import os

from pymongo import MongoClient

from abc import (
    ABC,
    abstractmethod
)


class MongoDBClient:
    """
    MongoDBClient provides a simple interface for interacting with a MongoDB database.

    This class handles the creation of a MongoDB client, allows for common database operations 
    such as inserting documents, querying collections, and closing the connection. 
    It abstracts the lower-level pymongo operations to make database interactions easier.
    """

    def __init__(self, db_name=None, uri="mongodb://localhost:27017/"):
        """
        Initializes the MongoDBClient instance with a specified database name and connection URI.

        Args:
            db_name (str, optional): The name of the database to connect to. 
                                     If not provided, the value is fetched from the MONGO_DB_NAME environment variable.
            uri (str, optional): The MongoDB connection URI. Defaults to "mongodb://localhost:27017/".

        Attributes:
            client (MongoClient): The MongoClient instance connected to the MongoDB server.
            db (Database): The database instance to interact with.
        """

        self.client = MongoClient(uri)
        self.db_name = db_name or os.getenv('MONGO_DB_NAME')
        self.db = self.client[self.db_name]

    def get_collection(self, collection_name, *, apply_pipeline=False, pipeline=None):
        """
        Retrieves a collection object by name.

        Args:
            collection_name (str): The name of the collection to retrieve.

        Returns:
            Collection: The MongoDB collection object.
        """

        data = self.db[collection_name]

        if apply_pipeline and pipeline is not None:
            data = self._apply_pipeline(data, pipeline)
        elif apply_pipeline and pipeline is None:
            raise ValueError("Pipeline is required when 'apply_pipeline' is set to True.")

        return data

    def _apply_pipeline(self, data, pipeline):
        """
        Applies an aggregation pipeline to a collection and returns the results.

        Args:
            collection_name (str): The name of the collection to aggregate.
            pipeline (list): The aggregation pipeline to apply.

        Returns:
            CommandCursor: A cursor to the documents generated by the pipeline.
        """

        return data.aggregate(pipeline)

    def insert_one(self, collection_name, document):
        """
        Inserts a single document into a specified collection.

        Args:
            collection_name (str): The name of the collection where the document will be inserted.
            document (dict): The document to be inserted.

        Returns:
            ObjectId: The ID of the inserted document.
        """

        collection = self.get_collection(collection_name)
        result = collection.insert_one(document)
        return result.inserted_id

    def insert_many(self, collection_name, documents):
        """
        Inserts multiple documents into a specified collection.

        Args:
            collection_name (str): The name of the collection where the documents will be inserted.
            documents (list[dict]): A list of dictionaries representing the documents to be inserted.

        Returns:
            list[ObjectId]: A list of IDs of the inserted documents.
        """

        collection = self.get_collection(collection_name)
        result = collection.insert_many(documents)
        return result.inserted_ids

    def find(self, collection_name, query):
        """
        Finds documents in a specified collection that match a given query.

        Args:
            collection_name (str): The name of the collection to query.
            query (dict): A dictionary representing the query filter.

        Returns:
            list[dict]: A list of dictionaries representing the matching documents.
        """

        collection = self.get_collection(collection_name)
        return list(collection.find(query))

    def close(self):
        """
        Closes the MongoDB client connection.

        This method should be called when the database connection is no longer needed.
        """

        self.client.close()


class DataService(ABC):
    """
    DataService is an abstract base class that defines a template for services 
    interacting with a MongoDB database through a MongoDBClient instance.

    This class enforces the implementation of the `cleaned_data` method in subclasses 
    to ensure data cleaning or transformation logic is provided. It acts as a base for 
    any service class that needs to work with MongoDB data.
    """

    def __init__(self, db_client: MongoDBClient):
        """
        Initializes the DataService instance with a MongoDB client.

        Args:
            db_client (MongoDBClient): An instance of MongoDBClient used to interact with the database.

        Attributes:
            db_client (MongoDBClient): Stores the MongoDB client for database operations.
        """

        self.db_client = db_client

    @abstractmethod
    def cleaned_data(self, _data) -> list:
        """
        Abstract method that must be implemented by subclasses to clean or transform data.

        Args:
            _data: The raw data that needs to be cleaned or transformed.

        Returns:
            list: A list of cleaned or transformed data. The implementation should be provided by subclasses.
        """

        return None
