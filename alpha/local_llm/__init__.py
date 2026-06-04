"""Local LLM proof helpers.

This package is intentionally not wired into the production solve path. It
contains fake-client-only seams used to prove portable-contract consumption.
"""

from .portable_contract import (  # noqa: F401
    DEFAULT_CONTRACT_PATH,
    FakeLocalLLMProofClient,
    LocalLLMProofRequest,
    LocalLLMProofResult,
    PortableContract,
    PortableContractError,
    build_local_llm_proof_request,
    load_portable_contract,
    run_fake_local_llm_contract_proof,
)
