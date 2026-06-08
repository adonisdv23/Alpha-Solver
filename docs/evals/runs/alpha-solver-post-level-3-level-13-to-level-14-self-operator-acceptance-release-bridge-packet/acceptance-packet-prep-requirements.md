# Acceptance packet prep requirements

Before manual local acceptance can run, the future acceptance packet must:

- verify all prerequisite implementation lanes are merged and GS done;
- recheck live GitHub state before acting;
- name the exact local-only command or operator procedure to be used;
- identify expected raw and redacted artifact paths;
- identify required operator confirmation text;
- list blocked actions before execution starts;
- define pass, fail, warning, and blocked result categories;
- preserve the evidence boundary that acceptance is local-only and operator-supervised;
- include an abort path if explicit operator confirmation is missing.
