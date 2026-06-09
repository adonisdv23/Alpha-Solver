# Non-execution proof

The wrapper does not execute proposed commands. It only passes proposed command strings or argv to deterministic classification and gate helpers.

Tests prove non-execution by proposing sentinel-creating command strings and dangerous command examples, then asserting the sentinel files do not exist after the wrapper returns. Tests also monkeypatch `subprocess.run` to raise if invoked while forbidden provider/API/browser/deployment/billing/credential/Google Sheets/evidence-promotion examples are classified.
