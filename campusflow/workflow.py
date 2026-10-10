"""Assignment, status lifecycle and the work queue."""

from campusflow.tickets import PRIORITY_ORDER, find_ticket, ticket_number

STATUSES = ("open", "in_progress", "resolved")
ALLOWED_TRANSITIONS = {("open", "in_progress"), ("in_progress", "resolved")}


def assign_ticket(tickets, ticket_id, staff_name):
    ticket = find_ticket(tickets, ticket_id)
    name = staff_name.strip() if isinstance(staff_name, str) else ""
    if not name:
        raise ValueError("Staff name must not be blank.")
    if ticket["status"] == "resolved":
        raise ValueError("Resolved tickets must be reopened before they can be changed.")
    ticket["assigned_to"] = name
    return ticket


def change_status(tickets, ticket_id, new_status):
    ticket = find_ticket(tickets, ticket_id)
    new_status = str(new_status).strip().lower()
    if new_status not in STATUSES:
        raise ValueError("Status must be one of: " + ", ".join(STATUSES) + ".")

    current = ticket["status"]
    if current == "resolved":
        raise ValueError("Resolved tickets must be reopened before they can be changed.")
    if (current, new_status) not in ALLOWED_TRANSITIONS:
        raise ValueError(f"Cannot move a ticket from {current} to {new_status}.")
    if new_status == "in_progress" and not ticket["assigned_to"]:
        raise ValueError("Assign the ticket to someone before starting work on it.")

    ticket["status"] = new_status
    return ticket


def reopen_ticket(tickets, ticket_id):
    ticket = find_ticket(tickets, ticket_id)
    if ticket["status"] != "resolved":
        raise ValueError("Only resolved tickets can be reopened.")
    ticket["status"] = "open"
    return ticket


def work_queue(tickets):
    """Open tickets: critical -> low, ties broken by the earlier numeric ID."""
    open_tickets = [t for t in tickets if t["status"] == "open"]
    return sorted(
        open_tickets,
        key=lambda t: (PRIORITY_ORDER.index(t["priority"]), ticket_number(t["id"])),
    )
