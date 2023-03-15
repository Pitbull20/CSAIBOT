import sqlite3


class DataBase:
    def __init__(self, fileName):

        self.dbName = "DataBase/" + fileName
        conn = sqlite3.connect(self.dbName)
        cursor = conn.cursor()
        cursor.execute('''
            create table if not exists Groups 
            (
                Id integer primary key ,
                GroupId integer unique not null,
                UniversityGroupName text default 'КНШІ',
                GroupNumber int default 11
            )
        ''')
        conn.commit()
        conn.close()

    def create(self, id):
        conn = sqlite3.connect(self.dbName)
        cursor = conn.cursor()
        cursor.execute(f"insert or ignore into Groups (GroupId) values ({id})")
        conn.commit()
        conn.close()

    def get_element_by_id(self,id):
        conn = sqlite3.connect(self.dbName)
        cursor = conn.cursor()
        cursor.execute(f"select * from Groups where id = {id}")
        rows = cursor.fetchone()
        conn.close()
        return rows
