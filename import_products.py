import pymysql.cursors
import json
import os


def sql_insert(data, output_file):
    with open(output_file, 'w') as f:
        f.write("INSERT INTO petshop (product_url, product_name, barcode, product_price, product_stock, product_images, description, sku, category, product_id, brand)\n")
        f.write("VALUES\n")

        for i, item in enumerate(data):
            sku = item.get('sku', 'N/A')
            values = (
                f"('{item.get('product_url', '')}', "
                f"'{item['product_name']}', "
                f"'{item.get('barcode', '')}', "
                f"{item['product_price']}, "
                f"'{item['product_stock']}', "
                f"'{', '.join(item['product_images']) if 'product_images' in item else ''}', "
                f"'{item['description']}', "
                f"'{sku}', "
                f"'{item['category']}', "
                f"{item['product_id']}, "
                f"'{item['brand']}')"
            )
            if i < len(data) - 1:
                values += ","
            f.write(values + "\n")

        f.write(";\n")


def generate_sql_file():
    json_file_path = os.path.abspath('../petshop_products.json')
    sql_file_path = os.path.abspath('../petshop_insert.sql')

    if not os.path.exists(json_file_path):
        print(f"Error: JSON file '{json_file_path}' not found.")
        return

    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        try:
            data = json.load(json_file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return

    sql_insert(data, sql_file_path)


def insert_data(connection, data):
    try:
        with connection.cursor() as cursor:
            for item in data:
                sku = item.get('sku', 'N/A')
                insert_sql = """
                    INSERT INTO petshop (
                        product_url, product_name, barcode, product_price, 
                        product_stock, product_images, description, sku, 
                        category, product_id, brand
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        product_url = VALUES(product_url),
                        product_name = VALUES(product_name),
                        barcode = VALUES(barcode),
                        product_price = VALUES(product_price),
                        product_stock = VALUES(product_stock),
                        product_images = VALUES(product_images),
                        description = VALUES(description),
                        category = VALUES(category),
                        product_id = VALUES(product_id),
                        brand = VALUES(brand)
                """
                cursor.execute(insert_sql, (
                    item['product_url'],
                    item['product_name'],
                    item.get('barcode', 'N/A'),
                    item['product_price'],
                    item['product_stock'],
                    ', '.join(item['product_images']),
                    item['description'],
                    item.get('sku', 'N/A'),
                    item['category'],
                    item['product_id'],
                    item['brand']
                ))

            # commit changes
            connection.commit()

    except Exception as e:
        print(f"Error inserting data: {e}")


def main():
    json_file_path = os.path.abspath('../petshop_products.json')

    if not os.path.exists(json_file_path):
        print(f"Error: JSON file '{json_file_path}' not found.")
        return

    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        try:
            data = json.load(json_file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return

    # connect to mysql database
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='your_sql_password_here',
        database='petshop',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        insert_data(connection, data)

    finally:
        connection.close()


if __name__ == "__main__":
    main()

    generate_sql_file()