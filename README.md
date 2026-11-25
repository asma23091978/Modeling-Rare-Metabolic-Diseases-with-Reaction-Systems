# Modeling Rare Metabolic Diseases with Reaction Systems (PT-RS)

This repository contains the computational material associated with the manuscript **“Modeling Rare Metabolic Diseases with Reaction Systems”**. The study models phenylalanine-tyrosine (Phe-Tyr) catabolism with Reaction Systems (RSs) and Discrete Entity-Level Annotation (DEA), and analyzes disease-relevant outcomes by target-oriented attractor analysis and dynamic negative slicing.

DEA suffixes used in the implementation are: `_a` for accumulated metabolite level, no suffix for normal level, `_b` for low metabolite/cofactor level or hypomorphic enzyme activity, and `_nul` for null enzyme activity.

## Repository structure

```text
.
├── README.md
├── requirements.txt
├── .gitignore
├── slicing_script.py
├── rules.pl
├── params.pl
├── params_fixed_context.pl
├── BioReSolvePositive.pl
├── output/
│   └── LTS.dot
├── Results/
    ├── README.md
    ├── conditional_dependency_matrices/
    │   ├── necessary_matrix_by_target_hga_a.pdf
    │   ├── necessary_matrix_by_target_hawk_a.pdf
    │   ├── necessary_matrix_by_target_sa.pdf
    │   ├── necessary_matrix_by_target_tyr_b.pdf
    │   └── necessary_matrix_by_target_tyr_b_bh4_b.pdf
    └── dynamic_negative_slicing/
       ├── table_results_bicolor-1.pdf
       ├── table_results_bicolor-2.pdf
       └── sa/
           ├── pos_output_sa.txt
           └── neg_output_sa.txt
```

## Requirements

- Python 3.9 or later
- [SWI-Prolog](https://www.swi-prolog.org/)
- The Python dependencies listed in `requirements.txt`
- The Prolog files listed below

Install the Python dependencies from the repository root:

```sh
pip install -r requirements.txt
```

## Generating the transition graph

The labeled transition system (LTS) is generated locally from the reaction rules and initial context. The resulting `.dot` can be generated through the following steps:

2. In the `BioReSolvePositive.pl` file, change the following directives to load a Reaction System specification by pointing to a path in your file system:

:-["YOUR_PATH/rules.pl"].

Some predicates automatically save some output on the file system (mostly LTS representations in .dot format) wdpath/1 sets the working directory with permissions for I/O on filesuse the following directives and settings for the reaction rules and output directory:

wdpath("YOUR_PATH/output_tmp/").


3. In `rules.pl`, enable the following directive. 

   ```prolog
   :- ['params_fixed_context_30-01_nul.pl'].
   ```

4. Start SWI-Prolog from the repository root. At the `?-` prompt, enter these queries one at a time:

   ```prolog
   ['BioReSolvePositive.pl'].
   main_do(digraph).
   ```

5. Rename the generated `output/tmp-digraph-*.dot` file to `output/LTS.dot`, the path expected by the Python analysis.

## Running the analysis

After generating the graph, run the analysis from the repository root:

```sh
python slicing_script.py
```

The script reads `output/LTS.dot`, identifies attractors containing the manuscript targets, extracts the corresponding initial contexts, and calls BioReSolve for dynamic negative slicing. Generated analysis files are written under `Results/`.

## Citation
