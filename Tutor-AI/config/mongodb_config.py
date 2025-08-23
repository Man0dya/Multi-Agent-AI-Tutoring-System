import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MongoDBConfig:
    """MongoDB configuration and connection management"""
    
    def __init__(self):
        # MongoDB connection settings
        self.mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.database_name = os.getenv('MONGODB_DATABASE', 'tutor_ai')
        self.client = None
        self.db = None
        
    def connect(self):
        """Establish connection to MongoDB"""
        try:
            self.client = MongoClient(self.mongo_uri)
            self.db = self.client[self.database_name]
            
            # Test connection
            self.client.admin.command('ping')
            print(f"✅ Connected to MongoDB: {self.database_name}")
            return True
            
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            return False
    
    def get_database(self):
        """Get database instance"""
        if not self.db:
            self.connect()
        return self.db
    
    def get_collection(self, collection_name):
        """Get a specific collection"""
        db = self.get_database()
        return db[collection_name]
    
    def close_connection(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("🔌 MongoDB connection closed")
    
    def create_indexes(self):
        """Create necessary indexes for optimal performance"""
        try:
            # Content collection indexes
            content_collection = self.get_collection('content')
            content_collection.create_index([("subject", 1)])
            content_collection.create_index([("topic", 1)])
            content_collection.create_index([("type", 1)])
            content_collection.create_index([("created_at", -1)])
            
            # User progress indexes
            progress_collection = self.get_collection('user_progress')
            progress_collection.create_index([("user_id", 1)])
            progress_collection.create_index([("subject", 1)])
            progress_collection.create_index([("timestamp", -1)])
            
            # Questions indexes
            questions_collection = self.get_collection('questions')
            questions_collection.create_index([("subject", 1)])
            questions_collection.create_index([("difficulty", 1)])
            questions_collection.create_index([("bloom_level", 1)])
            
            print("✅ MongoDB indexes created successfully")
            
        except Exception as e:
            print(f"❌ Error creating indexes: {e}")
    
    def get_stats(self):
        """Get database statistics"""
        try:
            db = self.get_database()
            collections = db.list_collection_names()
            
            stats = {
                'database': self.database_name,
                'collections': len(collections),
                'collection_names': collections
            }
            
            for collection_name in collections:
                collection = db[collection_name]
                stats[f'{collection_name}_count'] = collection.count_documents({})
            
            return stats
            
        except Exception as e:
            return {'error': str(e)}

# Global MongoDB instance
mongodb_config = MongoDBConfig()
