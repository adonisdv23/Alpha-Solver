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
from .provider_adapter import (  # noqa: F401
    LocalLLMAdapterMessage,
    LocalLLMAdapterRequest,
    LocalLLMAdapterResult,
    LocalLLMProviderAdapterError,
    LocalLLMProviderBackend,
    OllamaLocalHTTPBackend,
    StubLocalLLMProviderBackend,
    build_ollama_chat_payload,
    build_local_llm_adapter_request,
    parse_ollama_assistant_text,
    run_local_llm_provider_adapter,
)
