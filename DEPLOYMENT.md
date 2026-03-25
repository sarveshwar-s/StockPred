# StockPred Flask Application - Deployment Guide

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your actual credentials
   ```

3. **Required Environment Variables**
   - `DB_HOST`: Your MySQL database host
   - `DB_USER`: Database username
   - `DB_PASSWORD`: Database password
   - `DB_NAME`: Database name (default: trading)
   - `FINANCIAL_API_KEY`: Financial Modeling Prep API key
   - `IEX_API_KEY`: IEX Cloud API key
   - `SECRET_KEY`: Flask session secret key

4. **Run the Application**
   ```bash
   # Development
   python test.py
   
   # Production with Gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 test:app
   ```

## API Keys Required

1. **Financial Modeling Prep**: Get API key from https://financialmodelingprep.com/
2. **IEX Cloud**: Get API key from https://iexcloud.io/

## Database Setup

Ensure your MySQL database has the required `intrasymbols` table:

```sql
CREATE TABLE intrasymbols (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(255),
    price DECIMAL(10,2),
    stock_symbol VARCHAR(10),
    exchange VARCHAR(50)
);
```

## Security Notes

- Never commit `.env` file to version control
- Use strong, unique passwords for database
- Rotate API keys regularly
- Use HTTPS in production
- Set `DEBUG=False` in production

## Monitoring

The application includes proper logging. Monitor logs for:
- Database connection errors
- API rate limit warnings
- Prediction model errors