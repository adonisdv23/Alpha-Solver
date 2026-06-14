# Stop Control Evidence

`ALPHA_PROVIDER_EMERGENCY_STOP` is an operator stop control. When enabled, `/v1/solve` returns a provider SAFE-OUT before provider client execution. The focused test uses `FakeProviderClient([])` and asserts no request was recorded.
