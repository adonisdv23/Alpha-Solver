#!/usr/bin/env bash
set -u

OUT_DIR="artifacts/local_llm_controlled_usage_operator_run_001"

COMMAND_FILE="$OUT_DIR/executed_command.txt"
STDOUT_FILE="$OUT_DIR/cli_stdout.json"
STDERR_FILE="$OUT_DIR/cli_stderr.txt"
EXIT_FILE="$OUT_DIR/exit_code.txt"
META_FILE="$OUT_DIR/run_metadata.txt"

{
  echo "repo_head=$(git rev-parse HEAD)"
  echo "repo_status_begin"
  git status --short
  echo "repo_status_end"
  echo "command_identity=python3 -m alpha.local_llm.operator_cli"
  echo "artifact_dir=$OUT_DIR"
} > "$META_FILE"

cat > "$COMMAND_FILE" <<'CMD'
env -u OPENAI_API_KEY -u ANTHROPIC_API_KEY -u GOOGLE_API_KEY -u GEMINI_API_KEY -u DEEPSEEK_API_KEY \
python3 -m alpha.local_llm.operator_cli \
  --enable-local-llm \
  --prompt-file artifacts/local_llm_controlled_usage_operator_run_001/controlled_usage_prompt.txt \
  --endpoint-url "http://127.0.0.1:11434/api/chat" \
  --model "qwen2.5:3b" \
  --timeout-seconds "60"
CMD

env -u OPENAI_API_KEY -u ANTHROPIC_API_KEY -u GOOGLE_API_KEY -u GEMINI_API_KEY -u DEEPSEEK_API_KEY \
python3 -m alpha.local_llm.operator_cli \
  --enable-local-llm \
  --prompt-file "$OUT_DIR/controlled_usage_prompt.txt" \
  --endpoint-url "http://127.0.0.1:11434/api/chat" \
  --model "qwen2.5:3b" \
  --timeout-seconds "60" \
  > "$STDOUT_FILE" \
  2> "$STDERR_FILE"

rc=$?
printf '%s\n' "$rc" > "$EXIT_FILE"

exit 0
