# Modeling Rare Metabolic Diseases with Reaction Systems

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
    └── LTS.dot

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
   % :- ['params.pl'].
   ```

4. Start SWI-Prolog from the repository root. At the `?-` prompt, enter these queries one at a time:

   ```prolog
   ['BioReSolvePositive.pl'].
   main_do(digraph).
   ```

5. Rename the generated `output/tmp-digraph-*.dot` file to `output/LTS.dot`, the path expected by the Python analysis.

## Running the analysis

Once `output/LTS.dot` is ready, switch `rules.pl` to the slicing configuration:

```prolog
% :- ['params_fixed_context.pl'].
:- ['params.pl'].
```

From the repository root, run: 

```sh
python slicing_script.py
```

The script reads `output/LTS.dot`, identifies attractors containing the manuscript targets, extracts the corresponding initial contexts, and writes `params.pl` for each slicing case before calling BioReSolve for dynamic negative slicing. Generated analysis files are written under `Results/`. 


## Citation

If you use this code or build on this work, please cite the associated article.

```bibtex
@article{Bendjeddou2027ReactionSystems,
  author  = {Bendjeddou, Asma and Brodo, Linda and Falaschi, Moreno and Graziani, Caterina},
  title   = {Modeling rare metabolic diseases with reaction systems},
  journal = {Journal of Logical and Algebraic Methods in Programming},
  volume  = {152},
  year    = {2027},
  pages   = {101185},
  issn    = {2352-2208},
  doi     = {10.1016/j.jlamp.2026.101185}
}
```
