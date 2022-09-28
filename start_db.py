import asyncio
from energy_gym_server.models.database import Base, engine


async def start_base():
    async with engine.begin() as conn:
        print('Создание таблиц в БД...')
        try:
            await conn.run_sync(Base.metadata.create_all)
        except Exception as e:
            print(f'Ошибка создания таблиц: {e}')
        else:
            print('Таблицы успешно созданы')

if __name__ == '__main__':
    asyncio.run(start_base())
