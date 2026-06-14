# Local Resource Notes

## Resource classes

- Small laptop: likely appropriate for smaller quantized chat or embedding models, subject to operator hardware and current Ollama packaging.
- Stronger laptop: likely appropriate for mid-size quantized models, especially coder or stronger generalist variants.
- Desktop/GPU: likely needed for larger variants or multiple-model iteration where latency matters.
- Unknown: use when model size, quantization, memory pressure, or local availability is not yet confirmed.

## Practical notes

- Exact RAM, VRAM, CPU, and latency needs are not measured in this lane.
- Install commands in this packet are not execution logs.
- The next harness should record model name, model digest when available, host class, endpoint URL shape, timeout, prompt count, and fail-closed reason codes.
- Multi-model local testing should start serially before any parallel execution, to avoid confounding resource failures with model behavior.
