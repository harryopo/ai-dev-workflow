import sqlite3
from pathlib import Path
from typing import List, Tuple, Optional


class Database:
    """SQLite 数据库操作封装"""
    
    def __init__(self, db_path: str = "data/app.db"):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
    
    def get_connection(self):
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def execute(self, sql: str, params: tuple = None) -> List[dict]:
        """执行 SQL 语句并返回结果"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            conn.commit()
            return [dict(row) for row in cursor.fetchall()]
    
    def insert(self, table: str, data: dict) -> int:
        """插入数据"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, tuple(data.values()))
            conn.commit()
            return cursor.lastrowid
    
    def update(self, table: str, data: dict, where: str, where_params: tuple) -> int:
        """更新数据"""
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
        params = tuple(data.values()) + where_params
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return cursor.rowcount
    
    def delete(self, table: str, where: str, params: tuple) -> int:
        """删除数据"""
        sql = f"DELETE FROM {table} WHERE {where}"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return cursor.rowcount
    
    def select(self, table: str, where: str = None, params: tuple = None, 
               order_by: str = None, limit: int = None) -> List[dict]:
        """查询数据"""
        sql = f"SELECT * FROM {table}"
        if where:
            sql += f" WHERE {where}"
        if order_by:
            sql += f" ORDER BY {order_by}"
        if limit:
            sql += f" LIMIT {limit}"
        
        return self.execute(sql, params)
    
    def init_table(self, create_sql: str):
        """初始化数据表"""
        self.execute(create_sql)
