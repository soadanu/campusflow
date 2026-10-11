"""Summary reports."""

from campusflow.tickets import PRIORITY_ORDER
from campusflow.workflow import STATUSES

#reports
def build_report(tickets):
    by_status = {status: 0 for status in STATUSES}
    by_priority = {priority: 0 for priority in PRIORITY_ORDER}
    for ticket in tickets:
        by_status[ticket["status"]] += 1
        by_priority[ticket["priority"]] += 1
    return {"total": len(tickets), "by_status": by_status, "by_priority": by_priority}


def format_report(report):
    lines = [f"Total tickets: {report['total']}", "By status:"]
    lines += [f"  {name}: {count}" for name, count in report["by_status"].items()]
    lines.append("By priority:")
    lines += [f"  {name}: {count}" for name, count in report["by_priority"].items()]
    return "\n".join(lines)
