#!/usr/bin/env bash
_alpha_solver_complete() {
  local cur prev opts
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"
  local subcommands="run replay gates finops traces"
  if [[ ${COMP_CWORD} -eq 1 ]]; then
    COMPREPLY=( $(compgen -W "${subcommands}" -- "$cur") )
    return 0
  fi
  case "${COMP_WORDS[1]}" in
    run)
      opts="--file --model --max-tokens --low-conf-threshold --clarify-conf-threshold --min-budget-tokens --seed --record --replay --metrics --no-metrics --out --verbose --dry-run"
      ;;
    replay)
      opts="--max-tokens --min-budget-tokens"
      ;;
    gates)
      opts="--low-conf-threshold --clarify-conf-threshold --min-budget-tokens --confidence --tokens"
      ;;
    finops)
      opts="--prompt --tokens --min-budget-tokens"
      ;;
    traces)
      opts="--prompt --max-tokens --min-budget-tokens --out"
      ;;
    *)
      opts=""
      ;;
  esac
  COMPREPLY=( $(compgen -W "${opts}" -- "$cur") )
  return 0
}
complete -F _alpha_solver_complete alpha-solver
