import mysql.connector

# Establish the database connection
db = mysql.connector.connect(
    host="localhost",
    user="komal",
    password="09etecs002",
    database="mysql"
)
cursor = db.cursor()

# Create tables in the database (run only once)
def create_tables():
    # Create the categories table
    cursor.execute("CREATE TABLE IF NOT EXISTS categories (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")

    # Create the products table
    cursor.execute("CREATE TABLE IF NOT EXISTS products (id INT AUTO_INCREMENT PRIMARY KEY, category_id INT, name VARCHAR(255), price INT)")
    cursor.execute("ALTER TABLE products ADD FOREIGN KEY (category_id) REFERENCES categories(id)")

    # Create the cart table
    cursor.execute("CREATE TABLE IF NOT EXISTS cart (id INT AUTO_INCREMENT PRIMARY KEY, user_name VARCHAR(255), product_id INT)")
    cursor.execute("ALTER TABLE cart ADD FOREIGN KEY (product_id) REFERENCES products(id)")

class Category:
    def __init__(self, name):
        self.name = name

class Product:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, product):
        self.items.append(product)

    def remove_item(self, product):
        self.items.remove(product)

    def calculate_total(self):
        total = sum(product.price for product in self.items)
        return total
    def checkout(self):
        self.items = []  # Empty the cart
        print("Thank you for your purchase! Your order has been successfully placed.")


class User:
    def __init__(self):
        self.cart = Cart()

    def view_categories(self):
        query = "SELECT name FROM categories"
        cursor.execute(query)
        categories = cursor.fetchall()
        print("Categories:")
        for category in categories:
            print(category[0])

    def view_products(self, category_name):
        query = "SELECT products.name, products.price FROM products " \
                "JOIN categories ON products.category_id = categories.id " \
                "WHERE categories.name = %s"
        cursor.execute(query, (category_name,))
        products = cursor.fetchall()
        if products:
            print(f"Products in {category_name}:")
            for product in products:
                print(f"- {product[0]}: Rs {product[1]}")
        else:
            print(f"Category '{category_name}' not found.")

    def view_product_details(self, product_name):
        query = "SELECT products.name, products.price FROM products " \
                "WHERE products.name = %s"
        cursor.execute(query, (product_name,))
        product = cursor.fetchone()
        if product:
            print(f"Product Details:")
            print(f"Name: {product[0]}")
            print(f"Price: Rs {product[1]}")
        else:
            print(f"Product '{product_name}' not found.")

    def add_to_cart(self, product_name):
        query = "SELECT products.name, products.price FROM products " \
                "WHERE products.name = %s"
        cursor.execute(query, (product_name,))
        product = cursor.fetchone()
        if product:
            self.cart.add_item(Product(product[0], product[1], None))
            print(f"{product[0]} added to cart.")
        else:
            print(f"Product '{product_name}' not found.")

    def remove_from_cart(self, product_name):
        query = "SELECT products.name, products.price FROM products " \
                "WHERE products.name = %s"
        cursor.execute(query, (product_name,))
        product = cursor.fetchone()
        if product:
            self.cart.remove_item(Product(product[0], product[1], None))
            print(f"{product[0]} removed from cart.")
        else:
            print(f"Product '{product_name}' not found.")

    def checkout(self):
        total = self.cart.calculate_total()
        if total > 10000:
            discount = 500
            final_amount = total - discount
        else:
            discount = 0
            final_amount = total

        print("Checkout Summary:")
        print(f"Total amount: Rs {total}")
        print(f"Discount: Rs {discount}")
        print(f"Final amount: Rs {final_amount}")

class Admin:
    def add_category(self, name):
        query = "INSERT INTO categories (name) VALUES (%s)"
        cursor.execute(query, (name,))
        db.commit()
        print(f"{name} category added.")
     
    def add_product(self, category_name, product_name, price, cursor):
        # Use a separate cursor for executing the SELECT query
        select_cursor = db.cursor(buffered=True)
        query = "SELECT id FROM categories WHERE name = %s"
        select_cursor.execute(query, (category_name,))

        category_id = None
        if select_cursor.rowcount > 0:
            category_id = select_cursor.fetchone()[0]

        if category_id:
            # Use a separate cursor for executing the INSERT query
            insert_cursor = db.cursor()
            insert_query = "INSERT INTO products (category_id, name, price) VALUES (%s, %s, %s)"
            insert_cursor.execute(insert_query, (category_id, product_name, price))
            db.commit()
            insert_cursor.close()  # Close the INSERT cursor

            print(f"Product '{product_name}' added to category '{category_name}'.")
        else:
            print(f"Category '{category_name}' not found.")

        select_cursor.close()  # Close the SELECT cursor


    

# Create tables in the database (run only once)
#create_tables()

