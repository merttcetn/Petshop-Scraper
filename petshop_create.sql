CREATE DEFINER=`root`@`localhost` PROCEDURE `petshop_create`()
BEGIN
    CREATE TABLE IF NOT EXISTS petshop (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_url VARCHAR(255),
        product_name VARCHAR(255),
        barcode VARCHAR(50),
        product_price DECIMAL(10, 2),
        product_stock VARCHAR(50),
        product_images TEXT,
        description TEXT,
        sku VARCHAR(50),
        category VARCHAR(100),
        product_id INT,
        brand VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
END
