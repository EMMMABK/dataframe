import pandas as pd 
import requests 
import time 
import psycopg2
# DataBase and password can be changable
conn = psycopg2.connect( 
    host="localhost", 
    database="dateformater", 
    user="postgres", 
    password="qwerty" 
) 

cur = conn.cursor() 
 
cur.execute(""" 
CREATE TABLE crypto_prices ( 
    name varchar(255), 
    date date, 
    open_price decimal, 
    high_price decimal, 
    low_price decimal, 
    close_price decimal 
); 
""") 

conn.commit() 

def crypto_price(crypto_name): 
    # Use the CoinGecko API to retrieve data for the given cryptocurrency 
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_name}/market_chart?vs_currency=usd&days=1&interval=1d" 
    response = requests.get(url) 
    data = response.json() 
     
    # Extract the relevant information from the response 
    dates = [pd.to_datetime(d, unit='ms').strftime("%Y-%m-%d") for d in data["prices"][0]] 
    open_price = data["prices"][1][1] 
    high_price = max(data["prices"], key=lambda x: x[1])[1] 
    low_price = min(data["prices"], key=lambda x: x[1])[1] 
    close_price = data["prices"][-1][1] 
    date = dates[0] 
    
    
    # Insert of dataframe to databas
    
    cur.execute("""
        INSERT INTO crypto_prices VALUES (%s,%s,%s,%s,%s,%s)
    """, (crypto_name, date, open_price, high_price, low_price, close_price))
    
    conn.commit()
    
    # Create a Pandas DataFrame with the information 
    df = pd.DataFrame({ 
        "Symbol": [crypto_name], 
        "Date": [date], 
        "Open": [open_price], 
        "High": [high_price], 
        "Low": [low_price], 
        "Close": [close_price] 
    }) 
     
    return df 

# Ask the user for the name of the cryptocurrency 
crypto_name = input("Enter the name of the cryptocurrency: ") 
 
# Get the price information for the cryptocurrency 
price_data = crypto_price(crypto_name) 


 
# Print the price information 
print(price_data) 
 
# Wait for 1 day if it's need IMPORTANT 
time.sleep(86400) 
 
# Get the price information for the cryptocurrency again 
price_data = crypto_price(crypto_name) 


# Print the updated price information 
print(price_data)   
cur.close() 
conn.close()
