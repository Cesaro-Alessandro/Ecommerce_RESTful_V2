import DBManager
import mysql.connector


class Product:
    def __init__(self, id, name, brand, price):
        self.id = id
        self.name = name
        self.brand = brand
        self.price = price

    def get_id(self):
        return self.id

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_brand(self, brand):
        self.brand = brand

    def get_brand(self):
        return self.brand

    def set_price(self, price):
        self.price = price

    def get_price(self):
        return self.price

    @staticmethod
    def get_All():
        connection = DBManager.Database()
        try:
            connection = connection._connection
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM products")
            result = cursor.fetchall()
            return result
        except:
            print("Database error")
            return None

    @staticmethod
    def get_By_Id(id):
        connection = DBManager.Database()
        try:
            connection = connection._connection
            cursor = connection.cursor(dictionary=True)
            sql = "SELECT * FROM products WHERE id = %s"
            bind = (str(id),)
            cursor.execute(sql, bind)
            result = cursor.fetchone()
            return result
        except:
            print("Database error")
            return None

    @staticmethod
    def delete_By_Id(id):
        connection = DBManager.Database()
        try:
            product = Product.get_By_Id(id)
            if product:
                connection = connection._connection
                cursor = connection.cursor()
                sql = "DELETE FROM products WHERE id = %s"
                bind = (str(id),)
                cursor.execute(sql, bind)
                connection.commit()
                return True
            else:
                return False
        except:
            print("Database error")
            return None

    @staticmethod
    def create(params):
        connection = DBManager.Database()
        try:
            connection = connection._connection
            cursor = connection.cursor()
            sql = "INSERT INTO products (name, brand, price) VALUES(%s, %s, %s)"
            bind = (params[0], params[1], float(params[2]))
            cursor.execute(sql, bind)
            connection.commit()
            product = Product.get_By_Id(cursor.lastrowid)
            return product
        except:
            print("Database error")
            return None

    def update(params):
        connection = DBManager.Database()
        i = 0
        product = Product.get_By_Id(params[0])
        for value in product:
            if params[i] == None:
                params[i] = value
            i += 1
        connection = connection._connection
        cursor = connection.cursor()
        sql = "UPDATE products SET name = %s, brand = %s, price = %s WHERE id = %s"
        bind = (params[1], params[2], params[3], params[0])
        cursor.execute(sql, bind)
        connection.commit()
        result = Product.get_By_Id(params[0])
        return result
