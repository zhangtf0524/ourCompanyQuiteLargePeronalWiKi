import sqlite3


class Sqlite3Database(object):
    """SQLite 数据库操作类"""

    def __init__(self, db_name):
        """初始化，连接到指定的数据库"""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('PRAGMA foreign_keys = ON;')

    def create_table(self, table_name, columns: str):
        """创建表格"""
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.cursor.execute(sql)
        self.conn.commit()

    def drop_table(self, table_name):
        """删除表格"""
        sql = f"DROP TABLE IF EXISTS {table_name}"
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_data(self, table_name, data: dict):
        """插入数据"""
        try:
            columns = ', '.join(data.keys())
            placeholders = ':' + ', :'.join(data.keys())
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            self.cursor.execute(sql, data)
            self.conn.commit()
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
        finally:
            self.conn.rollback()

    def update_data(self, table_name, data: dict, condition):
        """更新数据"""
        try:
            set_clause = ', '.join(f"{key} = :{key}" for key in data.keys())
            sql = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
            self.cursor.execute(sql, data)
            self.conn.commit()
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
        finally:
            self.conn.rollback()


    def delete_data(self, table_name, condition):
        """删除数据"""
        try:
            sql = f"DELETE FROM {table_name} WHERE {condition}"
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
        finally:
            self.conn.rollback()

    def select_data(self, table_name, columns=None, condition=None):
        """查询数据"""
        if columns is None:
            columns = '*'
        if condition is None:
            condition = ''
        else:
            condition = f"WHERE {condition}"
        sql = f"SELECT {columns} FROM {table_name} {condition}"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        columns = [col[0] for col in self.cursor.description]
        data = [dict(zip(columns, row)) for row in result]
        return data


    def __del__(self):
        """关闭数据库连接"""
        self.conn.close()

