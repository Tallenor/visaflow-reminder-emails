from time import sleep
from datetime import datetime, timezone, time
from dateutil.relativedelta import relativedelta
from scheduler import Scheduler
from src.utils import setup_logger
from src.database import get_all_reminders
from src.brevo import send_visa_reminder_email, send_rp_reminder_email

logger = setup_logger(__name__)


def calculate_months_left(target_date_str: str) -> int:
    """
    Calculate the number of months until the target date from today.

    Args:
        target_date_str: Target date string in 'YYYY-MM-DD' format.

    Returns:
        int: The number of months until the target date from today.
            0 if an invalid date format is provided or if the target date is not
            exactly 1, 2, or 3 months in the future.
            -1 if the target date is not in the future.
    """
    today = datetime.now(timezone.utc).date()

    try:
        # Parse the target date (assuming it is in 'YYYY-MM-DD' format)
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()
    except ValueError as e:
        logger.error(f"Error while parsing the target date: {e}")
        logger.error(
            f"Invalid date format provided: {target_date_str}\nExpected format: YYYY-MM-DD"
        )
        return 0

    # Ensure the target date is in the future.
    if target_date <= today:
        logger.error("Target date must be in the future.")
        return -1

    # Check for exact 1, 2, or 3 month offsets.
    for months in [1, 2, 3]:
        candidate_date = today + relativedelta(months=+months)
        if candidate_date == target_date:
            return months

    return 0


def task_one():
    logger.info("Running task one...")
    reminders = get_all_reminders()
    if not reminders:
        logger.info("No reminders found.")
        return

    visa_reminders, rp_reminders = (
        reminders["visa_reminders"],
        reminders["rp_reminders"],
    )

    logger.info("Processing reminders...")
    logger.info(f"Visa Reminders: {len(visa_reminders)}")
    for vr in visa_reminders:
        recipient = {"name": vr["firstName"], "email": vr["email"]}
        date_of_appointment = vr["data"]["dateOfAppointment"]
        # date_of_appointment = "2025-07-05" #! for testing
        match calculate_months_left(date_of_appointment):
            case 1:
                send_visa_reminder_email(recipient, "1")
            case 2:
                send_visa_reminder_email(recipient, "2")
            case 3:
                send_visa_reminder_email(recipient, "3")
            case _:
                continue

    logger.info("Visa reminders completed...")

    logger.info(f"RP Reminders: {len(rp_reminders)}")
    for rr in rp_reminders:
        recipient = {"name": rr["firstName"], "email": rr["email"]}
        date_of_expiration = rr["data"]["dateOfExpiration"]
        # date_of_expiration = "2025-06-06"  #! for testing
        match calculate_months_left(date_of_expiration):
            case 1:
                send_rp_reminder_email(recipient, "1")
            case 2:
                send_rp_reminder_email(recipient, "2")
            case 3:
                send_rp_reminder_email(recipient, "3")
            case _:
                continue

    logger.info("RP reminders completed...")
    logger.info("Task one completed.")


def run_scheduler():
    """
    Initializes and runs the scheduler that executes tasks function daily at 8 AM.

    The scheduler will continuously run and manage job execution, ensuring that
    tasks is triggered at the specified time every day.
    """
    try:
        schedule = Scheduler()
        scheduled_time = time(hour=8, minute=0)

        # every day at 8am, run task one
        schedule.daily(timing=scheduled_time, handle=task_one)
        # schedule.daily(timing=time(hour=8), handle=task_one) #! for testing

        # start the scheduler
        logger.info("Starting scheduler...")
        logger.info("Scheduler is running...")

        last_run_date = None
        while True:
            current_time = datetime.now()
            current_date = current_time.date()

            # Check if it's past scheduled time and hasn't been run today
            if current_time.time() >= scheduled_time and current_date != last_run_date:
                logger.info(f"Last run date: {last_run_date}")
                schedule.exec_jobs()
                last_run_date = current_date
                logger.info(f"Task completed for {current_date}")

            sleep(0.5)

        logger.info("Scheduler stopped.")
    except KeyboardInterrupt:
        logger.info("\nScheduler stopped by user.")
    except Exception as e:
        logger.info(f"An error occurred: {e}")
