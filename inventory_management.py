import csv

data_file = "inventory_managment.txt"
csv_file = "inventory_managment_sheet.csv"

def extract_product_id(line):
    try:
        return line.strip().split("Product ID is: ")[-1].strip()
    except IndexError:
        return ""
    
def parse_product_line(line):
    """Extracts Product data from text line into dictionary."""
    try:
        parts = line.split(" | ")
        name = parts[0].split(": ")[1]
        category = parts[1].split(": ")[1]
        price = parts[2].split(": ")[1].replace("Rs. ", "")
        stock = parts[3].split(": ")[1] 
        product_id = parts[4].split(": ")[1]
        return {
            "Name": name,
            "Category": category,
            "Price": price,
            "Stock": stock,
            "Product ID": product_id
        }
    except:
        return None
    
def export_to_csv():
    """Exports text file data to CSV."""
    try:
        with open(data_file, "r") as txtfile:
            lines = [line.strip() for line in txtfile if line.strip()]
        
        if not lines:
            print("⚠️ No data to export!")
            return
        
        employees = [parse_product_line(line) for line in lines if parse_product_line(line)]
        
        with open(csv_file, "w", newline="") as csvfile_obj:
            fieldnames = ["Name", "Category", "Price", "Stock", "Product ID"]
            writer = csv.DictWriter(csvfile_obj, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(employees)
        
        print(f"✅ Data exported successfully to {csv_file}")
    
    except FileNotFoundError:
        print("⚠️ No text file found to export!")

def is_valid_text(text):
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -'.")
    return all(c in allowed for c in text)

def id_exists(product_id):
    try:
        with open(data_file, "r") as file:
            for line in file:
                if extract_product_id(line) == str(product_id):
                    return True
    except FileNotFoundError:
        return False
    return False


def add_product():
    print("\n📝 Add New Product")
    while True:
        name = input("🎁 Enter product name: ").title().strip()
        if is_valid_text(name):
            break
        else:
            print("❌ Name should not contain numbers or special characters.")

    while True:
        category = input("💼 Enter product category: ").title().strip()
        if is_valid_text(category):
            break
        else:
            print("❌ Category should not contain numbers or special characters.")

    while True:
        price = input("💰 Enter product price: ")
        if price.isdigit():
            price = int(price)
            break
        else:
            print("❌ product should be a valid number.")

    while True:
        stock = input("🎁 Enter product stock quantity: ")
        if stock.isdigit():
            stock = int(stock)
            break
        else:
            print("❌ Stock should be a valid number.")

    while True:
        product_id = input("🆔 Enter product ID: ")
        if product_id.isdigit() and not id_exists(product_id):
            product_id = int(product_id)
            break
        else:
            print("❌ Invalid or duplicate product ID.")

    with open(data_file, 'a+') as f:
        f.seek(0)
        if f.read().strip():
            f.write("\n")
        f.write(f"The Product name is: {name} | Product Category is: {category} | Price is: Rs. {price} | Stock is: {stock} | Product ID is: {product_id}")
        print(f"\n✅ {name} added successfully!")


def view_products():
    print("\n🔍 View Product Details")
    product = input("🔎 Enter the name, or Product ID to search: ").strip()
    found = False
    results = []
    try:
        with open(data_file, "r") as file:
            for line in file:
                if product.isdigit():
                    if extract_product_id(line) == product:
                        results.append(f"{line.strip()}")
                        found = True
                else:
                    if product.lower() in line.lower():
                        results.append(f"{line.strip()}")
                        found = True
        if found:
            print("\n📋 Product Details are:\n")
            for result in results:
                print(result)

        else:
            print(f"❌ No details found for {product}.")

    except FileNotFoundError:
        print("⚠️ No data file found. Save something first!")

def update_products():
    print("\n✏️  Update Product Details")
    while True:
        product_id = input("🆔 Enter the Product ID to update: ").strip()
        updated_lines = []
        found = False
        try:
            with open(data_file, "r") as file:
                for line in file:
                    if extract_product_id(line) == product_id:
                        print(f"\n📄 Found: {line.strip()}\n")
                        while True:
                            name = input("🎁 New name: ").title().strip()
                            if is_valid_text(name):
                                break
                            else:
                                print("❌ Name should not contain numbers or special characters.")

                        while True:
                            category = input("💼 New Category: ").title().strip()
                            if is_valid_text(category):
                                break
                            else:
                                print("❌ Category should not contain numbers or special characters.")

                        try:
                            while True:
                                price = input("💰 New Price: ").strip()
                                if price.isdigit():
                                    break
                                else:
                                    print("❌ Price should be a valid number.")
                            
                            while True:
                                stock = input("🎁 New Stock Quantity: ").strip()
                                if stock.isdigit():
                                    break
                                else:
                                    print("❌ Stock should be a valid number.")


                        except ValueError:
                            print("⚠️ Please enter a valid number for Price.")
                            return
                        
                        updated_line = f"The Product name is: {name} | Product Category is: {category} | Price is: Rs. {price} | Stock is: {stock} | Product ID is: {product_id}\n"
                        updated_lines.append(updated_line)
                        found = True
                    else:
                        updated_lines.append(line)

            if found:
                with open(data_file, "w") as file:
                    file.writelines(updated_lines)
                print("\n✅ Product details updated successfully!")
                break
            else:
                print("❌ No Product found with that ID.")

        except FileNotFoundError:
            print("⚠️ No data file found. Add some Product first!")
            break


def delete_product():
    print("\n🗑️  Delete Product")
    while True:
        product_id = input("🆔 Enter the Product ID to delete: ").strip()
        updated_lines = []
        found = False
        confirm = input("❓ Are you sure? Type 'yes' to proceed: ").lower()
        if confirm != "yes":
            print("❌ Action cancelled.")
            return
        else:
            with open(data_file, "r") as file:
                for line in file:
                    if extract_product_id(line) == product_id:
                        print(f"🧾 Deleting: {line.strip()}")
                        found = True
                        continue
                    if line.strip():
                        updated_lines.append(line.strip())

            if found:
                with open(data_file, "w") as file:
                    file.writelines("\n".join(updated_lines))
                print("\n✅ Product deleted successfully!")
                break
            else:
                print("❌ No Product found with that ID.")


def run_product_program():
    print("\n👋 Welcome to the Product Management System!")
    while True:
      print("\n📌 ---- MENU ----\n1️⃣  Add Product\n2️⃣  View All Products\n3️⃣  View Product\n4️⃣  Update Product\n5️⃣  Delete Product\n6️⃣  Export to CSV\n7️⃣  Exit")
      choice = input("👉 Choose an option: ").lower().strip()
      if "add" in choice or "1" in choice:
          add_product()

      elif "all" in choice or "2" in choice:
        try:
            with open(data_file, "r") as file:
                print("\n📋 All Products:\n")
                print(file.read())

        except FileNotFoundError:
            print("⚠️ No data file found. Add Products first!")

      elif "view" in choice or "3" in choice:
          view_products()

      elif "update" in choice or "4" in choice:
        update_products()

      elif "delete" in choice or "5" in choice:
        delete_product()

      elif "export" in choice or "6" in choice:
            export_to_csv()

      elif "exit" in choice or "7" in choice:
          print("\n👋 Goodbye! Have a productive day!\n")
          break
      
      else:
          print("Invalid choice. Please say 'add', 'view all', 'view product', 'update', 'delete' or 'exit'.\n")

run_product_program()