from sqlalchemy import select, insert, delete, update, text
from .models import mushrooms
from .db import engine
import random

def get_all_mushrooms():  # ✅ 인자 없이
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, name, level FROM mushrooms"))
        return [dict(row) for row in result]

def get_mushroom_by_id(m_id: int):
    with engine.begin() as conn:
        # result = conn.execute(select(mushrooms)).fetchall()
        result = conn.execute(
            text("SELECT * FROM mushrooms WHERE id = :id"),
            {"id": m_id}
        ).fetchone()
        return result

def create_mushroom(name: str):
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO mushrooms (name, level, success_rate) VALUES (:name, :level, :rate)"),
            {"name": name, "level": 1, "rate": 80}
        )

def upgrade_mushroom(m_id: int) -> dict:
    with engine.begin() as conn:
        result = conn.execute(
            text("SELECT * FROM mushrooms WHERE id = :id"),
            {"id": m_id}
        ).fetchone()

        if not result:
            return {"success": False, "deleted": False, "level_change": 0}

        level = result.level
        rate = result.success_rate

        roll = random.randint(1, 100)

        if roll <= rate:
            # ✅ 강화 성공
            new_level = level + 1
            new_rate = max(10, rate - 5)
            conn.execute(
                text("UPDATE mushrooms SET level = :level, success_rate = :rate WHERE id = :id"),
                { "level": new_level, "rate": new_rate, "id": m_id }
            )
            return {"broken": False, "deleted": False, "level_change": +1}
        else:
            # ❌ 강화 실패
            destroy_roll = random.randint(1, 100)
            if destroy_roll == 1:
                # 💥 1% 확률로 삭제
                conn.execute(
                    text("DELETE FROM mushrooms WHERE id = :id"),
                    {"id": m_id}
                )
                return {"broken": True, "deleted": True, "level_change": -level}
            else:
                # 📉 레벨 감소 (최소 1 유지)
                new_level = max(1, level - 1)
                if result.success_rate == 80:
                    new_rate = max(10, rate)
                else:
                    new_rate = max(10, rate + 5)
                    conn.execute(
                    text("UPDATE mushrooms SET level = :level, success_rate = :rate WHERE id = :id"),
                    {"level": new_level, "rate": new_rate, "id": m_id}
                )
                return {"broken": False, "deleted": False, "level_change": -1}

def delete_mushroom(m_id: int) -> bool:
    with engine.connect() as conn:
        result = conn.execute(
            text("DELETE FROM mushrooms WHERE id = :id"),
            {"id": m_id}
        )
        return result.rowcount > 0
