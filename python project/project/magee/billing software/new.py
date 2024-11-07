import datetime
import os

class BillSystem:
    def __init__(self):
        self.items = {}  # Store item name and its price
        self.cart = {}  # Store the items in the cart with quantities
        self.tax_rate = 0.1  # 10% tax
        self.discount_rate = 0  # No discount by default
        self.past_invoices = []  # Keep track of past invoices for customers
        self.categories = {}  # Store categories for items
        self.promotions = {}  # Store promotions for items

    def add_item(self, name, price, category="General", description=""):
        """Add item to the bill system."""
        self.items[name] = {"price": price, "category": category, "description": description}
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(name)
    
    def add_promotion(self, item_name, discount_type="percentage", discount_value=0):
        """Add promotion to an item (fixed or percentage)."""
        self.promotions[item_name] = {"type": discount_type, "value": discount_value}

    def view_items(self):
        """Display all available items with numbers to choose from."""
        if not self.items:
            print("No items available.")
        else:
            print("\nAvailable Items:")
            for index, (item, details) in enumerate(self.items.items(), 1):
                print(f"{index}. {item}: ₹{details['price']:.2f} - Category: {details['category']} - {details['description']}")

    def add_to_cart(self):
        """Add items to cart by selecting item numbers."""
        while True:
            self.view_items()  # Display items with numbers
            try:
                item_number = int(input("Enter the item number to add to the cart (or '0' to finish): ").strip())
                
                if item_number == 0:
                    break

                if item_number < 1 or item_number > len(self.items):
                    print("Invalid item number. Please try again.")
                    continue

                # Get item name using the number
                item_name = list(self.items.keys())[item_number - 1]
                quantity = int(input(f"Enter quantity for {item_name}: "))

                if item_name in self.cart:
                    self.cart[item_name] += quantity
                else:
                    self.cart[item_name] = quantity

                print(f"Added {quantity} of {item_name} to the cart.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    
    def update_cart(self):
        """Update or remove items in the cart."""
        while True:
            item_name = input("Enter the item name to update/remove (or 'done' to finish): ").strip()
            if item_name.lower() == 'done':
                break
            if item_name in self.cart:
                action = input(f"Do you want to 'update' or 'remove' {item_name} (current quantity: {self.cart[item_name]}): ").strip().lower()
                if action == 'update':
                    try:
                        new_quantity = int(input(f"Enter new quantity for {item_name}: "))
                        if new_quantity <= 0:
                            print("Quantity must be greater than 0.")
                        else:
                            self.cart[item_name] = new_quantity
                            print(f"Updated {item_name} quantity to {new_quantity}.")
                    except ValueError:
                        print("Invalid quantity. Please enter a valid integer.")
                elif action == 'remove':
                    del self.cart[item_name]
                    print(f"Removed {item_name} from the cart.")
                else:
                    print("Invalid action. Please type 'update' or 'remove'.")
            else:
                print(f"{item_name} is not in the cart. Try again.")

    def calculate_total(self):
        """Calculate the total cost with tax and apply promotions."""
        total_cost = 0
        total_discount = 0
        for item, quantity in self.cart.items():
            item_price = self.items[item]["price"]
            # Apply promotions
            if item in self.promotions:
                promo = self.promotions[item]
                if promo["type"] == "percentage":
                    item_price *= (1 - promo["value"] / 100)
                elif promo["type"] == "fixed":
                    item_price -= promo["value"]
                    item_price = max(item_price, 0)  # Ensure price doesn't go below 0
            total_cost += item_price * quantity
        discountable_amount = total_cost
        discount_amount = discountable_amount * (self.discount_rate / 100)
        payable_amount = total_cost - discount_amount
        return total_cost, discountable_amount, discount_amount, payable_amount

    def save_invoice_to_file(self, customer_name):
        """Save the invoice to a file with the customer's name as the filename."""
        if not self.cart:
            print("Your cart is empty.")
            return

        # Use customer_name as the filename (replace spaces with underscores)
        file_name = f"{customer_name.replace(' ', '_')}_invoice.txt"

        # Get current date and time
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
        # Prepare the invoice content
        invoice_content = "=" * 60 + "\n"
        invoice_content += f"ELECTRONIC STORE\t\tINVOICE\n\n"
        invoice_content += f"Invoice: {date_str}-{time_str.replace(':', '-')}\tDate: {date_str}\n"
        invoice_content += f"\t\t\tTime: {time_str}\n"
        invoice_content += f"Name of Customer: {customer_name}\n"
        invoice_content += "=" * 60 + "\n"
        invoice_content += f"PARTICULAR\tQUANTITY\tUNIT PRICE\tTOTAL\n"
        invoice_content += "-" * 60 + "\n"
        
        total_cost = 0
        for item, quantity in self.cart.items():
            total = self.items[item]["price"] * quantity
            # Apply promotions
            if item in self.promotions:
                promo = self.promotions[item]
                if promo["type"] == "percentage":
                    total *= (1 - promo["value"] / 100)
                elif promo["type"] == "fixed":
                    total -= promo["value"]
                    total = max(total, 0)  # Ensure price doesn't go below 0
            invoice_content += f"{item:<15} {quantity:<10} ₹{self.items[item]['price']:<10.2f} ₹{total:<10.2f}\n"
            total_cost += total
        
        # Calculate the discountable and payable amount
        total_cost, discountable_amount, discount_amount, payable_amount = self.calculate_total()
        
        invoice_content += "-" * 60 + "\n"
        invoice_content += f"\t\tYour discountable amount: ₹{discountable_amount:.2f}\n"
        invoice_content += "-" * 60 + "\n"
        invoice_content += f"\t\tYour {self.discount_rate}% discounted amount is: ₹{discount_amount:.2f}\n"
        invoice_content += "-" * 60 + "\n"
        invoice_content += f"\t\tYour payable amount is: ₹{payable_amount:.2f}\n"
        invoice_content += "-" * 60 + "\n"

        invoice_content += f"\n\tThank You {customer_name} for your shopping.\n"
        invoice_content += "\t\tSee you again!\n"
        invoice_content += "=" * 60 + "\n"

        # Save to a file using UTF-8 encoding to support the ₹ symbol
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(invoice_content)

        print(f"\nInvoice saved to {file_name} successfully!")

        # Save to past invoices
        self.past_invoices.append({"customer": customer_name, "filename": file_name})

    def view_past_invoices(self):
        """Display the list of past invoices."""
        if not self.past_invoices:
            print("No past invoices.")
        else:
            print("\nPast Invoices:")
            for invoice in self.past_invoices:
                print(f"Customer: {invoice['customer']}, Filename: {invoice['filename']}")

# Driver code to use the BillSystem class
if __name__ == "__main__":
    bill_system = BillSystem()

    # Add some items to the system (in INR)
    bill_system.add_item("APPLE SMART WATCH", 24000, category="Gadgets", description="Apple Smart Watch with advanced features.")
    bill_system.add_item("SMART WATCH", 5000, category="Gadgets", description="Basic Smart Watch with fitness tracking features.")
    bill_system.add_item("PHONE", 70000, category="Electronics", description="Smartphone with 128GB storage.")
    bill_system.add_item("LAPTOP", 150000, category="Electronics", description="Laptop with 16GB RAM, 1TB SSD.")
    bill_system.add_item("TABLET", 35000, category="Electronics", description="Tablet with 10-inch screen and stylus support.")
    bill_system.add_item("WIRELESS EARPHONES", 3000, category="Gadgets", description="Bluetooth wireless earphones with noise cancellation.")
    bill_system.add_item("SMART SPEAKER", 7000, category="Gadgets", description="Voice-activated smart speaker with Alexa.")

    # Set a promotion
    bill_system.add_promotion("LAPTOP", discount_type="percentage", discount_value=10)

    # Run the menu
    customer_name = input("Enter the customer's name: ").strip()

    while True:
        print("\n1. View available items")
        print("2. Add items to cart")
        print("3. Update or remove items in cart")
        print("4. Save invoice to file")
        print("5. View past invoices")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            bill_system.view_items()
        elif choice == '2':
            bill_system.add_to_cart()
        elif choice == '3':
            bill_system.update_cart()
        elif choice == '4':
            bill_system.save_invoice_to_file(customer_name)
        elif choice == '5':
            bill_system.view_past_invoices()
        elif choice == '6':
            print("Exiting the bill system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
