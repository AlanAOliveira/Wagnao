import sqlite3
from typing import Any, Dict, List, Tuple, Optional

class SQLiteCRUD:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def execute(self, sql: str, params: Tuple[Any, ...] = ()) -> sqlite3.Cursor:
        cur = self.conn.cursor()
        cur.execute(sql, params)
        self.conn.commit()
        return cur

    def create_table(self, table_name: str, schema: str):
        self.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})")

    def insert(self, table_name: str, data: Dict[str, Any]) -> int:
        keys = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        values = tuple(data.values())
        cur = self.execute(f"INSERT INTO {table_name} ({keys}) VALUES ({placeholders})", values)
        return cur.lastrowid

    def read_one(self, table_name: str, where: str = "1=1", params: Tuple[Any, ...] = ()) -> Optional[Dict]:
        cur = self.execute(f"SELECT * FROM {table_name} WHERE {where} LIMIT 1", params)
        row = cur.fetchone()
        return dict(row) if row else None

    def read_all(self, table_name: str, where: str = "1=1", params: Tuple[Any, ...] = ()) -> List[Dict]:
        cur = self.execute(f"SELECT * FROM {table_name} WHERE {where}", params)
        rows = cur.fetchall()
        return [dict(r) for r in rows]

    def update(self, table_name: str, data: Dict[str, Any], where: str, params: Tuple[Any, ...] = ()) -> int:
        set_clause = ", ".join(f"{k}=?" for k in data.keys())
        values = tuple(data.values()) + params
        cur = self.execute(f"UPDATE {table_name} SET {set_clause} WHERE {where}", values)
        return cur.rowcount

    def delete(self, table_name: str, where: str, params: Tuple[Any, ...] = ()) -> int:
        cur = self.execute(f"DELETE FROM {table_name} WHERE {where}", params)
        return cur.rowcount

    def close(self):
        self.cursor.close()
        self.conn.close()


# instance for CRUD usage
db = SQLiteCRUD("app.db")

