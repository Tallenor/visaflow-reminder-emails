import brevo_python as brevo
from src import BREVO_EMAIL_API_KEY
from src.utils import safe_get, setup_logger
from brevo_python.rest import ApiException

logger = setup_logger(__name__)

# Configuration
config = brevo.Configuration()
config.api_key["api-key"] = BREVO_EMAIL_API_KEY

# API instance
api_instance = brevo.TransactionalEmailsApi(brevo.ApiClient(config))

# Ids of the templates mapped to remaining number of months
templates = {"visa": {"1": 20, "2": 21, "3": 22}, "rp": {"1": 23, "2": 24, "3": 25}}


def send_visa_reminder_email(recipient: dict, for_month_remaining: str) -> bool:
    try:
        if for_month_remaining not in templates["visa"]:
            logger.error("Invalid key for month remaining")
            raise KeyError("Invalid key for month remaining")

        template_id = safe_get(templates, f"visa.{for_month_remaining}")
        name, email = recipient.get("name"), recipient.get("email")

        if not email or email == "":
            logger.error("Invalid email")
            raise ValueError("Invalid email")

        # Create email instance
        email_instance = brevo.SendSmtpEmail(
            template_id=template_id,
            to=[{"name": name, "email": email}],
        )

        # Send email
        response = api_instance.send_transac_email(email_instance)
        if response:
            msg = f"Visa Reminder email sent to {name} at `{email}` for {"months" if for_month_remaining > 1 else "month"} remaining =>  `{for_month_remaining}`"
            logger.info(msg)
            return True
        return False
    except ApiException as e:
        logger.error(f"An API error occurred while sending the email:\n{e}")

    except Exception as e:
        logger.error(f"An error occurred while sending the email:\n{e}")


def send_rp_reminder_email(recipient: dict, for_month_remaining: str) -> bool:
    try:
        if for_month_remaining not in templates["rp"]:
            logger.error("Invalid key for month remaining")
            raise KeyError("Invalid key for month remaining")

        template_id = safe_get(templates, f"rp.{for_month_remaining}")
        name, email = recipient.get("name"), recipient.get("email")

        if not email or email == "":
            logger.error("Invalid email")
            raise ValueError("Invalid email")

        # Create email instance
        email_instance = brevo.SendSmtpEmail(
            template_id=template_id,
            to=[{"name": name, "email": email}],
        )

        # Send email
        response = api_instance.send_transac_email(email_instance)
        if response:
            msg = f"RP Reminder email sent to {name} at `{email}` for {"months" if for_month_remaining > 1 else "month"} remaining => `{for_month_remaining}`"
            logger.info(msg)
            return True
        return False
    except ApiException as e:
        logger.error(f"An API error occurred while sending the email:\n{e}")

    except Exception as e:
        logger.error(f"An error occurred while sending the email:\n{e}")
