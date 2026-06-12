# Directory-reference behavior before and after

| Reference class | Before this lane | After this lane | Test coverage |
|---|---|---|---|
| Missing alpha-solver-post-* directory reference | Could be skipped because the suffix-less path did not exist before classification. | Collected as a checked post-Level reference and reported when absent. | `test_doc_path_checker_reports_missing_post_packet_directory_reference` |
| Existing alpha-solver-post-* directory reference | Allowed when the path existed. | Still allowed when the path exists. | `test_doc_path_checker_handles_trailing_slash_for_directory_references and test_doc_path_checker_uses_tmp_root_for_existing_directory_reference` |
| Missing legacy local-LLM directory reference | Could be skipped by the same suffix-less existence pre-filter. | Collected as a checked legacy local-LLM reference and reported when absent. | `test_doc_path_checker_reports_missing_legacy_local_llm_directory_reference` |
| Missing checked `.md` reference | Reported because checked text suffixes were already considered checkable. | Still reported. | Existing `test_doc_path_checker_checks_references_in_post_packet_fixture` |
| Glob/shell-like unresolved pattern | Ignored by the unresolved syntax skip. | Still ignored before checkable classification. | `test_doc_path_checker_ignores_glob_shell_like_unresolved_directory_pattern` |
| Intentional historical/mistake/non-action missing reference | Would now be visible after the directory-reference fix unless narrowly exempted. | Exempted only when explicit local context or a known preserved incident record identifies the reference as historical or non-action. | `test_doc_path_checker_exempts_intentional_historical_missing_directory_reference` |
