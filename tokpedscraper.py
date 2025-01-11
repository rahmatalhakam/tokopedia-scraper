from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
from datetime import datetime
import json
from requests.exceptions import Timeout, SSLError
import urllib3


def parse_tokopedia_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*'
    }

    max_retries = 2
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=30, verify=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            products = []
            shop_name = get_shop_name(url)
            
            # Find all product containers
            product_containers = soup.find_all('div', class_='css-1sn1xa2')
            
            for container in product_containers:
                try:
                    # Extract product name
                    name = container.find('div', {'class': 'prd_link-product-name'}).text.strip()
                    
                    # Extract price and convert to number
                    price_text = container.find('div', {'class': 'prd_link-product-price'}).text.strip()
                    price = int(re.sub(r'[^\d]', '', price_text))
                    
                    # Extract rating
                    rating_elem = container.find('span', {'class': 'prd_rating-average-text'})
                    rating = float(rating_elem.text.strip()) if rating_elem else None
                    
                    # Extract sales count
                    sales_elem = container.find('span', {'class': 'prd_label-integrity'})
                    sales_text = sales_elem.text.strip() if sales_elem else "0"
                    sales = re.sub(r'[^\d+]', '', sales_text)
                    sales = int(sales.replace('+', '')) if sales else 0
                    
                    # Extract product URL
                    url_elem = container.find('a', {'class': 'pcv3__info-content'})
                    url = url_elem['href'] if url_elem else None
                    
                    # Extract image URL
                    img_elem = container.find('img', {'class': 'css-1q90pod'})
                    image_url = img_elem['src'] if img_elem else None
                    
                    product = {
                        'shop': shop_name,
                        'name': name,
                        'price': price,
                        'rating': rating,
                        'sales': sales,
                        'url': url,
                        'image_url': image_url
                    }
                    
                    products.append(product)
                    
                except Exception as e:
                    print(f"Error processing product: {e}")
                    continue

            return products
        except SSLError as e:
            print(f"Error connecting to Tokopedia (attempt {attempt}/{max_retries}): {e}")
            continue  # Retry on SSL error
        except Timeout as e:
            print(f"Request timed out (attempt {attempt}/{max_retries}): {e}")
            continue  # Retry on timeout
    print("Failed to retrieve data after", max_retries, "attempts.")
    return []

def save_to_formats(df_list, base_filename):
    
    """Save the data to multiple formats"""
    # Save to CSV
    df_list.to_csv(f'{base_filename}.csv', index=False)
    
    # df.to_excel(f'{base_filename}.xlsx', index=False)
    # df.to_json(f'{base_filename}.json', orient='records', indent=2)
    
    return True


def get_file_name(keyword):
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H.%M.%S")
    return 'tokopedia_products '+ keyword + ' ' + formatted_time

def get_shop_name(url):
    parts = url.split('/')
    shop_part = parts[3]
    shop_name = shop_part.split('?')[0]
    return shop_name

def check_tokopedia_url(shop_url, query):
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            # Send GET request to the URL
            response = requests.get(shop_url, headers=headers, timeout=10, verify=False)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # Get the HTML content
            html_content = response.text
            
            # Count occurrences of "Beranda"
            occurrences = html_content.count("Beranda")
            
            # Determine which URL to use
            final_url = shop_url + query if occurrences <= 0 else shop_url + "/product" + query
            
            return {
                'final_url': final_url,
                'occurrences': occurrences,
                'status': 'success'
            }
        except SSLError as e:
            print(f"Error connecting to Tokopedia (attempt {attempt}/{max_retries}): {e}")
            continue  # Retry on SSL error
        except Timeout as e:
            print(f"Request timed out (attempt {attempt}/{max_retries}): {e}")
            if(attempt == max_retries):
                return {
                    'final_url': shop_url +"/product" + query,
                    'occurrences': 0,
                    'status': 'error',
                    'error': str(e)
                }
            else:
                continue  # Retry on timeout
        except requests.RequestException as e:
            return {
                'final_url': shop_url +"/product" + query,
                'occurrences': 0,
                'status': 'error',
                'error': str(e)
            }

def get_urls_from_csv(csv_file='tokopedia_shops.csv'):
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file)
        
        # Extract URLs into a list
        urls = df['url'].tolist()
        
        # Remove any None or NaN values
        urls = [url for url in urls if pd.notna(url)]
        
        print(f"Successfully extracted {len(urls)} URLs")
        
        # Print all URLs
        print("\nExtracted URLs:")
        for i, url in enumerate(urls, 1):
            print(f"{i}. {url}")
            
        return urls
        
    except FileNotFoundError:
        print(f"Error: The file {csv_file} was not found")
        return []
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        return []

def get_keyword_from_json(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            return data.get('keyword')
    except FileNotFoundError:
        print(f"Error: File {json_file_path} not found")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")
        return None

if __name__ == "__main__":

    urllib3.disable_warnings()
    keyword  = get_keyword_from_json("config.json")
    shop_urls = get_urls_from_csv()
    query = "?q="+keyword+"&sort=9"
    df_list = []

    print(">>>>>> KEYWORD: " + keyword)

    for shop_url in shop_urls:
        res = check_tokopedia_url(shop_url, query)
        url = res['final_url']
        print(">>>>>> URL: "+url + ". Status: " +res['status'])
        
        products = parse_tokopedia_html(url)
        df_list.extend(products)
    
    file_name = get_file_name(keyword)
    df_list = pd.DataFrame(df_list).sort_values(by="price")
    save_to_formats(df_list, file_name)
    
    # Print some statistics
    if df_list.empty:
        print("DataFrame is empty.")
    elif df_list.isnull().values.any():
        print(f"\nTotal products found: {len(df_list)}")
        print(f"Average price: Rp{df_list['price'].mean():,.2f}")
        print(f"Price range: Rp{df_list['price'].min():,} - Rp{df_list['price'].max():,}")
        print(f"Total sales: {df_list['sales'].sum()}")
        print(f"Average rating: {df_list['rating'].mean():.2f}")