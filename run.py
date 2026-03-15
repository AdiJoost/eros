from dotenv import load_dotenv

from src.coder import chat
from src.eros import generate_date

def main():
    load_dotenv()
    generate_date()


if __name__ == "__main__":
    main()