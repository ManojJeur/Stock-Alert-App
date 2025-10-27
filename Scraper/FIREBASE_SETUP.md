# 🔥 Firebase Setup Guide for Blinkit Scraper

## Quick Setup Steps

### 1. Install Firebase Dependencies
```bash
cd D:\Projects\StockAlertDashboard\Scraper
pip install firebase-admin
```

### 2. Get Firebase Service Account Key

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Go to **Project Settings** → **Service Accounts**
4. Click **Generate New Private Key**
5. Download the JSON file (e.g., `serviceAccountKey.json`)
6. Place it in the `Scraper` folder

### 3. Update Configuration

Edit `config.py` and update with your Firebase project details:

```python
# Firebase Configuration
FIREBASE_CONFIG = {
    "apiKey": "your-api-key",
    "authDomain": "your-project.firebaseapp.com", 
    "projectId": "your-project-id",
    "storageBucket": "your-project.appspot.com",
    "messagingSenderId": "123456789",
    "appId": "your-app-id"
}
```

### 4. Alternative: Use Service Account Key File

If you prefer using the service account key file, update `db.py`:

```python
# In db.py, replace the connect method with:
def connect(self) -> bool:
    try:
        if not firebase_admin._apps:
            # Use service account key file
            cred = credentials.Certificate('serviceAccountKey.json')
            self.app = firebase_admin.initialize_app(cred)
        else:
            self.app = firebase_admin.get_app()
        
        self.db = firestore.client()
        logger.info("Successfully connected to Firebase Firestore")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to Firebase: {e}")
        return False
```

### 5. Test Firebase Connection

```bash
python scraper.py test
```

## 🔧 Firebase Project Setup

### Create Firebase Project (if not done)

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **Create a project**
3. Enter project name: `stock-alert-dashboard`
4. Enable Google Analytics (optional)
5. Click **Create project**

### Enable Firestore Database

1. In Firebase Console, go to **Firestore Database**
2. Click **Create database**
3. Choose **Start in test mode** (for development)
4. Select a location for your database
5. Click **Done**

### Set Up Authentication (Optional)

1. Go to **Authentication** → **Sign-in method**
2. Enable **Anonymous** authentication (for simple setup)
3. Or set up **Email/Password** authentication

## 📊 Firestore Data Structure

The scraper will create documents in the `product_data` collection with this structure:

```json
{
  "product_name": "Amul Butter 500g",
  "current_price": 285.0,
  "old_price": 310.0,
  "availability": "Available",
  "stock_status": "In Stock",
  "product_url": "https://blinkit.com/products/amul-butter-500g",
  "timestamp": "2025-01-21T10:35:00Z"
}
```

## 🔒 Security Rules (Optional)

For production, update your Firestore security rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow read/write access to product_data collection
    match /product_data/{document} {
      allow read, write: if true; // For development
      // For production, use proper authentication:
      // allow read, write: if request.auth != null;
    }
  }
}
```

## 🚀 Testing Firebase Integration

### Test Connection
```bash
python scraper.py test
```

### Test with Sample Data
```bash
python example_usage.py
```

### Run Scraper
```bash
python scraper.py scrape
```

## 🔧 Troubleshooting

### Common Issues

1. **Authentication Error**
   - Check service account key file path
   - Verify Firebase project ID
   - Ensure Firestore is enabled

2. **Permission Denied**
   - Check Firestore security rules
   - Verify service account permissions
   - Ensure project is active

3. **Connection Timeout**
   - Check internet connection
   - Verify Firebase project is not suspended
   - Check firewall settings

### Debug Mode

Enable debug logging in `config.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📱 Integration with Your Dashboard

The Firebase data can be easily consumed by your frontend:

```javascript
// Example: Get all products
import { collection, getDocs } from 'firebase/firestore';

const getProducts = async () => {
  const querySnapshot = await getDocs(collection(db, 'product_data'));
  const products = [];
  querySnapshot.forEach((doc) => {
    products.push({ id: doc.id, ...doc.data() });
  });
  return products;
};
```

## 🎯 Next Steps

1. ✅ Install Firebase dependencies
2. ✅ Set up Firebase project
3. ✅ Configure service account
4. ✅ Test connection
5. ✅ Add product URLs to `urls.txt`
6. ✅ Run scraper: `python scraper.py scrape`

Your Blinkit scraper is now ready to work with Firebase! 🎉
