from loader import dp, bot
import asyncio

if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
