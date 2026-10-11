"""Ticket creation, validation and the priority engine."""

CATEGORIES = {
    "network": "Network",
    "hardware": "Hardware",
    "software": "Software",
    "other": "Other",
}
URGENCIES = ("low", "medium", "high")
PRIORITY_ORDER = ("critical", "high", "medium", "low")


def normalize_title(title):
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Title must not be blank.")
    return title.strip()


def normalize_category(category):
    key = str(category).strip().lower()
    if key not in CATEGORIES:
        raise ValueError("Category must be one of: " + ", ".join(CATEGORIES.values()) + ".")
    return CATEGORIES[key]


def normalize_urgency(urgency):
    value = str(urgency).strip().lower()
    if value not in URGENCIES:
        raise ValueError("Urgency must be one of: " + ", ".join(URGENCIES) + ".")
    return value


def parse_affected_users(value):
    """Accept a positive whole number (int, or text made only of digits)."""
    if isinstance(value, bool):
        raise ValueError("Affected users must be a positive whole number.")
    if isinstance(value, int):
        number = value
    elif isinstance(value, str):
        text = value.strip()
        if not (text.isascii() and text.isdigit()):
            raise ValueError("Affected users must be a positive whole number.")
        number = int(text)
    else:
        raise ValueError("Affected users must be a positive whole number.")
    if number < 1:
        raise ValueError("Affected users must be at least 1.")
    return number


def calculate_priority(urgency, affected_users):
    """Apply the rules in order; the first match wins."""
    urgency = normalize_urgency(urgency)
    users = parse_affected_users(affected_users)

    if urgency == "high" and users >= 10:
        return "critical"
    if urgency == "high" or users >= 10:
        return "high"
    if urgency == "medium" or users >= 3:
        return "medium"
    return "low"


def ticket_number(ticket_id):
    return int(ticket_id[1:])


def next_ticket_id(tickets):
    """Highest existing number + 1, so IDs stay unique after a reload."""
    highest = max((ticket_number(t["id"]) for t in tickets), default=0)
    return f"T{highest + 1:03d}"


def find_ticket(tickets, ticket_id):
    wanted = str(ticket_id).strip().upper()
    for ticket in tickets:
        if ticket["id"] == wanted:
            return ticket
    raise ValueError(f"Unknown ticket ID: {ticket_id!r}.")


def create_ticket(tickets, title, category, urgency, affected_users):
    """Validate everything first, then append. Invalid input never changes `tickets`."""
    title = normalize_title(title)
    category = normalize_category(category)
    urgency = normalize_urgency(urgency)
    users = parse_affected_users(affected_users)

    ticket = {
        "id": next_ticket_id(tickets),
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": users,
        "priority": calculate_priority(urgency, users),
        "status": "open",
        "assigned_to": None,
    }
    tickets.append(ticket)
    return ticket
