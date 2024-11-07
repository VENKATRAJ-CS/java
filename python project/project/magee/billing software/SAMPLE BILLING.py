import datetime

class BillSystem:
    def __init__(self):
        self.items = {}  # Store item name and its price
        self.cart = {}  # Store the items in the cart with quantities
        self.tax_rate = 0.1  # 10% tax
        self.discount_rate = 0  # No discount by default
    
    def add_item(self, name, price):
        """Add item to the bill system."""
        self.items[name] = price
    
    def view_items(self):
        """Display all available items and their prices."""
        if not self.items:
            print("No items available.")
        else:
            print("\nAvailable Items:")
            for item, price in self.items.items():
                print(f"{item}: ${price:.2f}")
    
    def add_to_cart(self):
        """Add items to cart."""
        while True:
            item_name = input("Enter the item name (or 'done' to finish): ").strip()
            if item_name.lower() == 'done':
                break
            if item_name in self.items:
                try:
                    quantity = int(input(f"Enter quantity for {item_name}: "))
                    if item_name in self.cart:
                        self.cart[item_name] += quantity
                    else:
                        self.cart[item_name] = quantity
                    print(f"Added {quantity} of {item_name} to the cart.")
                except ValueError:
                    print("Invalid quantity. Please enter a valid integer.")
            else:
                print(f"Item '{item_name}' not found. Try again.")
    
    def calculate_total(self):
        """Calculate the total cost with tax."""
        total_cost = 0
        for item, quantity in self.cart.items():
            total_cost += self.items[item] * quantity
        discountable_amount = total_cost  # The amount eligible for discount
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
            total = self.items[item] * quantity
            invoice_content += f"{item:<15} {quantity:<10} {self.items[item]:<10} {total:<10}\n"
            total_cost += total
        
        # Calculate the discountable and payable amount
        total_cost, discountable_amount, discount_amount, payable_amount = self.calculate_total()
        
        invoice_content += "-" * 60 + "\n"
        invoice_content += f"\t\tYour discountable amount: {discountable_amount:.2f}\n"
        invoice_content += "-" * 60 + "\n"
        invoice_content += f"\t\tYour {self.discount_rate}% discounted amount is: {discount_amount:.2f}\n"
        invoice_content += "-" * 60 + "\n"
        invoice_content += f"\t\tYour payable amount is: {payable_amount:.2f}\n"
        invoice_content += "-" * 60 + "\n"

        invoice_content += f"\n\tThank You {customer_name} for your shopping.\n"
        invoice_content += "\t\tSee you again!\n"
        invoice_content += "=" * 60 + "\n"

        # Save to a file
        with open(file_name, 'w') as file:
            file.write(invoice_content)

        print(f"\nInvoice saved to {file_name} successfully!")

# Driver code to use the BillSystem class
if __name__ == "__main__":
    bill_system = BillSystem()

    # Add some items to the system
    bill_system.add_item("PHONE", 700)
    bill_system.add_item("LAPTOP", 1500)
    bill_system.add_item("TABLET", 350)
    
    customer_name = input("Enter the customer's name: ").strip()

    while True:
        print("\n1. View available items")
        print("2. Add items to cart")
        print("3. Save invoice to file")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            bill_system.view_items()
        elif choice == '2':
            bill_system.add_to_cart()
        elif choice == '3':
            # Save the invoice to a text file with customer name as filename
            bill_system.save_invoice_to_file(customer_name)
        elif choice == '4':
            print("Thank you for using the billing system!")
            break
        else:
            print("Invalid choice. Please try again.")
