import unittest

from campusflow.tickets import create_ticket
from campusflow.workflow import (
    assign_ticket, change_status, reopen_ticket, work_queue,
)


def make_tickets():
    tickets = []
    create_ticket(tickets, "Wi-Fi down", "Network", "high", 15)   # T001 critical
    create_ticket(tickets, "Slow laptop", "Hardware", "low", 1)    # T002 low
    create_ticket(tickets, "App crash", "Software", "medium", 1)   # T003 medium
    create_ticket(tickets, "Projector", "Hardware", "high", 2)     # T004 high
    create_ticket(tickets, "Printer", "Hardware", "medium", 1)     # T005 medium
    return tickets


class AssignmentTests(unittest.TestCase):
    def test_assign_sets_name(self):
        tickets = make_tickets()
        assign_ticket(tickets, "t001", "  Ada ")
        self.assertEqual(tickets[0]["assigned_to"], "Ada")

    def test_unknown_id_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket(make_tickets(), "T999", "Ada")

    def test_blank_name_rejected(self):
        tickets = make_tickets()
        with self.assertRaises(ValueError):
            assign_ticket(tickets, "T001", "  ")
        self.assertIsNone(tickets[0]["assigned_to"])


class StatusTests(unittest.TestCase):
    def test_unassigned_cannot_start(self):
        tickets = make_tickets()
        with self.assertRaises(ValueError):
            change_status(tickets, "T001", "in_progress")
        self.assertEqual(tickets[0]["status"], "open")

    def test_full_lifecycle(self):
        tickets = make_tickets()
        assign_ticket(tickets, "T001", "Ada")
        change_status(tickets, "T001", "in_progress")
        self.assertEqual(tickets[0]["status"], "in_progress")
        change_status(tickets, "T001", "resolved")
        self.assertEqual(tickets[0]["status"], "resolved")

    def test_cannot_skip_to_resolved(self):
        tickets = make_tickets()
        assign_ticket(tickets, "T001", "Ada")
        with self.assertRaises(ValueError):
            change_status(tickets, "T001", "resolved")

    def test_resolved_is_locked_until_reopened(self):
        tickets = make_tickets()
        assign_ticket(tickets, "T001", "Ada")
        change_status(tickets, "T001", "in_progress")
        change_status(tickets, "T001", "resolved")
        with self.assertRaises(ValueError):
            assign_ticket(tickets, "T001", "Bola")
        with self.assertRaises(ValueError):
            change_status(tickets, "T001", "open")
        reopen_ticket(tickets, "T001")
        self.assertEqual(tickets[0]["status"], "open")
        assign_ticket(tickets, "T001", "Bola")
        self.assertEqual(tickets[0]["assigned_to"], "Bola")

    def test_reopen_requires_resolved(self):
        with self.assertRaises(ValueError):
            reopen_ticket(make_tickets(), "T001")


class QueueTests(unittest.TestCase):
    def test_sorted_by_priority_then_numeric_id(self):
        ids = [t["id"] for t in work_queue(make_tickets())]
        self.assertEqual(ids, ["T001", "T004", "T003", "T005", "T002"])

    def test_excludes_non_open_tickets(self):
        tickets = make_tickets()
        assign_ticket(tickets, "T001", "Ada")
        change_status(tickets, "T001", "in_progress")
        self.assertNotIn("T001", [t["id"] for t in work_queue(tickets)])

    def test_ids_compare_numerically_not_as_text(self):
        tickets = [
            {"id": "T010", "priority": "low", "status": "open"},
            {"id": "T002", "priority": "low", "status": "open"},
        ]
        self.assertEqual([t["id"] for t in work_queue(tickets)], ["T002", "T010"])


if __name__ == "__main__":
    unittest.main()
