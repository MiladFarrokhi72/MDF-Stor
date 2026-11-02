from datetime import date
from peewee import (
    SqliteDatabase,
    Model,
    AutoField,
    CharField,
    DecimalField,
    IntegerField,
    DateField,
    ForeignKeyField,
    DoesNotExist,
)

DATABASE = SqliteDatabase("mdf_shop.db")


class BaseModel(Model):
    class Meta:
        database = DATABASE


class Customer(BaseModel):
    CustomerID = AutoField()
    FirstName = CharField(max_length=50)
    LastName = CharField(max_length=50)
    Phone = CharField(max_length=20)
    Address = CharField(max_length=255, null=True)


class SalesExpert(BaseModel):
    ExpertID = AutoField()
    FirstName = CharField(max_length=50)
    LastName = CharField(max_length=50)
    Phone = CharField(max_length=20)


class MDFSheet(BaseModel):
    ProductID = AutoField()
    Brand = CharField(max_length=60)
    Color = CharField(max_length=40)
    Thickness = DecimalField(max_digits=6, decimal_places=2)
    Length = DecimalField(max_digits=8, decimal_places=2)
    Width = DecimalField(max_digits=8, decimal_places=2)
    UnitPrice = DecimalField(max_digits=12, decimal_places=2)
    Stock = IntegerField(default=0)


class Sale(BaseModel):
    SaleID = AutoField()
    Customer = ForeignKeyField(Customer, backref="sales", on_delete="RESTRICT")
    Expert = ForeignKeyField(SalesExpert, backref="sales", on_delete="RESTRICT")
    Product = ForeignKeyField(MDFSheet, backref="sales", on_delete="RESTRICT")
    SaleDate = DateField(default=date.today)
    Quantity = IntegerField()
    UnitPrice = DecimalField(max_digits=12, decimal_places=2)
    TotalPrice = DecimalField(max_digits=14, decimal_places=2)


def pause():
    input("\nPress Enter to continue...")


