import os
from flask import Flask, render_template, request, jsonify
import requests
import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
import logging
from intra import intrapred
from sklearns import prediction_close
from news import news_analysis
from tweets import twitter_analysis
from intratest import intratestpred

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Database configuration from environment variables
DB_CONFIG = {
    'host': os.environ.get('DB_HOST'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'database': os.environ.get('DB_NAME', 'trading'),
    'autocommit': True
}

# API configuration
FINANCIAL_API_BASE = "https://financialmodelingprep.com/api/v3"
IEX_API_KEY = os.environ.get('IEX_API_KEY')
FINANCIAL_API_KEY = os.environ.get('FINANCIAL_API_KEY', '')

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        yield connection
    except Error as e:
        logger.error(f"Database error: {e}")
        if connection:
            connection.rollback()
        raise
    finally:
        if connection and connection.is_connected():
            connection.close()

def make_api_request(url, params=None):
    """Helper function for making API requests with error handling"""
    try:
        if FINANCIAL_API_KEY:
            params = params or {}
            params['apikey'] = FINANCIAL_API_KEY
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        return None

def get_company_symbols():
    """Get company symbols from database"""
    with get_db_connection() as db:
        cursor = db.cursor()
        cursor.execute("SELECT company_name, price, stock_symbol, exchange FROM intrasymbols")
        results = cursor.fetchall()
        
        companies = []
        for row in results:
            companies.append({
                'name': row[0],
                'price': row[1], 
                'symbol': row[2],
                'exchange': row[3]
            })
        return companies

def get_company_by_symbol(symbol):
    """Get company name by symbol"""
    with get_db_connection() as db:
        cursor = db.cursor()
        cursor.execute("SELECT company_name FROM intrasymbols WHERE stock_symbol = %s", (symbol,))
        result = cursor.fetchone()
        return result[0] if result else None

@app.route("/")
def index():
    """Main page route"""
    return render_template("login.html")

@app.route("/user/<username>")
def show_user_name(username):
    """Display username - consider removing if not used"""
    return f"Username is: {username}"

@app.route("/investment/complist")
def list_company():
    """List active companies"""
    api_url = f"{FINANCIAL_API_BASE}/stock/actives"
    data = make_api_request(api_url)
    
    if not data:
        return render_template("complist.html", clist=[], error="Unable to fetch company list")
    
    return render_template("complist.html", clist=data)

@app.route("/investment/compdetails", methods=["POST", "GET"])
def details_company():
    """Get detailed company information"""
    if request.method != "POST":
        return render_template("compdetails.html", error="Invalid request method")
    
    company_name = request.form.get("companyname", "").strip()
    if not company_name:
        return render_template("compdetails.html", error="Company name is required")
    
    # Build API URLs
    urls = {
        'rating': f"{FINANCIAL_API_BASE}/company/rating/{company_name}",
        'dcf': f"{FINANCIAL_API_BASE}/company/discounted-cash-flow/{company_name.upper()}",
        'profile': f"{FINANCIAL_API_BASE}/company/profile/{company_name}"
    }
    
    # Fetch data from multiple APIs
    data = {}
    for key, url in urls.items():
        result = make_api_request(url)
        data[key] = result if result else {}
    
    return render_template(
        "compdetails.html", 
        data=company_name,
        rating=data['rating'],
        dcf=data['dcf'],
        profile=data['profile']
    )

@app.route("/investment/enterprise/<enterprise_name>")
def show_enterprise_details(enterprise_name):
    """Get enterprise value details"""
    if not enterprise_name:
        return render_template("enterprisedetails.html", error="Enterprise name is required")
    
    urls = {
        'annual': f"{FINANCIAL_API_BASE}/enterprise-value/{enterprise_name}",
        'quarterly': f"{FINANCIAL_API_BASE}/enterprise-value/{enterprise_name}?period=quarter"
    }
    
    data = {}
    for key, url in urls.items():
        result = make_api_request(url)
        data[key] = result if result else {}
    
    return render_template(
        "enterprisedetails.html",
        enterpriseannual=data['annual'],
        enterprisequarter=data['quarterly']
    )

@app.route("/investment/finstatement/<finance_name>")
def show_finance_details(finance_name):
    """Get financial statement growth"""
    if not finance_name:
        return render_template("fingrowth.html", error="Finance name is required")
    
    api_url = f"{FINANCIAL_API_BASE}/financial-statement-growth/{finance_name}"
    data = make_api_request(api_url)
    
    return render_template("fingrowth.html", financestate=data or {})

@app.route("/investment/finstate/<fin_company_name>")
def show_financial_state(fin_company_name):
    """Get comprehensive financial statements"""
    if not fin_company_name:
        return render_template("financestate.html", error="Company name is required")
    
    # Build all financial API URLs
    apis = {
        'income_annual': f"{FINANCIAL_API_BASE}/financials/income-statement/{fin_company_name}",
        'income_quarter': f"{FINANCIAL_API_BASE}/financials/income-statement/{fin_company_name}?period=quarter",
        'balance_annual': f"{FINANCIAL_API_BASE}/financials/balance-sheet-statement/{fin_company_name}",
        'balance_quarter': f"{FINANCIAL_API_BASE}/financials/balance-sheet-statement/{fin_company_name}?period=quarter",
        'cashflow_annual': f"{FINANCIAL_API_BASE}/financials/cash-flow-statement/{fin_company_name}",
        'cashflow_quarter': f"{FINANCIAL_API_BASE}/financials/cash-flow-statement/{fin_company_name}?period=quarter"
    }
    
    # Fetch all data
    financial_data = {}
    for key, url in apis.items():
        result = make_api_request(url)
        financial_data[key] = result if result else {}
    
    return render_template(
        "financestate.html",
        companynames=fin_company_name,
        finance_annual=financial_data['income_annual'],
        finance_quarter=financial_data['income_quarter'],
        balancesheetannual=financial_data['balance_annual'],
        balancesheetquarter=financial_data['balance_quarter'],
        cashflowannual=financial_data['cashflow_annual'],
        cashflowquarter=financial_data['cashflow_quarter']
    )

@app.route("/longterm/search")
def longterm_search():
    """Search page for long-term predictions"""
    try:
        companies = get_company_symbols()
        return render_template("longtermsearch.html", companies=companies)
    except Exception as e:
        logger.error(f"Error fetching company symbols: {e}")
        return render_template("longtermsearch.html", companies=[], error="Unable to fetch companies")

@app.route("/longterm/<longterm_name>/index")
def longterm_prediction(longterm_name):
    """Generate long-term stock predictions"""
    if not longterm_name:
        return render_template("longterm.html", error="Company symbol is required")
    
    try:
        # Fetch historical data
        api_url = f"{FINANCIAL_API_BASE}/historical-price-full/{longterm_name}"
        params = {'from': '2019-03-04', 'to': '2020-03-04'}
        historical_data = make_api_request(api_url, params)
        
        if not historical_data or 'historical' not in historical_data:
            return render_template("longterm.html", error="Unable to fetch historical data")
        
        # Process historical data
        dates = []
        prices = []
        for data_point in historical_data["historical"]:
            dates.append([int(data_point["date"].replace("-", ""))])
            prices.append(data_point["close"])
        
        if not dates or not prices:
            return render_template("longterm.html", error="No valid historical data found")
        
        # Generate predictions
        prediction_date = [[20200305]]  # Use constant date for prediction
        predictions = prediction_close(dates, prices, prediction_date)
        
        # Find best prediction
        actual_price = prices[-1]
        differences = [abs(pred - actual_price) for pred in predictions]
        best_prediction = predictions[differences.index(min(differences))]
        
        # Get company name and analysis
        company_name = get_company_by_symbol(longterm_name)
        if not company_name:
            company_name = longterm_name
        
        news_result = news_analysis(company_name)
        twitter_result = twitter_analysis(company_name)
        
        return render_template(
            "longterm.html",
            comnames=company_name,
            newsapi=news_result,
            twitterapi=twitter_result,
            sdates=dates,
            sprices=prices,
            alogsresult=predictions,
            confirmed=best_prediction,
        )
        
    except Exception as e:
        logger.error(f"Error in long-term prediction for {longterm_name}: {e}")
        return render_template("longterm.html", error="Prediction service temporarily unavailable")

@app.route("/intraday/search")
def intraday_search():
    """Search page for intraday predictions"""
    try:
        companies = get_company_symbols()
        return render_template("intradaysearch.html", companies=companies)
    except Exception as e:
        logger.error(f"Error fetching company symbols: {e}")
        return render_template("intradaysearch.html", companies=[], error="Unable to fetch companies")

@app.route("/intraday/<intra_comp>/index")
def intraday_prediction(intra_comp):
    """Generate intraday stock predictions"""
    if not intra_comp or not IEX_API_KEY:
        return render_template("intra.html", error="Invalid request or API key missing")
    
    try:
        # Fetch intraday data from IEX API
        api_url = f"https://cloud.iexapis.com/stable/stock/{intra_comp.lower()}/intraday-prices"
        params = {'token': IEX_API_KEY}
        intraday_data = make_api_request(api_url, params)
        
        if not intraday_data:
            return render_template("intra.html", error="Unable to fetch intraday data")
        
        # Process intraday data
        minute_list = []
        price_list = []
        
        for i, data_point in enumerate(intraday_data, 1):
            minute_list.append([i])
            # Handle null values
            open_price = data_point.get("open")
            if open_price is None and len(price_list) > 0:
                open_price = price_list[-1]  # Use previous price
            elif open_price is None:
                open_price = data_point.get("close", 0)  # Fallback to close price
            
            price_list.append(open_price)
        
        if len(minute_list) < 45:
            return render_template("intra.html", error="Insufficient data for prediction")
        
        # Generate predictions using first 45 minutes
        prediction_data = intrapred(minute_list[:45], price_list[:45], [[60]])
        test_prediction = intratestpred(minute_list, price_list, [[45]])
        
        # Get company name and analysis
        company_name = get_company_by_symbol(intra_comp.upper())
        if not company_name:
            company_name = intra_comp.upper()
        
        news_result = news_analysis(company_name)
        twitter_result = twitter_analysis(company_name)
        
        return render_template(
            "intra.html",
            companyname=company_name,
            newsapi=news_result,
            twitterapi=twitter_result,
            times=list(range(len(minute_list))),
            intratest=test_prediction,
            pricelist=price_list,
            predictions=prediction_data[0] if prediction_data else [],
            accuracy=prediction_data[1] if prediction_data and len(prediction_data) > 1 else 0,
        )
        
    except Exception as e:
        logger.error(f"Error in intraday prediction for {intra_comp}: {e}")
        return render_template("intra.html", error="Prediction service temporarily unavailable")

@app.route("/videos")
def videos():
    """Video content page"""
    return render_template("videos.html")

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    logger.error(f"Internal server error: {error}")
    return render_template("500.html"), 500

if __name__ == "__main__":
    # Check required environment variables
    required_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        print("Please set the following environment variables:")
        for var in missing_vars:
            print(f"  export {var}=your_value")
    else:
        app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
