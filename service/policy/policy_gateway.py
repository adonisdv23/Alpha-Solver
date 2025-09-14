from dataclasses import dataclass, field
from typing import Dict, Tuple

from . import redaction


@dataclass
class PolicyConfig:
    enable_input_redaction: bool = True
    detectors: Dict[str, bool] = field(default_factory=lambda: {"email": True, "phone": True})
    latency_budget_ms_p95: int = 50
    ner_provider: str = "none"
    fail_closed: bool = True


class PolicyGateway:
    """Gateway applying PII policy before logging and model input."""

    def __init__(self, config: PolicyConfig | None = None):
        self.config = config or PolicyConfig()

    def process(self, message: str, route_explain: Dict, *, for_model: bool = False) -> Tuple[str, str]:
        """Redact *message* for logging and optionally for model input.

        Parameters
        ----------
        message: str
            The raw incoming message.
        route_explain: Dict
            Mutable dict augmented with policy information.
        for_model: bool
            Whether the processed message will be sent to the model.

        Returns
        -------
        (log_text, model_text)
            Text for logging and for model consumption respectively.
        """
        try:
            redacted, stats = redaction.redact(message, self.config.detectors)
            route_explain["policy_verdict"] = "pass"
            route_explain["redaction_stats"] = stats
            log_text = redacted
            if for_model and self.config.enable_input_redaction:
                model_text = redacted
            else:
                model_text = message
            return log_text, model_text
        except Exception as exc:
            if self.config.fail_closed:
                route_explain["policy_verdict"] = "error"
                route_explain["redaction_stats"] = {"error": str(exc)}
                masked = "[REDACTED]"
                return masked, masked if (for_model and self.config.enable_input_redaction) else ""
            raise
