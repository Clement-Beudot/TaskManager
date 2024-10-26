from datetime import datetime, timedelta

DATE_MAPPINGS = {
    "tomorrow": (datetime.now() + timedelta(days=1)),
    "monday": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 0) % 7 or 7)),
    "tuesday": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 1) % 7 or 7)),
    "wednesday": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 2) % 7 or 7)),
    "thursday": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 3) % 7 or 7)),
    "friday": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 4) % 7 or 7)),
    "saturday": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 5) % 7 or 7)),
    "sunday": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 6) % 7 or 7)),

    "demain": (datetime.now() + timedelta(days=1)),
    "lundi": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 0) % 7 or 7)),
    "mardi": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 1) % 7 or 7)),
    "mercredi": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 2) % 7 or 7)),
    "jeudi": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 3) % 7 or 7)),
    "vendredi": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 4) % 7 or 7)),
    "samedi": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 5) % 7 or 7)),
    "dimanche": (datetime.now() + timedelta(days=(7 - datetime.now().weekday() + 6) % 7 or 7)),

}