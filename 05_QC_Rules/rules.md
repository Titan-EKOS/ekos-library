# QC Rules

Each rule comes from a redline. Format (parsed by the server's get_qc_rules):

    ## QC-0001 Short title
    ```yaml
    id: QC-0001
    rule: One-sentence check.
    scope: [all]                 # or jurisdictions / functions / tags
    function: qc
    jurisdiction: all
    source_redline: <job no> <markup file> p.<page> comment <n>
    projects: [<job no>]
    added: YYYY-MM-DD
    ```

<!-- Rules start below this line -->
