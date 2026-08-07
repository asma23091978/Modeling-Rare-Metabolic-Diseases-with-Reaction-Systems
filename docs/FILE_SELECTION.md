# File selection for the public paper repository

The source ZIP and the additional files were inspected against the manuscript methods, targets, appendix rule set, and Code Availability statement. Only files that are directly useful for the PT-RS paper or its computational reproducibility were retained.

## Included

- `slicing_script.py`: cleaned public version of the supplied `PTD_RS_slicing_analysis_english.py`. The active attractor/slicing logic and the Prolog environment written to `params.pl` were preserved; unrelated/dead experimental branches and large commented blocks were removed, the five manuscript targets were made explicit, output filenames were normalized, and execution is now under a standard `main()` entry point.
- `prolog/hgd0_04_02_reactions.pl`: current DEA/RS reaction model. Its 39 biological rules were compared with manuscript Appendix B; R38 had one spelling error (`h20`) and was corrected to `h2o`.
- five `necessary_matrix_by_target_*.pdf` files: direct target-specific attractor/conditional-dependency results.
- `table_results_bicolor-1.pdf` and `table_results_bicolor-2.pdf`: dynamic-negative-slicing matrices used in the manuscript appendix.
- positive and negative `sa` slicing summaries: the only supplied raw text slicing summaries.

## Not included as substitutes

- `rules_update7-01 (1)(1).pl`: older reaction file; it does not contain the final `_nul` enzyme states used by the manuscript model and contains a local absolute path.
- `alkaptonuria_17-07.pl`: older quantitative encoding with duplicated `myDeltaQ` definitions and an explicit editing note in the file.
- `alkaptonuria_17-07 -altobasso.pl`: older quantitative encoding using a different representation from the final DEA model.
- `graf_code_last.txt`: Prolog/quantitative model text, not a DOT transition graph.
- `BioReSolvePlus_bb_guarded.pl`: a BioReSolve variant with local absolute paths, but it does not contain the `ordslice`/`negslice` interface required by `slicing_script.py`; it cannot safely replace the missing `BioReSolvePositive.pl`.
- the complete manuscript LaTeX source: not required by the repository's Code Availability statement; only computational result artifacts needed for the paper were selected from it.

No missing runtime file was invented or reconstructed under a misleading filename.
