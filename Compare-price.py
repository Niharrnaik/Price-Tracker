import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to get Flipkart price
def get_flipkart_price(product_name):
    driver.get("https://www.flipkart.com/")
    try:
        # Close the login popup if it appears
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '✕')]"))
        ).click()
    except Exception:
        pass  # Ignore if pop-up doesn't appear

    # Search for the product
    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@name='q']"))
    )
    search_bar.send_keys(product_name)
    search_bar.send_keys(Keys.ENTER)

    try:
        # Extract product name and price
        name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@class='_4rR01T']"))
        ).text
        price = driver.find_element(By.XPATH, "//*[@class='_30jeq3 _1_WHN1']").text
        price = int(price.replace("₹", "").replace(",", ""))
    except Exception as e:
        print(f"Error on Flipkart: {e}")
        return None, float('inf')

    return name, price

# Function to get Amazon price
def get_amazon_price(product_name):
    driver.get("https://www.amazon.in/")
    # Search for the product
    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='twotabsearchtextbox']"))
    )
    search_bar.send_keys(product_name)
    search_bar.send_keys(Keys.ENTER)

    try:
        # Extract product name and price
        name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']"))
        ).text
        price_whole = driver.find_element(By.XPATH, "//span[@class='a-price-whole']").text
        try:
            price_fraction = driver.find_element(By.XPATH, "//span[@class='a-price-fraction']").text
            price = float(f"{price_whole}.{price_fraction}")
        except:
            price = int(price_whole.replace(",", ""))
    except Exception as e:
        print(f"Error on Amazon: {e}")
        return None, float('inf')

    return name, price

# Function to compare prices
def get_lowest_price(product_name):
    flipkart_name, flipkart_price = get_flipkart_price(product_name)
    amazon_name, amazon_price = get_amazon_price(product_name)

    results = [
        {"platform": "Flipkart", "name": flipkart_name, "price": flipkart_price},
        {"platform": "Amazon", "name": amazon_name, "price": amazon_price},
    ]

    # Get the lowest-priced product
    lowest = min(results, key=lambda x: x["price"])
    return results, lowest

# Initialize WebDriver
driver = webdriver.Chrome()
try:
    # Products to compare
    products = ["iPhone 14", "MacBook Pro"]
    all_results = []

    # Process each product and gather results
    for product in products:
        results, lowest = get_lowest_price(product)
        all_results.extend(results)

        # Display prices from both websites
        print(f"Prices for '{product}':")
        for result in results:
            print(f"  {result['platform']}: ₹{result['price']} ({result['name']})")
        
        # Display the lowest price
        print(f"The lowest-priced product for '{product}' is '{lowest['name']}' on {lowest['platform']} at ₹{lowest['price']}.")
        print()

    # Write all results to a CSV file
    with open("price_comparison.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["platform", "name", "price"])
        writer.writeheader()
        writer.writerows(all_results)

    # Load results into a Pandas DataFrame for display
    df = pd.DataFrame(all_results)

    # Display the DataFrame in Jupyter Notebook
    display(df)

finally:
    driver.quit()
