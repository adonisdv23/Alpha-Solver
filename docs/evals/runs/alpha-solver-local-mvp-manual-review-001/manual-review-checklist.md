# Manual Review Checklist

| # | Check | Status | Evidence boundary |
|---|-------|--------|-------------------|
| 1 | Local console opens | Observed | Screenshot shows local console in browser. |
| 2 | Route preview panel is visible | Observed | Screenshot shows route preview panel. |
| 3 | Route preview can be requested without smoke execution | Missing / deferred | Preview button is visible, but it was not clicked in provided evidence. |
| 4 | Model recommendation appears | Missing / deferred | Recommended model after preview was not observed. |
| 5 | Tool recommendation appears | Missing / deferred | Recommended tool after preview was not observed. |
| 6 | Route reasons appear | Missing / deferred | Route reasons after preview were not observed. |
| 7 | Warnings appear or explicit no-warning state appears | Missing / deferred | Warnings or no-warning state after preview were not observed. |
| 8 | Fallback appears or explicit no-fallback state appears | Missing / deferred | Fallback or no-fallback state after preview was not observed. |
| 9 | Evidence boundary appears | Observed | Evidence boundary panel and route preview evidence boundary are visible. |
| 10 | Provider/local execution authorization remains false in preview | Observed initial state | Screenshot shows provider/local execution authorized as `false`; no preview click was tested. |
| 11 | Tool execution authorization remains false in preview | Observed initial state | Screenshot shows tool execution authorized as `false`; no preview click was tested. |
| 12 | Smoke execution is separate from preview | Partially observed / deferred | Separate bounded smoke check section is visible, but separation was not action-tested. |
| 13 | Prompt-too-long behavior fails closed | Missing / deferred | Not tested. |
| 14 | Sanitized JSON panel exists | Observed | Screenshot shows sanitized JSON panel. |
| 15 | Copy behavior is scoped to sanitized JSON | Missing / deferred | Copy button is visible, but copy behavior was not tested. |
| 16 | No API key field is present | Observed | No API key field is visible in the screenshot. |
| 17 | No `/v1/solve` is exposed | Not evidenced by screenshot / deferred | The screenshot does not establish endpoint exposure status. |
| 18 | No external assets are required | Not evidenced by screenshot / deferred | The screenshot does not establish asset loading requirements. |
