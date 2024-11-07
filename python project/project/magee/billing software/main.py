import datetime
import os

class BillSystem:
    def __init__(self):
        self.items = {}
        self.cart = {}
        self.tax_rate = 0.1
        self.discount_rate = 0
        self.past_invoices = []
        self.categories = {}
        self.promotions = {}

    def add_item(self, name, price, category="General", description=""):
        self.items[name] = {"price": price, "category": category, "description": description}
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(name)
    
    def add_promotion(self, item_name, discount_type="percentage", discount_value=0):
        self.promotions[item_name] = {"type": discount_type, "value": discount_value}

    def view_items(self):
        if not self.items:
            print("No items available.")
        else:
            print("\nAvailable Items:")
            for index, (item, details) in enumerate(self.items.items(), 1):
                print(f"{index}. {item}: ₹{details['price']:.2f} - Category: {details['category']} - {details['description']}")

    def add_to_cart(self):
        while True:
            self.view_items()
            try:
                item_number = int(input("Enter the item number to add to the cart (or '0' to finish): ").strip())
                if item_number == 0:
                    break

                if item_number < 1 or item_number > len(self.items):
                    print("Invalid item number. Please try again.")
                    continue

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
        total_cost = 0
        total_discount = 0
        for item, quantity in self.cart.items():
            item_price = self.items[item]["price"]
            if item in self.promotions:
                promo = self.promotions[item]
                if promo["type"] == "percentage":
                    item_price *= (1 - promo["value"] / 100)
                elif promo["type"] == "fixed":
                    item_price -= promo["value"]
                    item_price = max(item_price, 0)
            total_cost += item_price * quantity
        discountable_amount = total_cost
        discount_amount = discountable_amount * (self.discount_rate / 100)
        payable_amount = total_cost - discount_amount
        return total_cost, discountable_amount, discount_amount, payable_amount

    def save_invoice_to_file(self, customer_name):
        if not self.cart:
            print("Your cart is empty.")
            return

        file_name = f"{customer_name.replace(' ', '_')}_invoice.txt"
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
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
            if item in self.promotions:
                promo = self.promotions[item]
                if promo["type"] == "percentage":
                    total *= (1 - promo["value"] / 100)
                elif promo["type"] == "fixed":
                    total -= promo["value"]
                    total = max(total, 0)
            invoice_content += f"{item:<15} {quantity:<10} ₹{self.items[item]['price']:<10.2f} ₹{total:<10.2f}\n"
            total_cost += total
        
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

        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(invoice_content)

        print(f"\nInvoice saved to {file_name} successfully!")

        self.past_invoices.append({"customer": customer_name, "filename": file_name})

    def view_past_invoices(self):
        if not self.past_invoices:
            print("No past invoices.")
        else:
            print("\nPast Invoices:")
            for invoice in self.past_invoices:
                print(f"Customer: {invoice['customer']}, Filename: {invoice['filename']}")

if __name__ == "__main__":
    bill_system = BillSystem()

    bill_system.add_item("APPLE SMART WATCH", 24000, category="Gadgets", description="Apple Smart Watch with advanced features.")
    bill_system.add_item("SMART WATCH", 5000, category="Gadgets", description="Basic Smart Watch with fitness tracking features.")
    bill_system.add_item("PHONE", 70000, category="Electronics", description="Smartphone with 128GB storage.")
    bill_system.add_item("LAPTOP", 150000, category="Electronics", description="Laptop with 16GB RAM, 1TB SSD.")
    bill_system.add_item("TABLET", 35000, category="Electronics", description="Tablet with 10-inch screen and stylus support.")
    bill_system.add_item("WIRELESS EARPHONES", 3000, category="Gadgets", description="Bluetooth wireless earphones with noise cancellation.")
    bill_system.add_item("SMART SPEAKER", 7000, category="Gadgets", description="Voice-activated smart speaker with Alexa.")

    bill_system.add_promotion("LAPTOP", discount_type="percentage", discount_value=10)
    
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
            print("Thank you for using the billing system!")
            break
        else:
            print("Invalid choice. Please try again.")
