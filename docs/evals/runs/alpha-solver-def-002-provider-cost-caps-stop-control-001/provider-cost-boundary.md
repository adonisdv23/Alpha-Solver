# Provider Cost Boundary

Provider execution is fail-closed when caps are absent, blank, malformed, non-finite, non-positive, when requested output tokens exceed the operator output cap, when provider result token usage is missing or exceeds caps, or when provider result cost is missing or exceeds the cost cap.

Cost checks are based on provider/price-hint telemetry returned by the provider adapter and are not exact billing accuracy claims.
