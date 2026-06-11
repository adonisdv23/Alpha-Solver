# Privacy and redaction rules

- Do not copy raw secrets or unredacted private artifacts.
- Do not include credentials, API keys, billing identifiers, private local machine data, or unrelated project material.
- Repo-relative evidence paths are allowed.
- Local paths recorded by prior evidence are provenance references only; classify them as reviewed-safe if they reveal no secret or private machine detail needed beyond the existing evidence, otherwise record a defect.
- If a Council chat sees possible secret material, it must summarize the category and path only, not reproduce the secret.
