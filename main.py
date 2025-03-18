from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Set up Chrome options
options = Options()
options.add_argument("--headless")  # Run in headless mode (no UI)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Nike US Running Shoes URL
url = "https://www.nike.com/w/mens-running-shoes-37v7jznik1zy7ok"

# Load the webpage
driver.get(url)
time.sleep(5)  # Wait for page to load fully

# Scroll down to load more products (if needed)
for _ in range(3):  
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    time.sleep(3)

# Extract product details
models = []
prices = []

products = driver.find_elements(By.CLASS_NAME, "product-card")

for product in products:
    try:
        model = product.find_element(By.CLASS_NAME, "product-card__title").text
        price = product.find_element(By.CLASS_NAME, "product-price").text
        models.append(model)
        prices.append(price)
    except:
        continue  # Skip if any data is missing

# Close the browser
driver.quit()

# Save to CSV
df = pd.DataFrame({"Product Name": models, "Product Price": prices})
df.to_csv("nike_us_shoes.csv", encoding="utf-8", index=False)

print("Scraping complete Data saved to nike_us_shoes.csv.")
