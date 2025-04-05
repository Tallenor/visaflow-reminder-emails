from xata.client import XataClient
from src import XATA_API_KEY, DB_URL
from src.utils import safe_get


# fmt: off
client = XataClient(api_key=XATA_API_KEY, db_url=DB_URL)
# fmt: on


def get_all_reminders() -> list | None:
    result = {
        "visa_reminders": [],
        "rp_reminders": [],  # residence permit reminders
    }

    # Construct payload
    payload = {
        "columns": ["data", "path.user.email", "path.user.firstName"],
        "sort": {"data": "asc"},
        "filter": {"$exists": "data"},
    }

    # Query DB
    response = client.data().query("UserJourney", payload)

    # Process response
    filtered_records = []
    if not response.is_success():
        return None
    records = response.get("records")
    if records:
        for record in records:
            obj = {
                "email": safe_get(record, "path.user.email"),
                "firstName": safe_get(record, "path.user.firstName"),
                "data": safe_get(record, "data"),
            }

            filtered_records.append(obj)

    # Group by type
    for r in filtered_records:
        if "dateOfIssuance" in r["data"] and "dateOfExpiration" in r["data"]:
            result["rp_reminders"].append(r)
        if "dateOfAppointment" in r["data"]:
            result["visa_reminders"].append(r)
    return result


# print(get_all_reminders()) # TODO: remove this
