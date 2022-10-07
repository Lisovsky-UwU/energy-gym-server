import asyncio
from sqlalchemy import text
from energy_gym_server.models.database import Base, engine, User
from energy_gym_server.models import UserRoles


async def start_base():
    async with engine.begin() as conn:
        print('Создание таблиц в БД...')
        try:
            await conn.run_sync(Base.metadata.create_all)
            await conn.execute(
                text(f"INSERT INTO {User.__tablename__} VALUES (-1, 'ADMIN', '-', 'hexReGON14', '{UserRoles.ADMIN.name}')")
            )
        except Exception as e:
            print(f'Ошибка создания таблиц: {e}')
        else:
            print('Таблицы успешно созданы')

if __name__ == '__main__':
    asyncio.run(start_base())
