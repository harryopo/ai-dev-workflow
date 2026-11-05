"""
Desktop Todo business adapter for PySide6.

Mirrors the shared TodoService contract used by the Web/Mobile templates:
- add_item, toggle_item, delete_item for business operations
- get_items, get_stats for querying state
- SQLite persistence out of the box
"""

import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class TodoItem:
    id: str
    name: str
    completed: bool


@dataclass
class TodoStats:
    total: int
    completed: int
    pending: int


class TodoAdapter:
    """SQLite-backed Todo business logic for the desktop template."""

    def __init__(self, db_path: str = "todos.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS todos (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    completed INTEGER DEFAULT 0
                )
                """
            )
            conn.commit()

    def get_items(self) -> List[TodoItem]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT id, name, completed FROM todos ORDER BY id DESC")
            return [
                TodoItem(
                    id=row["id"],
                    name=row["name"],
                    completed=bool(row["completed"]),
                )
                for row in cursor.fetchall()
            ]

    def add_item(self, name: str) -> TodoItem:
        trimmed = name.strip()
        if not trimmed:
            raise ValueError("项目名称不能为空")

        item = TodoItem(
            id=str(int(time.time() * 1000)),
            name=trimmed,
            completed=False,
        )
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO todos (id, name, completed) VALUES (?, ?, ?)",
                (item.id, item.name, 0),
            )
            conn.commit()
        return item

    def toggle_item(self, item_id: str) -> None:
        item = self._find_by_id(item_id)
        if item is None:
            return
        self._update(item_id, {"completed": not item.completed})

    def delete_item(self, item_id: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM todos WHERE id = ?", (item_id,))
            conn.commit()

    def get_stats(self, items: Optional[List[TodoItem]] = None) -> TodoStats:
        if items is None:
            items = self.get_items()
        total = len(items)
        completed = sum(1 for item in items if item.completed)
        return TodoStats(total=total, completed=completed, pending=total - completed)

    def _find_by_id(self, item_id: str) -> Optional[TodoItem]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT id, name, completed FROM todos WHERE id = ?", (item_id,)
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return TodoItem(
                id=row["id"],
                name=row["name"],
                completed=bool(row["completed"]),
            )

    def _update(self, item_id: str, updates: dict) -> None:
        set_clauses = []
        params: List = []

        if "completed" in updates:
            set_clauses.append("completed = ?")
            params.append(1 if updates["completed"] else 0)

        if not set_clauses:
            return

        params.append(item_id)
        sql = f"UPDATE todos SET {', '.join(set_clauses)} WHERE id = ?"
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(sql, params)
            conn.commit()
