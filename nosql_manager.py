from pymongo import MongoClient
from typing import Dict, Any, List, Optional
import json
from datetime import datetime

class NoSQLManager:
    def __init__(self, connection_string: str = "mongodb://localhost:27017/", db_name: str = "cis261_nosql"):
        try:
            self.client = MongoClient(connection_string)
            self.db = self.client[db_name]
            self.client.admin.command('ping')
            self.connected = True
        except Exception:
            self.connected = False
            self.client = None
            self.db = None
    
    def is_connected(self) -> bool:
        return self.connected
    
    def create_collection(self, collection_name: str, sample_doc: Dict[str, Any] = None) -> bool:
        if not self.connected:
            return False
        try:
            if collection_name not in self.db.list_collection_names():
                collection = self.db[collection_name]
                if sample_doc:
                    collection.insert_one({**sample_doc, "_created": datetime.now()})
                return True
            return False
        except Exception:
            return False
    
    def insert_document(self, collection_name: str, document: Dict[str, Any]) -> bool:
        if not self.connected:
            return False
        try:
            collection = self.db[collection_name]
            document["_created"] = datetime.now()
            result = collection.insert_one(document)
            return bool(result.inserted_id)
        except Exception:
            return False
    
    def find_documents(self, collection_name: str, query: Dict[str, Any] = None, limit: int = 0) -> List[Dict[str, Any]]:
        if not self.connected:
            return []
        try:
            collection = self.db[collection_name]
            query = query or {}
            cursor = collection.find(query)
            if limit > 0:
                cursor = cursor.limit(limit)
            return [doc for doc in cursor]
        except Exception:
            return []
    
    def update_documents(self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        if not self.connected:
            return 0
        try:
            collection = self.db[collection_name]
            update["_updated"] = datetime.now()
            result = collection.update_many(query, {"$set": update})
            return result.modified_count
        except Exception:
            return 0
    
    def delete_documents(self, collection_name: str, query: Dict[str, Any]) -> int:
        if not self.connected:
            return 0
        try:
            collection = self.db[collection_name]
            result = collection.delete_many(query)
            return result.deleted_count
        except Exception:
            return 0
    
    def list_collections(self) -> List[str]:
        if not self.connected:
            return []
        try:
            return self.db.list_collection_names()
        except Exception:
            return []
    
    def drop_collection(self, collection_name: str) -> bool:
        if not self.connected:
            return False
        try:
            self.db[collection_name].drop()
            return True
        except Exception:
            return False
    
    def close(self):
        if self.client:
            self.client.close()
