import asyncio

from dotenv import load_dotenv

from src.ait_changer import  generate_ne_names, tryin
from src.eros import generate_date


async def main():
    load_dotenv()
    await tryin()


if __name__ == "__main__":
    asyncio.run(main())