# Alpha Solver Quickstart

This guide gets you running Alpha Solver in under five minutes.

## 1. Clone & Install
```bash
git clone https://example.com/alpha-solver.git
cd alpha-solver
pip install -r requirements.txt
```

## 2. Configure Environment
Copy the example environment and edit as needed:
```bash
cp .env.example .env
```

## 3. Validate Setup
Run the environment checker and tests:
```bash
make env-check
make test
```

## 4. Start the Server
```bash
make run
```
The API is now available at [http://localhost:8000](http://localhost:8000).

Codespaces users can run the same commands in the integrated terminal.
