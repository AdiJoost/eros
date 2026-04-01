import asyncio

from dotenv import load_dotenv

from src.ait_changer import generate_date, generate_ne_names


async def main():
    load_dotenv()
    await generate_ne_names()


if __name__ == "__main__":
    asyncio.run(main())