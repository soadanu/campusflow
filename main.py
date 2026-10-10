"""CampusFlow command-line interface."""

import sys

from campusflow import reports, storage, tickets, workflow

MENU = """
=== CampusFlow ===
1. Create ticket
2. List tickets
3. View ticket
4. Assign ticket
5. Change status (start / resolve)
6. Reopen ticket
7. Work queue
8. Report
9. Exit
"""


def show_ticket(t):
    print(
        f"{t['id']} | {t['title']} | {t['category']} | urgency: {t['urgency']} | "
        f"users: {t['affected_users']} | priority: {t['priority']} | "
        f"status: {t['status']} | assigned: {t['assigned_to'] or '-'}"
    )


def show_tickets(items):
    if not items:
        print("No tickets to show.")
    for t in items:
        show_ticket(t)


def save(items, path):
    storage.save_tickets(items, path)


def handle(choice, items, path):
    """Returns True if the data changed."""
    if choice == "1":
        t = tickets.create_ticket(
            items,
            input("Title: "),
            input("Category (Network/Hardware/Software/Other): "),
            input("Urgency (low/medium/high): "),
            input("Affected users: "),
        )
        print(f"Created {t['id']} with priority {t['priority']}.")
        return True
    if choice == "2":
        show_tickets(items)
    elif choice == "3":
        show_ticket(tickets.find_ticket(items, input("Ticket ID: ")))
    elif choice == "4":
        t = workflow.assign_ticket(items, input("Ticket ID: "), input("Assign to: "))
        print(f"{t['id']} assigned to {t['assigned_to']}.")
        return True
    elif choice == "5":
        t = workflow.change_status(items, input("Ticket ID: "), input("New status (in_progress/resolved): "))
        print(f"{t['id']} is now {t['status']}.")
        return True
    elif choice == "6":
        t = workflow.reopen_ticket(items, input("Ticket ID: "))
        print(f"{t['id']} reopened.")
        return True
    elif choice == "7":
        show_tickets(workflow.work_queue(items))
    elif choice == "8":
        print(reports.format_report(reports.build_report(items)))
    else:
        print("Please choose 1-9.")
    return False


def main(path=storage.DEFAULT_PATH):
    try:
        items = storage.load_tickets(path)
    except storage.StorageError as error:
        print(f"Error: {error}")
        print("Nothing was changed. Fix or move the file, then run again.")
        sys.exit(1)

    while True:
        print(MENU)
        choice = input("Choose: ").strip()
        if choice == "9":
            print("Goodbye.")
            break
        try:
            if handle(choice, items, path):
                save(items, path)
        except ValueError as error:
            print(f"Error: {error}")
        except OSError as error:
            print(f"Could not save: {error}")


if __name__ == "__main__":
    main()
