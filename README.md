# CampusFlow

A command-line helpdesk ticket manager for Learn2Earn campus staff. It records support requests, calculates priority, assigns work, tracks status, and saves everything to JSON.

## Team
| Fellow | Role | Contribution |
|---|---|---|
| <Engineer A> | Creation, validation, priority engine | <summary> |
| <Engineer B> | Assignment, workflow, queue, reports | <summary> |

## Setup
Python 3.10 or newer. No third-party packages.

```
python main.py
```

Menu: 1 Create, 2 List, 3 View, 4 Assign, 5 Change status, 6 Reopen, 7 Work queue, 8 Report, 9 Exit.

## Tests
```
python -m unittest discover -s tests -v
```
Covers priority rules and boundaries, validation, ID generation, assignment, status transitions, reopening, queue ordering, reports, and JSON round-trip including corrupted files.

## Rules
Priority (first match wins):
1. high urgency AND 10+ affected users: critical
2. high urgency OR 10+ affected users: high
3. medium urgency OR 3+ affected users: medium
4. otherwise: low

Status: open -> in_progress -> resolved. A ticket must be assigned before it can start. A resolved ticket is locked until reopened (resolved -> open).

## Data
Tickets are saved to `data/tickets.json` (ignored by Git). To start fresh, delete that file. If the file is corrupted, the app shows an error and exits without changing it.

## Reviewed pull requests
- Engineer A PR: <link>
- Engineer B PR: <link>

## Known limitations
- Single user, no locking if two copies run at once.
- Staff names are free text.
- Tickets cannot be edited or deleted after creation.
