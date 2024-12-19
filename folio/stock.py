import requests
import pandas as pd

# Define the Alpha Vantage API URL and your API key
API_KEY = 'your_alpha_vantage_api_key'  # Replace with your actual API key
BASE_URL = 'https://www.alphavantage.co/query'

# Function to fetch the current stock price from Alpha Vantage
def get_stock_price(symbol):
    url = f"{BASE_URL}?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    # Check if the response is valid and contains data
    if "Time Series (5min)" in data:
        latest_time = list(data["Time Series (5min)"].keys())[0]
        latest_data = data["Time Series (5min)"][latest_time]
        return float(latest_data["4. close"])  # Returning the latest closing price
    else:
        print(f"Error fetching data for {symbol}. Response: {data}")
        return None

# Class to manage the stock portfolio
class StockPortfolio:
    def __init__(self):
        self.portfolio = pd.DataFrame(columns=["Symbol", "Shares", "Purchase Price"])
    
    # Add a stock to the portfolio
    def add_stock(self, symbol, shares, purchase_price):
        self.portfolio = self.portfolio.append({
            "Symbol": symbol,
            "Shares": shares,
            "Purchase Price": purchase_price
        }, ignore_index=True)
        print(f"Added {shares} shares of {symbol} at ${purchase_price} each.")
    
    # Remove a stock from the portfolio
    def remove_stock(self, symbol):
        self.portfolio = self.portfolio[self.portfolio["Symbol"] != symbol]
        print(f"Removed all shares of {symbol}.")
    
    # Get the current value of the portfolio
    def get_portfolio_value(self):
        total_value = 0
        for _, row in self.portfolio.iterrows():
            current_price = get_stock_price(row["Symbol"])
            if current_price:
                total_value += current_price * row["Shares"]
        return total_value
    
    # Get the profit/loss for the portfolio
    def get_profit_loss(self):
        total_profit_loss = 0
        for _, row in self.portfolio.iterrows():
            current_price = get_stock_price(row["Symbol"])
            if current_price:
                total_profit_loss += (current_price - row["Purchase Price"]) * row["Shares"]
        return total_profit_loss
    
    # Display the portfolio
    def display_portfolio(self):
        print("\nPortfolio Summary:")
        print(self.portfolio)
        total_value = self.get_portfolio_value()
        total_profit_loss = self.get_profit_loss()
        print(f"\nTotal Portfolio Value: ${total_value:.2f}")
        print(f"Total Profit/Loss: ${total_profit_loss:.2f}")

# Main function to interact with the user
def main():
    portfolio = StockPortfolio()
    
    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio")
        print("4. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            symbol = input("Enter stock symbol (e.g., AAPL): ").upper()
            shares = int(input("Enter number of shares: "))
            purchase_price = float(input("Enter purchase price per share: $"))
            portfolio.add_stock(symbol, shares, purchase_price)
        
        elif choice == '2':
            symbol = input("Enter stock symbol to remove: ").upper()
            portfolio.remove_stock(symbol)
        
        elif choice == '3':
            portfolio.display_portfolio()
        
        elif choice == '4':
            print("Exiting the portfolio tracker.")
            break
        
        else:
            print("Invalid choice, please try again.")

# Run the program
if __name__ == "__main__":
    main()
