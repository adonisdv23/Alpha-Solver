# Operator input required

This lane required real operator approval before advancing past the execution gate.

Actual status:

```text
operator_approval_required=true
real_operator_approval_available=false
operator_approval_simulated=false
execution_gate_status=blocked_by_missing_approval
stop_state=blocked
```

The lane therefore used allowed option B from the operator-supervision rule: execute only the safe parts that do not require operator participation and mark DEF-001 as still not fully retired.

This packet does not claim a complete operator-supervised end-to-end flow. It captures a partial local flow and the correct stop-state behavior when operator approval is missing.
