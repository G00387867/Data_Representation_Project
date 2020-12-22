import mysql.connector
import dbconfig as cfg


class StockDAO:

    
    def initConnectToDB(self):
        db = mysql.connector.connect(
            host=       cfg.mysql["host"],
            user=       cfg.mysql["user"],
            password=   cfg.mysql["password"],
            database=   cfg.mysql["database"],
            pool_name="my_connection_pool",
            pool_size=10
        )
        return db

    def getConnection(self):
        db = mysql.connector.connect(
            pool_name='my_connection_pool'
        )
        return db
    
    def __init__(self):
        db = self.initConnectToDB()
        db.close()


    def create (self, values):
        db = self.getConnection()
        cursor = db.cursor()
        sql = "insert into stocks (item, category, price) values (%s, %s, %s)"
        cursor.execute(sql, values)
        
        self.db.commit()
        lastRoWId = cursor.lastrowid
        db.close()
        return lastRoWId

    def getAll (self):
        db = self.getConnection()
        cursor = db.cursor()
        sql = "select * from stocks"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print (results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))
        db.close()
        return returnArray


    def findByID (self, id):
        db = self.getConnection()
        cursor = db.cursor()
        sql = "select * from stocks where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        stocks = self.convertToDictionary(result)
        db.close()
        return stocks


    def update (self, values):
        db = self.getConnection()
        cursor = db.cursor()
        sql = "update stocks set item = %s, category = %s , price = %s where id = %s "        
        cursor.execute(sql, values)
        self.db.commit()
        db.close()

    def delete (self, id):
        db = self.getConnection()
        cursor = db.cursor()
        sql = "delete from stocks where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        self.db.commit()
        db.close()

        # print("delete done")

    def convertToDictionary(self, result):
        colnames=["id", "item", "category", "price"]
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item      

stockDAO = StockDAO()
