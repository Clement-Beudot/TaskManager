from datetime import datetime, timedelta

DATE_MAPPINGS = {
    "tomorrow": (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y"),
    "monday": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 0) % 7 or 7)).strftime("%d-%m-%Y"),
    "tuesday": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 1) % 7 or 7)).strftime("%d-%m-%Y"),
    "wednesday": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 2) % 7 or 7)).strftime("%d-%m-%Y"),
    "thursday": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 3) % 7 or 7)).strftime("%d-%m-%Y"),
    "friday": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 4) % 7 or 7)).strftime("%d-%m-%Y"),
    "saturday": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 5) % 7 or 7)).strftime("%d-%m-%Y"),
    "sunday": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 6) % 7 or 7)).strftime("%d-%m-%Y"),

    "demain": (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y"),
    "lundi": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 0) % 7 or 7)).strftime("%d-%m-%Y"),
    "mardi": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 1) % 7 or 7)).strftime("%d-%m-%Y"),
    "mercredi": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 2) % 7 or 7)).strftime("%d-%m-%Y"),
    "jeudi": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 3) % 7 or 7)).strftime("%d-%m-%Y"),
    "vendredi": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 4) % 7 or 7)).strftime("%d-%m-%Y"),
    "samedi": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 5) % 7 or 7)).strftime("%d-%m-%Y"),
    "dimanche": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 6) % 7 or 7)).strftime("%d-%m-%Y"),

}