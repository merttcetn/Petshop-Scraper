# PetShop Web Scraping Project 🐾

## Overview

This project demonstrates web scraping using Scrapy and importing the scraped data into a MySQL database. The aim is to extract product information from a fictional pet shop website and save the data in both JSON format and a MySQL database.

Project was developed for a case study. Hence, the actual pet shop website name has been concealed for privacy reasons. It's important to note that this project is purely educational and does not have any commercial intentions.

## Files Included

1. **petshop_scrapy.py**: A Python script using Scrapy to scrape product information from the pet shop website and save it as a JSON file.
2. **import_products.py**: A Python script to import the JSON data into a MySQL database.
3. **petshop_create.sql**: SQL script to create the `petshop` table in the MySQL database.

## How to Run

### Prerequisites

- Python 3.x
- Scrapy
- MySQL
- MySQL Connector for Python

### Instructions

1. **Clone the Repository**

   ```sh
   git clone <repository_url>
   cd <repository_folder>
   ```

2. **Set Up the Environment**

   Install the required Python packages:

   ```sh
   pip install scrapy mysql-connector-python
   ```

3. **Update the Scrapy Script**

   In `petshop_scrapy.py`, update the target URL to point to the actual pet shop website you intend to scrape. Replace the placeholder with the appropriate URL.

   ```python
   start_urls = ['https://www.examplepetshop.com']  # Change to the actual URL
   ```

4. **Run the Scrapy Script**

   Execute the Scrapy script to scrape data and save it as `petshop_products.json`:

   ```sh
   scrapy runspider petshop_scrapy.py -o petshop_products.json
   ```

5. **Create the MySQL Table**

   Run the `petshop_create.sql` script to create the `petshop` table in your MySQL database:

   ```sh
   mysql -u your_username -p your_database < petshop_create.sql
   ```

6. **Import JSON Data to MySQL**

   Execute the import script to load data from `petshop_products.json` into the `petshop` table:

   ```sh
   python import_products.py
   ```

## Explanation

The project originally targeted a specific website, and the name has been generalized to "petshop" for privacy and confidentiality reasons. Ensure you replace the placeholder URL in `petshop_scrapy.py` with the actual URL of the website you wish to scrape.

By following these steps, you can successfully scrape product data from a pet shop website and import it into a MySQL database, demonstrating your proficiency in web scraping and database management.

## Notes

- Ensure you have the necessary permissions to scrape data from the target website.
- Modify the database connection details in `import_products.py` to match your MySQL setup.
- Handle any legal or ethical considerations regarding web scraping for your specific use case.