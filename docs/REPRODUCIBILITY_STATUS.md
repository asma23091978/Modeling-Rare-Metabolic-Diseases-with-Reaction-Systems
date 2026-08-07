# Reproducibility status

## Verified against the manuscript

- The manuscript analyzes five target outcomes: `hga_a`, `sa`, `hawkinsin_a`, `tyr_b`, and the combined `tyr_b + bh4_b` target.
- The public Python script now enumerates exactly those five targets as presence targets.
- The manuscript appendix contains biological rules R1-R39.
- The 39 biological `react(...)` rules in `prolog/hgd0_04_02_reactions.pl` were compared in order against Appendix B. They match after correcting one typo in R38: `h20` -> `h2o`.
- The five supplied conditional-dependency matrices correspond to the five reported target analyses.
- The two bicolor PDF tables correspond to the dynamic negative slicing matrices cited in the manuscript appendix.

## Still missing for a clean full rerun

### 1. Slicing-enabled BioReSolve engine

The Python script loads:

```text
BioReSolvePositive.pl
```

and calls:

```prolog
main_do(negslice, EKs, ListReactNumbR, ListEpos, ListEneg, ListCS).
```

The supplied `BioReSolvePlus_bb_guarded.pl` does not provide this slicing interface, so it was not renamed or substituted.

### 2. Exact LTS DOT graph

The script reads:

```text
output/hgd0_04-02.dot
```

The exact graph was not supplied. `graf_code_last.txt` is not a DOT file.

### 3. Final LTS-generation configuration/driver

The manuscript states that the LTS was generated in BioReSolve over 17,496 initial configurations. The final configuration/driver that generates those contexts and the exact manuscript LTS was not identifiable among the supplied final DEA files. The older quantitative model files were not used as replacements.

## Publication housekeeping still pending

- choose and add the repository license;
- if available, record the exact Python package versions and SWI-Prolog version used for the reported run (the supplied `requirements.txt` contains package names but no version pins);
- after acceptance/publication, replace the citation placeholder in `README.md` with the final bibliographic citation/DOI;
- ideally archive raw slicing summaries/JSON outputs for the other four targets if the original run outputs are available.
