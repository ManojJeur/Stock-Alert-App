# Stock Alert Dashboard

A comprehensive stock monitoring and alert system that tracks stock prices and sends notifications via WhatsApp when price thresholds are met.

## Features

- **Real-time Stock Monitoring**: Track multiple stocks simultaneously
- **Price Alerts**: Set custom price thresholds for buy/sell alerts
- **WhatsApp Notifications**: Receive instant alerts via WhatsApp
- **Web Dashboard**: Modern React-based frontend for monitoring
- **RESTful API**: FastAPI backend for data management
- **Data Scraping**: Automated stock data collection

## Project Structure

```
StockAlertDashboard/
├── Backend/                 # FastAPI backend
│   ├── main.py             # Main application entry point
│   ├── requirements.txt    # Python dependencies
│   └── app/               # Application modules
├── Frontend/               # React frontend
│   ├── package.json       # Node.js dependencies
│   └── src/              # React components
├── Scraper/               # Stock data scraper
│   ├── scraper.py        # Main scraping logic
│   └── sample_data.json  # Sample stock data
└── alerts/               # Notification system
    ├── send_whatsapp.py  # WhatsApp integration
    └── .env             # Environment variables
```

## Quick Start

### Backend Setup
```bash
cd Backend
pip install -r requirements.txt
python main.py
```

### Frontend Setup
```bash
cd Frontend
npm install
npm start
```

### Scraper Setup
```bash
cd Scraper
python scraper.py
```

## Configuration

1. Copy `.env.example` to `.env` in the alerts directory
2. Add your WhatsApp API credentials
3. Configure stock symbols and price thresholds
4. Run the scraper to start monitoring

## Technologies Used

- **Backend**: FastAPI, Python
- **Frontend**: React, JavaScript
- **Database**: SQLite/PostgreSQL
- **Notifications**: WhatsApp Business API
- **Data Source**: Yahoo Finance API

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details
