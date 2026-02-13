import requests
from bs4 import BeautifulSoup
import json
import time

url = "https://www.daraz.com.np/#hp-flash-sale"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

products = []

try:

    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        print("Successfully accessed Daraz")
    else:
        print(f"Failed to access website. Status code: {response.status_code}")
    
  
    soup = BeautifulSoup(response.text, 'html.parser')
    

    product_containers = soup.find_all('div', class_='fs-card-text')
    
    print(f"Found {len(product_containers)} product containers\n")
    
    for container in product_containers:
        try:

            title_elem = container.find('p', class_='fs-card-title')
            if title_elem:
                title = title_elem.get_text(strip=True)
            else:
                title = "N/A"
            

            price_elem = container.find('span', class_='price')
            if price_elem:
                price = price_elem.get_text(strip=True)
            else:
                price = "N/A"
            

            if title != "N/A" and price != "N/A":
                product = {
                    'title': title,
                    'price': price
                }
                products.append(product)
                print(f"  {title}")
                print(f"  Price: {price}\n")
        
        except Exception as e:
            print(f"Error extracting product: {e}")
            continue
    
    with open('products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    
    print(f"\n Saved {len(products)} products to products.json")
    
 
    time.sleep(2)

except requests.Timeout:
    print("The request timed out")
except Exception as e:
    print(f"An error occurred: {e}")