# Sample Usage
class User:
    def __init__(self, name):
        self.name = name
        self.cart = Cart()

    def view_categories(self):
        query = "SELECT * FROM categories"
        cursor.execute(query)
        categories = cursor.fetchall()
        print("\nCategories:")
        for category in categories:
            print(f"- {category[1]}")
    def add_to_cart(self, product_name):
        query = "SELECT id FROM products WHERE name = %s"
        cursor.execute(query, (product_name,))
        product_id = cursor.fetchone()
        if product_id:
            query = "INSERT INTO carts (user_id, product_id) VALUES (%s, %s)"
            cursor.execute(query, (self.name, product_id[0]))
            db.commit()
            print(f"{product_name} added to cart.")
        else:
            print(f"Product '{product_name}' not found.")

    def show_menu(self):
        print("Welcome to MyCart Shopping Assistant!")
        
        while True:
            print("\nPlease choose an option:")
            print("1. View Categories")
            print("2. View Products in a Category")
            print("3. View Product Details")
            print("4. Add Product to Cart")
            print("5. View Cart")
            print("6. Remove Product from Cart")
            print("7. Checkout")
            print("8. Exit")

            choice = input("Enter your choice (1-8): ")

            if choice == "1":
                self.view_categories()
            elif choice == "2":
                category_name = input("Enter the category name: ")
                self.view_products(category_name)
            elif choice == "3":
                product_name = input("Enter the product name: ")
                self.view_product_details(product_name)
            elif choice == "4":
                product_name = input("Enter the product name: ")
                self.add_to_cart(product_name)
            elif choice == "5":
                self.view_cart()
            elif choice == "6":
                product_name = input("Enter the product name: ")
                self.remove_from_cart(product_name)
            elif choice == "7":
                self.cart.checkout()

            elif choice == "8":
                print("Thank you for shopping with MyCart!")
                break
            else:
                print("Invalid choice. Please try again.")
    def view_products(self, category_name):
        # Use a separate cursor for executing the SELECT query
        cursor = db.cursor(buffered=True)
        query = """
            SELECT p.name, p.price
            FROM products p
            JOIN categories c ON p.category_id = c.id
            WHERE c.name = %s
        """
        cursor.execute(query, (category_name,))

        if cursor.rowcount > 0:
            print(f"Products under '{category_name}':")
            for product in cursor.fetchall():
                print(f"Product: {product[0]} - Price: {product[1]}")
        else:
            print(f"No products found under '{category_name}'.")

        cursor.close()  # Close the cursor
    
    def view_product_details(self, product_name):
        # Use a separate cursor for executing the SELECT query
        cursor = db.cursor(buffered=True)
        query = """
            SELECT p.name, p.price, c.name AS category
            FROM products p
            JOIN categories c ON p.category_id = c.id
            WHERE p.name = %s
        """
        cursor.execute(query, (product_name,))

        if cursor.rowcount > 0:
            product = cursor.fetchone()
            print(f"Product: {product[0]}")
            print(f"Price: {product[1]}")
            print(f"Category: {product[2]}")
        else:
            print(f"Product '{product_name}' not found.")

        cursor.close() 
    def add_to_cart(self, product_name):
        # Use a separate cursor for executing the SELECT and INSERT queries
        cursor = db.cursor(buffered=True)

        # Get the product ID
        select_query = "SELECT id FROM products WHERE name = %s"
        cursor.execute(select_query, (product_name,))
        product_id = cursor.fetchone()

        # Insert the product into the cart
        insert_query = "INSERT INTO cart (user_name, product_id) VALUES (%s, %s)"
        cursor.execute(insert_query, (self.name, product_id[0]))

        db.commit()  # Commit the changes

        cursor.close()  # Close the cursor
    
    def view_cart(self):
        select_query = "SELECT p.name, p.price FROM products p JOIN cart c ON p.id = c.product_id WHERE c.user_name = %s"
        cursor.execute(select_query, (self.name,))
        products = cursor.fetchall()

        if not products:
            print("Your cart is empty.")
        else:
            print("Your cart:")
            total_amount = 0
            for product in products:
                product_name, product_price = product
                print(f"{product_name} - Rs {product_price}")
                total_amount += product_price

            print(f"Total amount: Rs {total_amount}")

    
    def remove_from_cart(self, product_name):
        select_query = "SELECT id FROM products WHERE name = %s"
        cursor.execute(select_query, (product_name,))
        product_id = cursor.fetchone()

        if not product_id:
            print("Product not found.")
            return

        cursor.fetchall()  # Consume any unread result

        delete_query = "DELETE FROM cart WHERE user_name = %s AND product_id = %s"
        try:
            cursor.execute(delete_query, (self.name, product_id[0]))
            db.commit()
            print(f"{product_name} removed from your cart.")
        except mysql.connector.Error as error:
            print(f"An error occurred: {error}")
    
   

    def checkout(self):
     if not self.cart:
        print("Your cart is empty. Please add items before checking out.")
     else:
        # Process the checkout logic here
        # ...

        # Empty the cart
        self.cart.clear()

        print("Thank you for your purchase! Your order has been successfully placed.")
admin = Admin()
admin.add_category("Electronics")
admin.add_product("Electronics", "Smartphone", 15000, cursor)

user_name = input("Enter your name: ")
user = User(user_name)
user.show_menu()
