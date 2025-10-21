from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import json
from datetime import datetime

app = FastAPI(title="Stock Alert Dashboard API", version="1.0.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
def init_db():
    conn = sqlite3.connect('stock_alerts.db')
    cursor = conn.cursor()
    
    # Create stocks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            current_price REAL,
            alert_price REAL,
            alert_type TEXT CHECK(alert_type IN ('buy', 'sell')),
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create alerts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id INTEGER,
            message TEXT NOT NULL,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (stock_id) REFERENCES stocks (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Pydantic models
class StockCreate(BaseModel):
    symbol: str
    name: str
    alert_price: float
    alert_type: str

class StockResponse(BaseModel):
    id: int
    symbol: str
    name: str
    current_price: Optional[float]
    alert_price: float
    alert_type: str
    is_active: bool
    created_at: str

class AlertResponse(BaseModel):
    id: int
    stock_id: int
    message: str
    sent_at: str

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Routes
@app.get("/")
async def root():
    return {"message": "Stock Alert Dashboard API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/stocks", response_model=List[StockResponse])
async def get_stocks():
    conn = sqlite3.connect('stock_alerts.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, symbol, name, current_price, alert_price, alert_type, is_active, created_at
        FROM stocks WHERE is_active = 1
        ORDER BY created_at DESC
    ''')
    
    stocks = []
    for row in cursor.fetchall():
        stocks.append(StockResponse(
            id=row[0],
            symbol=row[1],
            name=row[2],
            current_price=row[3],
            alert_price=row[4],
            alert_type=row[5],
            is_active=bool(row[6]),
            created_at=row[7]
        ))
    
    conn.close()
    return stocks

@app.post("/stocks", response_model=StockResponse)
async def create_stock(stock: StockCreate):
    conn = sqlite3.connect('stock_alerts.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO stocks (symbol, name, alert_price, alert_type)
            VALUES (?, ?, ?, ?)
        ''', (stock.symbol.upper(), stock.name, stock.alert_price, stock.alert_type))
        
        stock_id = cursor.lastrowid
        conn.commit()
        
        # Fetch the created stock
        cursor.execute('''
            SELECT id, symbol, name, current_price, alert_price, alert_type, is_active, created_at
            FROM stocks WHERE id = ?
        ''', (stock_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        return StockResponse(
            id=row[0],
            symbol=row[1],
            name=row[2],
            current_price=row[3],
            alert_price=row[4],
            alert_type=row[5],
            is_active=bool(row[6]),
            created_at=row[7]
        )
        
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Stock symbol already exists")

@app.put("/stocks/{stock_id}/price")
async def update_stock_price(stock_id: int, current_price: float):
    conn = sqlite3.connect('stock_alerts.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE stocks SET current_price = ? WHERE id = ?
    ''', (current_price, stock_id))
    
    conn.commit()
    conn.close()
    
    return {"message": "Price updated successfully"}

@app.get("/alerts", response_model=List[AlertResponse])
async def get_alerts():
    conn = sqlite3.connect('stock_alerts.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, stock_id, message, sent_at
        FROM alerts
        ORDER BY sent_at DESC
        LIMIT 50
    ''')
    
    alerts = []
    for row in cursor.fetchall():
        alerts.append(AlertResponse(
            id=row[0],
            stock_id=row[1],
            message=row[2],
            sent_at=row[3]
        ))
    
    conn.close()
    return alerts

@app.post("/alerts")
async def create_alert(stock_id: int, message: str):
    conn = sqlite3.connect('stock_alerts.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO alerts (stock_id, message)
        VALUES (?, ?)
    ''', (stock_id, message))
    
    conn.commit()
    conn.close()
    
    return {"message": "Alert created successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
