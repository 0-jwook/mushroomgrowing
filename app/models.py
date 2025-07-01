from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

mushrooms = Table(
    "mushrooms",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(255)),  # 길이 지정 필수
    Column("level", Integer, default=1),
    Column("success_rate", Integer, default=80),  # 강화 성공 확률
)
