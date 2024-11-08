# User class to manage login and roles
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role
    
    def authenticate(self, password):
        return self.password == password
    
# Product class to represent each product in the inventory
class Product:
    def __init__(self, product_id, name, category, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity
    
    def update_stock(self, quantity):
        self.stock_quantity += quantity
    
    def __str__(self):
        return f"{self.product_id}: {self.name} | Category: {self.category} | Price: ${self.price} | Stock: {self.stock_quantity}"
    
# Inventory class to manage the collection of products
class Inventory:
    def __init__(self):
        self.products = {}
        self.low_stock_threshold = 5
    
    def add_product(self, product):
        if product.product_id in self.products:
            print("Error: Product ID already exists.")
        else:
            self.products[product.product_id] = product
            print("Product added successfully.")
    
    def edit_product(self, product_id, **kwargs):
        # print('here 123')
        product = self.products.get(product_id)
        if not product:
            print("Error: Product not found.")
            return
        
        for key, value in kwargs.items():
            setattr(product, key, value)
        print("Product updated successfully.")

    def delete_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
            print("Product deleted successfully.")
        else:
            print("Error: Product not found.")

    def view_products(self):
        if not self.products:
            print("No Product in Inventory.")
        for product in self.products.values():
            print(product)
            if product.stock_quantity < self.low_stock_threshold:
                print(f"Warning: {product.name} stock is low!")
    
    def search_product(self, name=None, category=None):
        results = []
        for product in self.products.values():
            if name and name.lower() in product.name.lower():
                results.append(product)
            elif category and category.lower() == product.category.lower():
                results.append(product)
        
        if results:
            for product in results:
                print(product)
        else:
            print("No Products found.")
    
    def adjust_stock(self, product_id, quantity):
        product = self.products.get(product_id)
        if not product:
            print("Error: Product not found.")
            return
        
        product.update_stock(quantity)
        print("Stock updated successfully.")

class InventorySystem:
    def __init__(self):
        self.inventory = Inventory()
        self.users = {
            "admin": User("admin", "admin123", "Admin"),
            "user": User("user", "user123", "User")
        }
        self.current_user = None
        
    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        user = self.users.get(username)
        
        if user and user.authenticate(password):
            self.current_user = user
            print(f"Welcome, {user.username} ({user.role})!")
            return True
        else:
            print("Invalid login.")
            return False
    
    def run(self):
        if not self.login():
            return
        
        while True:
            if self.current_user.role == "Admin":
                print("\nOptions: 1. Add Product 2. Edit Product 3. Delete Product 4. View Products 5. Adjust Stock 6. Search Product 7. Logout")
            else:
                print("\nOptions: 1. View Products 2. Search Product 3. Logout")
            
            choice = input("Enter your choice: ")
            
            if choice == "1":
                if self.current_user.role == "Admin":
                    self.add_product()
                else:
                    self.inventory.view_products()
            
            elif choice == "2":
                if self.current_user.role == "Admin":
                    self.edit_product()
                else:
                    self.search_product()
            
            elif choice == "3":
                if self.current_user.role == "Admin":
                    self.delete_product()
                else:
                    # Logout
                    break 
                
            elif choice == "4" and self.current_user.role == "Admin":
                self.inventory.view_products()
            
            elif choice == "5" and self.current_user.role == "Admin":
                self.adjust_stock()
                
            elif choice == "6" and self.current_user.role == "Admin":
                self.search_product()
            
            elif choice == "7" and self.current_user.role == "Admin":
                break # Logout for Admin
            
            else:
                print("Invalid choice, please try again.")
    
    def add_product(self):
        product_id = input("Enter product ID: ")
        name = input("Enter product name: ")
        category = input("Enter product category: ")
        price = float(input("Enter product price: "))
        stock_quantity = int(input("Enter stock quantity: "))
        
        product = Product(product_id, name, category, price, stock_quantity)
        self.inventory.add_product(product)
    
    def edit_product(self):
        product_id = input("Enter product ID to edit: ")
        name = input("Enter new name (leave blank to skip): ")
        category = input("Enter new category (leave blank to skip): ")
        price = input("Enter new price (leave blank to skip): ")
        stock_quantity = input("Enter new stock quantity (leave blank to skip): ")
        
        kwargs = {}
        if name:
            kwargs["name"] = name
        if category:
            kwargs["category"] = category
        if price:
            kwargs["price"] = float(price)
        if stock_quantity:
            kwargs["stock_quantity"] = int(stock_quantity)
        # print(kwargs)
        self.inventory.edit_product(product_id, **kwargs)
    
    def delete_product(self):
        product_id = input("Enter product ID to delete: ")
        self.inventory.delete_product(product_id)
    
    def adjust_stock(self):
        product_id = input("Enter product ID to adjust stock: ")
        quantity = int(input("Enter quantity to adjust (positive to restock, negative to reduce): "))
        self.inventory.adjust_stock(product_id, quantity)
    
    def search_product(self):
        name = input("Enter product name to search (leave blank for category search): ")
        category = input("Enter product category to search (leave blank for name search): ")
        self.inventory.search_product(name=name, category=category)

if __name__ == "__main__":
    system = InventorySystem()
    system.run()

        

