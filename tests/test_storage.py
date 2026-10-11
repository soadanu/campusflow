import os
import tempfile
import unittest

from campusflow.reports import build_report
from campusflow.storage import StorageError, load_tickets, save_tickets
from campusflow.tickets import create_ticket


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = os.path.join(self.folder.name, "data", "tickets.json")

    def test_missing_file_gives_empty_list(self):
        self.assertEqual(load_tickets(self.path), [])

    def test_round_trip_preserves_tickets(self):
        tickets = []
        create_ticket(tickets, "Wi-Fi down", "Network", "high", 15)
        create_ticket(tickets, "Laptop", "Hardware", "low", 1)
        save_tickets(tickets, self.path)
        self.assertEqual(load_tickets(self.path), tickets)

    def test_ids_stay_unique_after_reload(self):
        tickets = []
        create_ticket(tickets, "A", "Other", "low", 1)
        create_ticket(tickets, "B", "Other", "low", 1)
        save_tickets(tickets, self.path)
        reloaded = load_tickets(self.path)
        new = create_ticket(reloaded, "C", "Other", "low", 1)
        self.assertEqual(new["id"], "T003")
        self.assertEqual(len({t["id"] for t in reloaded}), 3)

    def test_corrupted_json_raises_and_keeps_file(self):
        os.makedirs(os.path.dirname(self.path))
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("{not valid json")
        with self.assertRaises(StorageError):
            load_tickets(self.path)
        with open(self.path, encoding="utf-8") as f:
            self.assertEqual(f.read(), "{not valid json")

    def test_wrong_shape_raises(self):
        os.makedirs(os.path.dirname(self.path))
        with open(self.path, "w", encoding="utf-8") as f:
            f.write('{"id": "T001"}')
        with self.assertRaises(StorageError):
            load_tickets(self.path)


class ReportTests(unittest.TestCase):
    def test_empty_report(self):
        report = build_report([])
        self.assertEqual(report["total"], 0)
        self.assertEqual(sum(report["by_status"].values()), 0)
        self.assertEqual(sum(report["by_priority"].values()), 0)

    def test_report_counts(self):
        tickets = []
        create_ticket(tickets, "A", "Other", "high", 15)
        create_ticket(tickets, "B", "Other", "low", 1)
        create_ticket(tickets, "C", "Other", "low", 1)
        report = build_report(tickets)
        self.assertEqual(report["total"], 3)
        self.assertEqual(report["by_status"]["open"], 3)
        self.assertEqual(report["by_priority"]["critical"], 1)
        self.assertEqual(report["by_priority"]["low"], 2)


if __name__ == "__main__":
    unittest.main()
