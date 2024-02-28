import mysql.connector


class Database:
    def __init__(self):
        try:
            data = self.__get_File_Data()
            self._connection = mysql.connector.connect(
                host=data[0], user=data[1], password=data[2], database=data[3]
            )
        except:
            self._connection = None
            print("Cannot connect to database")

    @classmethod
    def __get_File_Data(self):
        file = open("Config.txt", "r")
        data = []
        for line in file:
            data.append(line.strip().split(":")[1])
        file.close()
        return data
