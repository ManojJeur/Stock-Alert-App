"""
Firebase Firestore operations for Blinkit Product Scraper
"""

import firebase_admin
from firebase_admin import credentials, firestore
import logging
from typing import Optional, Dict, Any, List
from contextlib import contextmanager
from datetime import datetime
from config import FIREBASE_CONFIG, COLLECTION_NAME

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FirebaseManager:
    """Handles all Firebase Firestore operations for the scraper"""
    
    def __init__(self):
        self.db = None
        self.app = None
    
    def connect(self) -> bool:
        """Initialize Firebase connection"""
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                # Initialize Firebase Admin SDK with service account key
                cred = credentials.Certificate('serviceAccountKey.json')
                self.app = firebase_admin.initialize_app(cred)
                logger.info("Firebase Admin SDK initialized with service account key")
            else:
                self.app = firebase_admin.get_app()
                logger.info("Using existing Firebase app")
            
            # Get Firestore client
            self.db = firestore.client()
            logger.info("Successfully connected to Firebase Firestore")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Firebase: {e}")
            return False
    
    def disconnect(self):
        """Close Firebase connection"""
        # Firebase connections are managed automatically
        logger.info("Firebase connection closed")
    
    def create_collection(self) -> bool:
        """Create the collection if it doesn't exist (Firestore creates collections automatically)"""
        try:
            # Firestore creates collections automatically when first document is added
            # We'll test by adding a dummy document and then deleting it
            test_doc = self.db.collection(COLLECTION_NAME).document('test')
            test_doc.set({'test': True})
            test_doc.delete()
            logger.info("Firestore collection verified/created successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to create/verify collection: {e}")
            return False
    
    def insert_or_update_product(self, product_data: Dict[str, Any]) -> bool:
        """
        Insert new product or update existing product data
        Uses document ID based on product URL for upsert functionality
        """
        try:
            # Use product URL as document ID for easy upsert
            doc_id = product_data.get('product_url', '').replace('/', '_').replace(':', '_')
            
            # Add timestamp if not present
            if 'timestamp' not in product_data:
                product_data['timestamp'] = datetime.now()
            
            # Set document in Firestore (this will create or update)
            doc_ref = self.db.collection(COLLECTION_NAME).document(doc_id)
            doc_ref.set(product_data)
            
            logger.info(f"Product data upserted: {product_data.get('product_name', 'Unknown')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to insert/update product data: {e}")
            return False
    
    def get_all_products(self) -> List[Dict[str, Any]]:
        """Retrieve all products from Firestore"""
        try:
            products = []
            docs = self.db.collection(COLLECTION_NAME).stream()
            
            for doc in docs:
                product_data = doc.to_dict()
                product_data['id'] = doc.id
                products.append(product_data)
            
            # Sort by timestamp descending
            products.sort(key=lambda x: x.get('timestamp', datetime.min), reverse=True)
            return products
            
        except Exception as e:
            logger.error(f"Failed to retrieve products: {e}")
            return []
    
    def get_product_by_url(self, product_url: str) -> Optional[Dict[str, Any]]:
        """Get specific product by URL"""
        try:
            doc_id = product_url.replace('/', '_').replace(':', '_')
            doc_ref = self.db.collection(COLLECTION_NAME).document(doc_id)
            doc = doc_ref.get()
            
            if doc.exists:
                product_data = doc.to_dict()
                product_data['id'] = doc.id
                return product_data
            return None
            
        except Exception as e:
            logger.error(f"Failed to retrieve product by URL: {e}")
            return None
    
    def delete_product(self, product_url: str) -> bool:
        """Delete a product from Firestore"""
        try:
            doc_id = product_url.replace('/', '_').replace(':', '_')
            doc_ref = self.db.collection(COLLECTION_NAME).document(doc_id)
            doc_ref.delete()
            logger.info(f"Product deleted: {product_url}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete product: {e}")
            return False
    
    def get_products_count(self) -> int:
        """Get total number of products in Firestore"""
        try:
            docs = self.db.collection(COLLECTION_NAME).stream()
            count = sum(1 for _ in docs)
            return count
        except Exception as e:
            logger.error(f"Failed to get products count: {e}")
            return 0


@contextmanager
def get_db_connection():
    """Context manager for Firebase connections"""
    db = FirebaseManager()
    try:
        if db.connect():
            yield db
    finally:
        db.disconnect()


def test_connection() -> bool:
    """Test Firebase connection and collection creation"""
    try:
        with get_db_connection() as db:
            if db.create_collection():
                logger.info("Firebase connection test successful")
                return True
            return False
    except Exception as e:
        logger.error(f"Firebase connection test failed: {e}")
        return False


if __name__ == "__main__":
    # Test the Firebase connection
    test_connection()
