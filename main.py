from src.scheduler import run_scheduler
from src.utils import setup_logger

logger = setup_logger("main")


def main():
    try:
        run_scheduler()
    except KeyboardInterrupt:
        print("\nGoodbye.")
    except Exception:
        pass


if __name__ == "__main__":
    main()
