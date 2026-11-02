import sqlite3


def connect_db():
    db = sqlite3.connect("mdf_shop.db")
    db.execute("PRAGMA foreign_keys = ON")
    return db


def create_tables():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Customer (
            CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            Phone TEXT,
            Address TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Sales_Expert (
            ExpertID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            Phone TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
            Brand TEXT NOT NULL,
            Color TEXT,
            Thickness REAL,
            Length REAL,
            Width REAL,
            UnitPrice INTEGER NOT NULL,
            Stock INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Sales (
            SaleID INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerID INTEGER,
            ExpertID INTEGER,
            ProductID INTEGER,
            SaleDate TEXT,
            Quantity INTEGER NOT NULL,
            UnitPrice INTEGER NOT NULL,
            TotalPrice INTEGER NOT NULL,
            FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
            FOREIGN KEY (ExpertID) REFERENCES Sales_Expert(ExpertID),
            FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
        )
    """)

    db.commit()
    db.close()


def get_input(message):
    return input(message).strip()


def register_customer():
    db = connect_db()
    cursor = db.cursor()

    first = get_input("First Name: ")
    last = get_input("Last Name: ")
    phone = get_input("Phone: ")
    address = get_input("Address: ")

    cursor.execute("""
        INSERT INTO Customer (FirstName, LastName, Phone, Address)
        VALUES (?, ?, ?, ?)
    """, (first, last, phone, address))

    db.commit()
    print("Customer created successfully!")
    print("Customer ID:", cursor.lastrowid)
    db.close()


def register_product():
    db = connect_db()
    cursor = db.cursor()

    brand = get_input("Brand: ")
    color = get_input("Color: ")
    thickness = float(get_input("Thickness: "))
    length = float(get_input("Length: "))
    width = float(get_input("Width: "))
    price = int(get_input("Unit Price: "))
    stock = int(get_input("Stock: "))

    cursor.execute("""
        INSERT INTO Products
        (Brand, Color, Thickness, Length, Width, UnitPrice, Stock)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (brand, color, thickness, length, width, price, stock))

    db.commit()
    print("Product created successfully!")
    print("Product ID:", cursor.lastrowid)
    db.close()


def register_expert():
    db = connect_db()
    cursor = db.cursor()

    first = get_input("First Name: ")
    last = get_input("Last Name: ")
    phone = get_input("Phone: ")

    cursor.execute("""
        INSERT INTO Sales_Expert (FirstName, LastName, Phone)
        VALUES (?, ?, ?)
    """, (first, last, phone))

    db.commit()
    print("Sales expert created successfully!")
    print("Expert ID:", cursor.lastrowid)
    db.close()


def show_data(table):
    allowed_tables = {"Customer", "Products", "Sales_Expert"}
    if table not in allowed_tables:
        print("Invalid table!")
        return

    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    records = cursor.fetchall()

    if records:
        for record in records:
            print(record)
    else:
        print("No information found!")

    db.close()


def search_data(table, id_field):
    db = connect_db()
    cursor = db.cursor()

    try:
        user_id = int(get_input("Enter ID: "))
    except ValueError:
        print("Please enter a valid numeric ID.")
        db.close()
        return

    cursor.execute(
        f"SELECT * FROM {table} WHERE {id_field} = ?",
        (user_id,)
    )
    result = cursor.fetchone()

    if result:
        print("Information found:")
        print(result)
    else:
        print("Record not found!")

    db.close()


def delete_data(table, id_field):
    db = connect_db()
    cursor = db.cursor()

    try:
        user_id = int(get_input("Enter ID to delete: "))
    except ValueError:
        print("Please enter a valid numeric ID.")
        db.close()
        return

    cursor.execute(
        f"SELECT * FROM {table} WHERE {id_field} = ?",
        (user_id,)
    )
    result = cursor.fetchone()

    if result:
        confirm = get_input("Are you sure? (y/n): ")

        if confirm.lower() == "y":
            try:
                cursor.execute(
                    f"DELETE FROM {table} WHERE {id_field} = ?",
                    (user_id,)
                )
                db.commit()
                print("Record deleted successfully!")
            except sqlite3.IntegrityError:
                print("Cannot delete! This record is used in Sales.")
        else:
            print("Delete cancelled!")
    else:
        print("Record not found!")

    db.close()


def update_data(table, id_field, fields):
    db = connect_db()
    cursor = db.cursor()

    try:
        user_id = int(get_input("Enter ID to update: "))
    except ValueError:
        print("Please enter a valid numeric ID.")
        db.close()
        return

    cursor.execute(
        f"SELECT * FROM {table} WHERE {id_field} = ?",
        (user_id,)
    )
    result = cursor.fetchone()

    if not result:
        print("Record not found!")
        db.close()
        return

    print("Leave blank to keep the previous value.")
    values = []

    for index, field in enumerate(fields):
        new_value = get_input(f"Enter new {field}: ")
        if new_value == "":
            values.append(result[index + 1])
        else:
            values.append(new_value)

    query = ", ".join(f"{field} = ?" for field in fields)

    cursor.execute(
        f"UPDATE {table} SET {query} WHERE {id_field} = ?",
        (*values, user_id)
    )

    db.commit()
    print("Information updated successfully!")
    db.close()


def menu():
    while True:
        print("""
====================================
       MDF SHOP MANAGEMENT
====================================

1.  Create Customer
2.  Create MDF Sheet
3.  Create Sales Expert

4.  Show Customers
5.  Show MDF Sheets
6.  Show Sales Experts

7.  Delete Customer
8.  Delete MDF Sheet
9.  Delete Sales Expert

10. Search Customer
11. Search MDF Sheet
12. Search Sales Expert

13. Update Customer
14. Update MDF Sheet
15. Update Sales Expert

0. Exit

====================================
""")

        choice = get_input("Please Select: ")

        if choice == "1":
            register_customer()
        elif choice == "2":
            register_product()
        elif choice == "3":
            register_expert()
        elif choice == "4":
            show_data("Customer")
        elif choice == "5":
            show_data("Products")
        elif choice == "6":
            show_data("Sales_Expert")
        elif choice == "7":
            delete_data("Customer", "CustomerID")
        elif choice == "8":
            delete_data("Products", "ProductID")
        elif choice == "9":
            delete_data("Sales_Expert", "ExpertID")
        elif choice == "10":
            search_data("Customer", "CustomerID")
        elif choice == "11":
            search_data("Products", "ProductID")
        elif choice == "12":
            search_data("Sales_Expert", "ExpertID")
        elif choice == "13":
            update_data(
                "Customer",
                "CustomerID",
                ["FirstName", "LastName", "Phone", "Address"]
            )
        elif choice == "14":
            update_data(
                "Products",
                "ProductID",
                ["Brand", "Color", "Thickness", "Length",
                 "Width", "UnitPrice", "Stock"]
            )
        elif choice == "15":
            update_data(
                "Sales_Expert",
                "ExpertID",
                ["FirstName", "LastName", "Phone"]
            )
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    create_tables()
    menu()
