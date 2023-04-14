import asyncio
from aiogram import Bot, Dispatcher
from configs import config
from handlers import r1,r2,r3
from commands import set_commands
from middlewares import DbSessionMiddleware
from aiogram.fsm.storage.memory import MemoryStorage

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import logging

async def main():
    logging.basicConfig(level=logging.DEBUG)

    engine = create_async_engine(url=config.db_url, echo=False)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(config.bot_token.get_secret_value())
    dp = Dispatcher(storage=MemoryStorage())

    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))

    dp.include_routers(r1,r2,r3)
    
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())