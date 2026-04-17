import asyncio

from dotenv import load_dotenv

from src.ait_changer import  generate_ne_names, tryin
from src.better_changer import update_testcase
from src.eros import generate_date


async def main():
    load_dotenv()
    await tryin()

async def run_testcase():
    systemprompt = "Write a bachelorsthesis about the import of bananas."
    await update_testcase(systemprompt)

if __name__ == "__main__":
    asyncio.run(run_testcase())
    