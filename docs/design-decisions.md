# Design Decisions

Agreed by: <Engineer A> and <Engineer B>

## Ownership
- Engineer A: <files/features>
- Engineer B: <files/features>

## Data structure
Tickets are stored in a list of dictionaries. The list is passed to every function as the first argument.

## Error handling
Business-logic functions raise `ValueError` with a clear message. The CLI catches it and prints it. Invalid input never changes the ticket list (validate first, then modify).

## Return values
`create_ticket`, `assign_ticket`, `change_status`, `reopen_ticket` return the affected ticket dictionary.

## Persistence
`campusflow/storage.py` owns loading and saving. Missing file = fresh start. Malformed file = `StorageError`, program exits without touching the file.

## Testing without input()
Logic functions take plain arguments; only `main.py` calls `input()`.

## Other decisions
- <add yours>
