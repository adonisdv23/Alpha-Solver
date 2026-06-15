#!/usr/bin/env bash
set -euo pipefail

ENDPOINT_URL="http://127.0.0.1:11434/api/chat"
MODEL="gemma3:4b"
PROMPT="Synthetic local-only fixture: summarize this toy note in one sentence. Note: Ada put two blue blocks and one red block in a box."
VERDICT="FAILED_LOCAL_LAB_OTHER"
PREFLIGHT_RESULT="NOT_RUN"
COMMAND_EXIT_STATUS="NOT_RUN"
STDOUT_FILE=""
STDERR_FILE=""
OLLAMA_LIST_FILE=""

cleanup() {
  [[ -n "${STDOUT_FILE}" && -f "${STDOUT_FILE}" ]] && rm -f "${STDOUT_FILE}"
  [[ -n "${STDERR_FILE}" && -f "${STDERR_FILE}" ]] && rm -f "${STDERR_FILE}"
  [[ -n "${OLLAMA_LIST_FILE}" && -f "${OLLAMA_LIST_FILE}" ]] && rm -f "${OLLAMA_LIST_FILE}"
}
trap cleanup EXIT

print_non_claims() {
  cat <<'NONCLAIMS'
non-claims:
  - no local model quality claim
  - no Value Read success claim
  - no hosted provider validation claim
  - no production readiness claim
  - no public readiness claim
  - no benchmark success claim
  - no runtime readiness claim
  - no Alpha superiority claim
  - no /v1/solve, dashboard, public API, Google Sheets, provider-token, model-pull, model-install, registry-sweep, fallback-model, or tag-substitution claim
NONCLAIMS
}

print_result_block() {
  echo
  echo "=== LOCAL OLLAMA SINGLEPATH OPERATOR RESULT ==="
  echo "preflight exact model check result: ${PREFLIGHT_RESULT}"
  echo "command exit status: ${COMMAND_EXIT_STATUS}"
  echo "raw stdout:"
  if [[ -n "${STDOUT_FILE}" && -s "${STDOUT_FILE}" ]]; then
    cat "${STDOUT_FILE}"
  else
    echo "<empty>"
  fi
  echo "raw stderr if available:"
  if [[ -n "${STDERR_FILE}" && -s "${STDERR_FILE}" ]]; then
    cat "${STDERR_FILE}"
  else
    echo "<empty>"
  fi
  echo "operator verdict: ${VERDICT}"
  print_non_claims
}

echo "=== ALPHA SOLVER LOCAL OLLAMA SINGLEPATH OPERATOR HELPER ==="
echo "Evidence boundary: operator-local smoke helper only."
echo "Run this only on the same local machine where Ollama is already installed and serving ${ENDPOINT_URL}."
echo "This script does not run ollama pull, install models, call hosted providers, use provider tokens, access credentials, expose /v1/solve, expose dashboard/public API behavior, mutate Google Sheets, sweep registries, use fallback models, or substitute model tags."
echo "Exact required first-column ollama model tag: ${MODEL}"
echo

STDOUT_FILE="$(mktemp)"
STDERR_FILE="$(mktemp)"
OLLAMA_LIST_FILE="$(mktemp)"

if ollama list >"${OLLAMA_LIST_FILE}" 2>"${STDERR_FILE}" && awk 'NR > 1 {print $1}' "${OLLAMA_LIST_FILE}" | grep -Fxq "${MODEL}"; then
  PREFLIGHT_RESULT="PRESENT_EXACT_MODEL_${MODEL}"
else
  PREFLIGHT_RESULT="ABSENT_EXACT_MODEL_${MODEL}"
  VERDICT="BLOCKED_LOCAL_LAB_EXACT_MODEL_ABSENT"
  COMMAND_EXIT_STATUS="NOT_RUN"
  : >"${STDOUT_FILE}"
  print_result_block
  exit 1
fi

set +e
python -m alpha.local_llm.operator_cli --enable-local-llm --endpoint-url http://127.0.0.1:11434/api/chat --model gemma3:4b --timeout-seconds 30 --prompt "Synthetic local-only fixture: summarize this toy note in one sentence. Note: Ada put two blue blocks and one red block in a box." >"${STDOUT_FILE}" 2>"${STDERR_FILE}"
COMMAND_EXIT_STATUS="$?"
set -e

if [[ "${COMMAND_EXIT_STATUS}" == "0" ]]; then
  VERDICT="SUCCESS_LOCAL_SMOKE"
elif grep -Eiq 'connection refused|failed to connect|could not connect|connection error|connection reset|endpoint|unreachable|timed out|timeout|127\.0\.0\.1:11434|localhost:11434' "${STDOUT_FILE}" "${STDERR_FILE}"; then
  VERDICT="BLOCKED_LOCAL_LAB_ENDPOINT_UNREACHABLE"
else
  VERDICT="FAILED_LOCAL_LAB_OTHER"
fi

print_result_block

if [[ "${COMMAND_EXIT_STATUS}" == "0" ]]; then
  exit 0
fi
exit 1