def read_int(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Please enter a valid whole number.")


def read_decimal(prompt):
    while True:
        try:
            value = input(prompt).strip()
            return round(float(value), 2)
        except ValueError:
            print("Please enter a valid number.")


def show_customers():
    rows = list(Customer.select().order_by(Customer.CustomerID))
    if not rows:
        print("No customers found.")
        return
    for item in rows:
        print(
            f"ID: {item.CustomerID} | Name: {item.FirstName} {item.LastName} "
            f"| Phone: {item.Phone} | Address: {item.Address or '-'}"
        )


def show_products():
    rows = list(MDFSheet.select().order_by(MDFSheet.ProductID))
    if not rows:
        print("No MDF sheets found.")
        return
    for item in rows:
        print(
            f"ID: {item.ProductID} | Brand: {item.Brand} | Color: {item.Color} "
            f"| Thickness: {item.Thickness} | Size: {item.Length} x {item.Width} "
            f"| Unit price: {item.UnitPrice} | Stock: {item.Stock}"
        )


def show_experts():
    rows = list(SalesExpert.select().order_by(SalesExpert.ExpertID))
    if not rows:
        print("No sales experts found.")
        return
    for item in rows:
        print(
            f"ID: {item.ExpertID} | Name: {item.FirstName} {item.LastName} "
            f"| Phone: {item.Phone}"
        )


def create_customer():
    print("\nCREATE CUSTOMER")
    first = input("First name: ").strip()
    last = input("Last name: ").strip()
    phone = input("Phone: ").strip()
    address = input("Address: ").strip()
    if not first or not last or not phone:
        print("First name, last name, and phone are required.")
        return
    obj = Customer.create(
        FirstName=first, LastName=last, Phone=phone, Address=address or None
    )
    print(f"Customer created successfully. ID: {obj.CustomerID}")


def create_product():
    print("\nCREATE MDF SHEET")
    brand = input("Brand: ").strip()
    color = input("Color: ").strip()
    thickness = read_decimal("Thickness: ")
    length = read_decimal("Length: ")
    width = read_decimal("Width: ")
    price = read_decimal("Unit price: ")
    stock = read_int("Stock quantity: ")
    if not brand or not color or min(thickness, length, width, price) < 0 or stock < 0:
        print("Please enter valid product information.")
        return
    obj = MDFSheet.create(
        Brand=brand, Color=color, Thickness=thickness, Length=length,
        Width=width, UnitPrice=price, Stock=stock
    )
    print(f"MDF sheet created successfully. ID: {obj.ProductID}")


def create_expert():
    print("\nCREATE SALES EXPERT")
    first = input("First name: ").strip()
    last = input("Last name: ").strip()
    phone = input("Phone: ").strip()
    if not first or not last or not phone:
        print("First name, last name, and phone are required.")
        return
    obj = SalesExpert.create(FirstName=first, LastName=last, Phone=phone)
    print(f"Sales expert created successfully. ID: {obj.ExpertID}")


def find_record(model, field, record_id, label):
    try:
        return model.get(field == record_id)
    except DoesNotExist:
        print(f"{label} not found.")
        return None


def delete_record(model, field, label):
    record_id = read_int(f"{label} ID to delete: ")
    obj = find_record(model, field, record_id, label)
    if obj is None:
        return
    confirm = input(f"Delete {label.lower()} #{record_id}? (y/n): ").strip().lower()
    if confirm == "y":
        try:
            obj.delete_instance()
            print(f"{label} deleted successfully.")
        except Exception:
            print(f"Could not delete {label.lower()}. It may be linked to a sale.")
    else:
        print("Delete operation cancelled.")


def search_record(model, field, label):
    record_id = read_int(f"{label} ID to search: ")
    obj = find_record(model, field, record_id, label)
    if obj is not None:
        print(obj)


def update_customer():
    record_id = read_int("Customer ID to update: ")
    obj = find_record(Customer, Customer.CustomerID, record_id, "Customer")
    if obj is None:
        return
    print("Leave a field blank to keep its current value.")
    value = input(f"First name [{obj.FirstName}]: ").strip()
    if value:
        obj.FirstName = value
    value = input(f"Last name [{obj.LastName}]: ").strip()
    if value:
        obj.LastName = value
    value = input(f"Phone [{obj.Phone}]: ").strip()
    if value:
        obj.Phone = value
    value = input(f"Address [{obj.Address or ''}]: ").strip()
    if value:
        obj.Address = value
    obj.save()
    print("Customer updated successfully.")


def update_product():
    record_id = read_int("MDF sheet ID to update: ")
    obj = find_record(MDFSheet, MDFSheet.ProductID, record_id, "MDF sheet")
    if obj is None:
        return
    print("Leave a field blank to keep its current value.")
    fields = [
        ("Brand", "Brand", str),
        ("Color", "Color", str),
        ("Thickness", "Thickness", float),
        ("Length", "Length", float),
        ("Width", "Width", float),
        ("Unit price", "UnitPrice", float),
        ("Stock", "Stock", int),
    ]
    for prompt, attr, converter in fields:
        current = getattr(obj, attr)
        value = input(f"{prompt} [{current}]: ").strip()
        if value:
            try:
                converted = converter(value)
                if converted < 0:
                    raise ValueError
                setattr(obj, attr, converted)
            except ValueError:
                print(f"Invalid value for {prompt}. Keeping the previous value.")
    obj.save()
    print("MDF sheet updated successfully.")


def update_expert():
    record_id = read_int("Sales expert ID to update: ")
    obj = find_record(SalesExpert, SalesExpert.ExpertID, record_id, "Sales expert")
    if obj is None:
        return
    print("Leave a field blank to keep its current value.")
    for prompt, attr in [
        ("First name", "FirstName"),
        ("Last name", "LastName"),
        ("Phone", "Phone"),
    ]:
        value = input(f"{prompt} [{getattr(obj, attr)}]: ").strip()
        if value:
            setattr(obj, attr, value)
    obj.save()
    print("Sales expert updated successfully.")


def create_sale():
    print("\nCREATE SALE")
    print("\nCustomers:")
    show_customers()
    customer_id = read_int("Customer ID: ")
    customer = find_record(Customer, Customer.CustomerID, customer_id, "Customer")
    if customer is None:
        return

    print("\nSales experts:")
    show_experts()
    expert_id = read_int("Sales expert ID: ")
    expert = find_record(SalesExpert, SalesExpert.ExpertID, expert_id, "Sales expert")
    if expert is None:
        return

    print("\nMDF sheets:")
    show_products()
    product_id = read_int("MDF sheet ID: ")
    product = find_record(MDFSheet, MDFSheet.ProductID, product_id, "MDF sheet")
    if product is None:
        return

    quantity = read_int("Quantity: ")
    if quantity <= 0:
        print("Quantity must be greater than zero.")
        return
    if quantity > product.Stock:
        print(f"Insufficient stock. Available quantity: {product.Stock}")
        return

    unit_price = read_decimal(f"Unit price [{product.UnitPrice}]: ")
    if unit_price < 0:
        print("Unit price cannot be negative.")
        return
    total = round(unit_price * quantity, 2)

    with DATABASE.atomic():
        sale = Sale.create(
            Customer=customer,
            Expert=expert,
            Product=product,
            Quantity=quantity,
            UnitPrice=unit_price,
            TotalPrice=total,
        )
        product.Stock -= quantity
        product.save()

    print(f"Sale created successfully. Sale ID: {sale.SaleID}")
    print(f"Total price: {total}")


def show_sales():
    rows = Sale.select().order_by(Sale.SaleID)
    found = False
    for sale in rows:
        found = True
        print(
            f"Sale ID: {sale.SaleID} | Customer: {sale.Customer.FirstName} "
            f"{sale.Customer.LastName} | Expert: {sale.Expert.FirstName} "
            f"{sale.Expert.LastName} | Product: {sale.Product.Brand} "
            f"({sale.Product.Color}) | Date: {sale.SaleDate} "
            f"| Quantity: {sale.Quantity} | Unit price: {sale.UnitPrice} "
            f"| Total: {sale.TotalPrice}"
        )
    if not found:
        print("No sales found.")


def search_sale():
    sale_id = read_int("Sale ID to search: ")
    sale = find_record(Sale, Sale.SaleID, sale_id, "Sale")
    if sale is not None:
        print(
            f"Sale ID: {sale.SaleID} | Customer: {sale.Customer.FirstName} "
            f"{sale.Customer.LastName} | Expert: {sale.Expert.FirstName} "
            f"{sale.Expert.LastName} | Product: {sale.Product.Brand} "
            f"({sale.Product.Color}) | Date: {sale.SaleDate} "
            f"| Quantity: {sale.Quantity} | Unit price: {sale.UnitPrice} "
            f"| Total: {sale.TotalPrice}"
        )


def delete_sale():
    sale_id = read_int("Sale ID to delete: ")
    sale = find_record(Sale, Sale.SaleID, sale_id, "Sale")
    if sale is None:
        return
    confirm = input(f"Delete sale #{sale_id}? (y/n): ").strip().lower()
    if confirm == "y":
        with DATABASE.atomic():
            product = sale.Product
            product.Stock += sale.Quantity
            product.save()
            sale.delete_instance()
        print("Sale deleted successfully. Product stock has been restored.")
    else:
        print("Delete operation cancelled.")


def update_sale():
    sale_id = read_int("Sale ID to update: ")
    sale = find_record(Sale, Sale.SaleID, sale_id, "Sale")
    if sale is None:
        return

    print("Enter the new values. Leave an ID blank to keep the current value.")
    customer_text = input(f"Customer ID [{sale.Customer_id}]: ").strip()
    expert_text = input(f"Sales expert ID [{sale.Expert_id}]: ").strip()
    product_text = input(f"MDF sheet ID [{sale.Product_id}]: ").strip()
    quantity_text = input(f"Quantity [{sale.Quantity}]: ").strip()
    price_text = input(f"Unit price [{sale.UnitPrice}]: ").strip()

    customer = sale.Customer
    expert = sale.Expert
    product = sale.Product
    quantity = sale.Quantity
    unit_price = float(sale.UnitPrice)

    if customer_text:
        customer = find_record(Customer, Customer.CustomerID, int(customer_text), "Customer")
        if customer is None:
            return
    if expert_text:
        expert = find_record(SalesExpert, SalesExpert.ExpertID, int(expert_text), "Sales expert")
        if expert is None:
            return
    if product_text:
        product = find_record(MDFSheet, MDFSheet.ProductID, int(product_text), "MDF sheet")
        if product is None:
            return
    try:
        if quantity_text:
            quantity = int(quantity_text)
        if price_text:
            unit_price = float(price_text)
        if quantity <= 0 or unit_price < 0:
            raise ValueError
    except ValueError:
        print("Invalid quantity or unit price.")
        return

    # Restore the old quantity before checking stock for the updated sale.
    old_product = sale.Product
    with DATABASE.atomic():
        old_product.Stock += sale.Quantity
        old_product.save()

        if product.ProductID != old_product.ProductID:
            if quantity > product.Stock:
                old_product.Stock -= sale.Quantity
                old_product.save()
                print(f"Insufficient stock. Available quantity: {product.Stock}")
                return
            product.Stock -= quantity
            product.save()
        else:
            if quantity > product.Stock:
                old_product.Stock -= sale.Quantity
                old_product.save()
                print(f"Insufficient stock. Available quantity: {product.Stock}")
                return
            product.Stock -= quantity
            product.save()

        sale.Customer = customer
        sale.Expert = expert
        sale.Product = product
        sale.Quantity = quantity
        sale.UnitPrice = unit_price
        sale.TotalPrice = round(quantity * unit_price, 2)
        sale.save()

    print("Sale updated successfully.")


def print_menu():
    print("\n" + "=" * 48)
    print("             MDF SHOP MANAGEMENT")
    print("=" * 48)
    print("1.  Create Customer")
    print("2.  Show Customers")
    print("3.  Delete Customer")
    print("4.  Search Customer")
    print("5.  Update Customer")
    print("6.  Create MDF Sheet")
    print("7.  Show MDF Sheets")
    print("8.  Delete MDF Sheet")
    print("9.  Search MDF Sheet")
    print("10. Update MDF Sheet")
    print("11. Create Sales Expert")
    print("12. Show Sales Experts")
    print("13. Delete Sales Expert")
    print("14. Search Sales Expert")
    print("15. Update Sales Expert")
    print("16. Create Sale")
    print("17. Show Sales")
    print("18. Delete Sale")
    print("19. Search Sale")
    print("20. Update Sale")
    print("21. Exit")


def main():
    DATABASE.connect(reuse_if_open=True)
    DATABASE.create_tables([Customer, SalesExpert, MDFSheet, Sale])

    try:
        while True:
            print_menu()
            choice = read_int("Select an option (1-21): ")

            if choice == 1:
                create_customer()
            elif choice == 2:
                show_customers()
            elif choice == 3:
                delete_record(Customer, Customer.CustomerID, "Customer")
            elif choice == 4:
                search_record(Customer, Customer.CustomerID, "Customer")
            elif choice == 5:
                update_customer()
            elif choice == 6:
                create_product()
            elif choice == 7:
                show_products()
            elif choice == 8:
                delete_record(MDFSheet, MDFSheet.ProductID, "MDF sheet")
            elif choice == 9:
                search_record(MDFSheet, MDFSheet.ProductID, "MDF sheet")
            elif choice == 10:
                update_product()
            elif choice == 11:
                create_expert()
            elif choice == 12:
                show_experts()
            elif choice == 13:
                delete_record(SalesExpert, SalesExpert.ExpertID, "Sales expert")
            elif choice == 14:
                search_record(SalesExpert, SalesExpert.ExpertID, "Sales expert")
            elif choice == 15:
                update_expert()
            elif choice == 16:
                create_sale()
            elif choice == 17:
                show_sales()
            elif choice == 18:
                delete_sale()
            elif choice == 19:
                search_sale()
            elif choice == 20:
                update_sale()
            elif choice == 21:
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please select a number from 1 to 21.")

            pause()

    finally:
        if not DATABASE.is_closed():
            DATABASE.close()


if __name__ == "__main__":
    main()
