import unittest

from campusflow.tickets import calculate_priority, create_ticket, next_ticket_id


class PriorityTests(unittest.TestCase):
    def test_high_urgency_many_users_is_critical(self):
        self.assertEqual(calculate_priority("high", 12), "critical")

    def test_high_urgency_boundary_ten_users_is_critical(self):
        self.assertEqual(calculate_priority("high", 10), "critical")

    def test_high_urgency_few_users_is_high(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_low_urgency_ten_users_is_high(self):
        self.assertEqual(calculate_priority("low", 10), "high")

    def test_low_urgency_four_users_is_medium(self):
        self.assertEqual(calculate_priority("low", 4), "medium")

    def test_medium_urgency_one_user_is_medium(self):
        self.assertEqual(calculate_priority("medium", 1), "medium")

    def test_boundary_three_users_is_medium_two_is_low(self):
        self.assertEqual(calculate_priority("low", 3), "medium")
        self.assertEqual(calculate_priority("low", 2), "low")

    def test_low_urgency_one_user_is_low(self):
        self.assertEqual(calculate_priority("low", 1), "low")


class CreateTicketTests(unittest.TestCase):
    def test_creates_ticket_with_expected_fields(self):
        tickets = []
        t = create_ticket(tickets, "Campus Wi-Fi is down", "network", "HIGH", "15")
        self.assertEqual(
            t,
            {
                "id": "T001",
                "title": "Campus Wi-Fi is down",
                "category": "Network",
                "urgency": "high",
                "affected_users": 15,
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
            },
        )
        self.assertEqual(tickets, [t])

    def test_ids_increment(self):
        tickets = []
        create_ticket(tickets, "A", "Other", "low", 1)
        create_ticket(tickets, "B", "Other", "low", 1)
        self.assertEqual([t["id"] for t in tickets], ["T001", "T002"])

    def test_next_id_after_existing_tickets(self):
        self.assertEqual(next_ticket_id([{"id": "T001"}, {"id": "T007"}]), "T008")

    def test_rejects_invalid_affected_users_without_changing_tickets(self):
        for bad in (0, -3, 2.5, "2.5", "abc", "", None, True):
            tickets = []
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    create_ticket(tickets, "Title", "Other", "low", bad)
                self.assertEqual(tickets, [])

    def test_rejects_blank_title(self):
        with self.assertRaises(ValueError):
            create_ticket([], "   ", "Other", "low", 1)

    def test_rejects_invalid_category_and_urgency(self):
        with self.assertRaises(ValueError):
            create_ticket([], "T", "Plumbing", "low", 1)
        with self.assertRaises(ValueError):
            create_ticket([], "T", "Other", "urgent", 1)


if __name__ == "__main__":
    unittest.main()
