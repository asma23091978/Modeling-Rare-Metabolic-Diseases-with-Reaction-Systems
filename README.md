# Modeling Rare Metabolic Diseases with Reaction Systems (PT-RS)

This repository contains the computational material associated with the manuscript **“Modeling Rare Metabolic Diseases with Reaction Systems”**. The study models phenylalanine-tyrosine (Phe-Tyr) catabolism with Reaction Systems (RSs) and Discrete Entity-Level Annotation (DEA), and analyzes disease-relevant outcomes by target-oriented attractor analysis and dynamic negative slicing.

## What is included

The repository contains:

- `slicing_script.py`: Python post-processing for attractor analysis and dynamic negative slicing;
- `prolog/hgd0_04_02_reactions.pl`: the PT-RS Prolog reaction specification, including auxiliary DEA rules and the 39 biological rules reported in the manuscript appendix;
- `results/conditional_dependency_matrices/`: the five supplied target-specific conditional-dependency matrices;
- `results/dynamic_negative_slicing/`: the two slicing summary matrices used in the manuscript appendix, plus the supplied positive/negative raw summary for the `sa` target;
- `scripts/repo_check.py`: a repository consistency checker;
- `requirements.txt`: Python dependencies.

The biological rule block was checked against manuscript Appendix B (R1-R39). One transcription error in the previous GitHub package was corrected in R38: `h20` -> `h2o`.

## Paper targets

The public script is configured for the five target outcomes analyzed in the manuscript:

| Manuscript target | Code entity/entities | Interpretation |
|---|---|---|
| HGA accumulation | `hga_a` | accumulated homogentisic acid |
| Succinylacetone production | `sa` | succinylacetone present |
| Hawkinsin accumulation | `hawkinsin_a` | accumulated hawkinsin |
| Low tyrosine | `tyr_b` | low tyrosine |
| Low tyrosine + low BH4 | `tyr_b`, `bh4_b` | combined target |

DEA suffixes used in the implementation are: `_a` for accumulated metabolite level, no suffix for normal level, `_b` for low metabolite/cofactor level or hypomorphic enzyme activity, and `_nul` for null enzyme activity.

## Repository structure

```text
.
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE-TODO.md
├── slicing_script.py
├── prolog/
│   └── hgd0_04_02_reactions.pl
├── output/
│   └── README.md
├── results/
│   ├── README.md
│   ├── conditional_dependency_matrices/
│   │   ├── necessary_matrix_by_target_hga_a.pdf
│   │   ├── necessary_matrix_by_target_hawk_a.pdf
│   │   ├── necessary_matrix_by_target_sa.pdf
│   │   ├── necessary_matrix_by_target_tyr_b.pdf
│   │   └── necessary_matrix_by_target_tyr_b_bh4_b.pdf
│   └── dynamic_negative_slicing/
│       ├── table_results_bicolor-1.pdf
│       ├── table_results_bicolor-2.pdf
│       └── sa/
│           ├── pos_output_sa.txt
│           └── neg_output_sa.txt
├── docs/
│   ├── FILE_SELECTION.md
│   └── REPRODUCIBILITY_STATUS.md
└── scripts/
    └── repo_check.py
```

## Requirements

- Python 3.9 or later
- SWI-Prolog
- the Python packages in `requirements.txt`
- the exact slicing-enabled BioReSolve Prolog file expected by the script as `BioReSolvePositive.pl`
- the exact LTS graph expected by the script as `output/hgd0_04-02.dot`

Install the Python dependencies with:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Running the analysis

After adding the two exact runtime files listed above, run:

```bash
python slicing_script.py
```

The script reads `output/hgd0_04-02.dot`, identifies attractors containing each paper target, extracts the corresponding initial contexts, generates `params.pl`, and calls BioReSolve for dynamic negative slicing. Generated files are written under `Results/` and are intentionally ignored by Git.

## Reproducibility status

This GitHub package is **paper-aligned but not yet fully executable from a clean clone**, because two files required by the current workflow were not present in the material supplied for this update:

1. `BioReSolvePositive.pl` containing the slicing predicates used by the Python code, including `main_do(negslice, ...)`;
2. `output/hgd0_04-02.dot`, the exact labeled transition system used for the reported analysis.

For end-to-end regeneration of the LTS from the RS model, the final LTS-generation configuration/driver used for the 17,496 initial configurations should also be archived. The older quantitative Prolog files supplied separately were not inserted as substitutes because they do not match the final DEA encoding described in the manuscript.

See `docs/REPRODUCIBILITY_STATUS.md` for the detailed check.

## Repository check

Run:

```bash
python scripts/repo_check.py
```

The checker reports missing runtime files and scans public text/code files for local absolute paths.

## Citation

The associated manuscript is **“Modeling Rare Metabolic Diseases with Reaction Systems”**. Add the final journal citation and DOI here once they are assigned.

## License

A license has not yet been selected for this repository. `LICENSE-TODO.md` is intentionally retained so that no license is assigned without the authors' decision.
