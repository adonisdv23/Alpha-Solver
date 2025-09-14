# Observability

The Alpha Solver CLI can record and replay reasoning sessions using the built-in
P3 observability components.

## Record a run

```bash
python alpha_solver_cli.py "2+2" --record --obs-stats
```

The solver writes events to a replay file and prints a JSON summary on the
second line, including the `session_id`.

## Replay a session

```bash
python alpha_solver_cli.py "2+2" --replay SESSION_ID
```

Replay verifies that the events and results match the recorded session.

## View stats without recording

```bash
python alpha_solver_cli.py "2+2" --obs-stats
```

Stats report the number of events logged and sessions recorded for the run.
