"""Target-oriented attractor analysis and dynamic negative slicing.

This script was adapted from 
L. Brodo, R. Bruni, M. Falaschi, R. Gori, P. Milazzo, Slicing analyses for negative dependencies in reaction systems modeling gene regulatory networks, Nat.
Comput. 24 (2025) 1045–1074. https://doi.org/10.1007/s11047-025-10046-5.

Required runtime files:
- output/LTS.dot
- BioReSolvePositive.pl
"""

import glob
import json
import os
from functools import reduce
from itertools import chain

import networkx as nx
import pandas as pd
from IPython.display import display
from swiplserver import PrologMQI


class Target:
    def __init__(self, present, absent=None):
        self.present = present
        self.absent = absent or []

    def __str__(self):
        return f"present: {self.present} absent: {self.absent}"


# Targets explicitly analyzed in the manuscript.
# DEA code mapping:
#   _a   = accumulated metabolite level
#   _b   = low metabolite/cofactor level or hypomorphic enzyme activity
#   _nul = null enzyme activity
PAPER_TARGETS = [
    Target(["hga_a"]),
    Target(["sa"]),
    Target(["hawkinsin_a"]),
    Target(["tyr_b"]),
    Target(["tyr_b", "bh4_b"]),
]
targets = PAPER_TARGETS

DOT_NAME = "LTS"
DOT_PATH = os.path.join("output", DOT_NAME + ".dot")
BIORESOLVE_FILE = "BioReSolvePositive.pl"
CONTEXT_SIZE = 10  # BH4, Phe, TAT, PLP, DHPR, PAH, GSTZ1, HPD, HGD, FAH

PROLOG_ENVIRONMENT = "myenvironment('[bh4_p_b = {bh4_b}.bh4_p_b1,\n  bh4_p_b1 = {xbh4_b}.bh4_p_b1,\n  bh4_p_n = {bh4}.bh4_p_n1,\n  bh4_p_n1 = {xbh4}.bh4_p_n1,\n  phe_p_b = {phe_b}.phe_p_b1,\n  phe_p_b1 = {xphe_b}.phe_p_b1,\n  phe_p_n = {phe}.phe_p_n1,\n  phe_p_n1 = {xphe}.phe_p_n1,\n tat_p_nul = {tat_nul}.tat_p_nul1,\n tat_p_nul1 = {xtat_nul}.tat_p_nul1,\n tat_p_b = {tat_b}.tat_p_b1,\n  tat_p_b1 = {xtat_b}.tat_p_b1,\n  tat_p_n = {tat}.tat_p_n1,\n  tat_p_n1 = {xtat}.tat_p_n1,\n  plp_p_b = {plp_b}.plp_p_b1,\n  plp_p_b1 = {xplp_b}.plp_p_b1,\n  plp_p_n = {plp}.plp_p_n1,\n  plp_p_n1 = {xplp}.plp_p_n1,\n dhpr_p_nul = {dhpr_nul}.dhpr_p_nul1,\n dhpr_p_nul1 = {xdhpr_nul}.dhpr_p_nul1,\n dhpr_p_b = {dhpr_b}.dhpr_p_b1,\n  dhpr_p_b1 = {xdhpr_b}.dhpr_p_b1,\n  dhpr_p_n = {dhpr}.dhpr_p_n1,\n  dhpr_p_n1 = {xdhpr}.dhpr_p_n1,\n pah_fe2_p_nul = {pah_fe2_nul}.pah_fe2_p_nul1,\n pah_fe2_p_nul1 = {xpah_fe2_nul}.pah_fe2_p_nul1,\n pah_fe2_p_b = {pah_fe2_b}.pah_fe2_p_b1,\n  pah_fe2_p_b1 = {xpah_fe2_b}.pah_fe2_p_b1,\n  pah_fe2_p_n = {pah_fe2}.pah_fe2_p_n1,\n pah_fe2_p_n1 = {xpah_fe2}.pah_fe2_p_n1,\n gstz1_p_nul = {gstz1_nul}.gstz1_p_nul1,\n gstz1_p_nul1 = {xgstz1_nul}.gstz1_p_nul1,\n gstz1_p_b = {gstz1_b}.gstz1_p_b1,\n  gstz1_p_b1 = {xgstz1_b}.gstz1_p_b1,\n  gstz1_p_n = {gstz1}.gstz1_p_n1,\n  gstz1_p_n1 = {xgstz1}.gstz1_p_n1,\n hpdfe_p_nul = {hpdfe_nul}.hpdfe_p_nul1,\n hpdfe_p_nul1= {xhpdfe_nul}.hpdfe_p_nul1,\n hpdfe_p_b = {hpdfe_b}.hpdfe_p_b1,\n  hpdfe_p_b1 = {xhpdfe_b}.hpdfe_p_b1,\n hpdfe_p_n = {hpdfe}.hpdfe_p_n1,\n  hpdfe_p_n1 = {xhpdfe}.hpdfe_p_n1,\n hgdfe_p_nul = {hgdfe_nul}.hgdfe_p_nul1,\n hgdfe_p_nul1= {xhgdfe_nul}.hgdfe_p_nul1,\n hgdfe_p_b = {hgdfe_b}.hgdfe_p_b1,\n  hgdfe_p_b1 = {xhgdfe_b}.hgdfe_p_b1,\n hgdfe_p_n = {hgdfe}.hgdfe_p_n1,\n  hgdfe_p_n1 = {xhgdfe}.hgdfe_p_n1,\n fahmgca_p_nul = {fahmgca_nul}.fahmgca_p_nul1,\n fahmgca_p_nul1= {xfahmgca_nul}.fahmgca_p_nul1,\n fahmgca_p_b = {fahmgca_b}.fahmgca_p_b1,\n fahmgca_p_b1 = {xfahmgca_b}.fahmgca_p_b1,\n fahmgca_p_n = {fahmgca}.fahmgca_p_n1,\n fahmgca_p_n1 = {xfahmgca}.fahmgca_p_n1 \n]').\n \n"
PROLOG_ENTITIES = 'myentities([h,o2,h2o,bh2, alphakg, nadh, gsh, ala, arat]).\n \n'


def check_node(node):
    """Return True when node belongs to a cycle."""
    cycle = list(nx.find_cycle(G, node))
    return reduce(
        lambda b1, b2: b1 or b2,
        (edge[0] == node or edge[1] == node for edge in cycle),
    )


def compute_attractor(node):
    """Return the entities present in the cycle reachable from node."""
    cycle = list(nx.find_cycle(G, node))
    states = (edge[0].split(";") + edge[1].split(";") for edge in cycle)
    merged = reduce(lambda x, y: x + y, states)
    return list(dict.fromkeys(merged))


def count_states(contexts_dict):
    return sum(len(states) for states in contexts_dict.values())


def target_computations(target):
    """Find target-containing attractors and their originating contexts."""
    all_nodes = list(G.nodes)
    filtered = [node for node in all_nodes if check_node(node)]
    attractors_map = {node: compute_attractor(node) for node in filtered}

    for entity in target.present:
        filtered = [node for node in filtered if entity in attractors_map[node]]

    for entity in target.absent:
        filtered = [node for node in filtered if entity not in attractors_map[node]]

    filtered_with_target = [
        node for node in filtered if set(node.split(";")) & set(target.present)
    ]

    contexts = []
    contexts_dict = {}
    for state_text in (node.split(";") for node in filtered_with_target):
        context = state_text[:CONTEXT_SIZE]
        pure_state = state_text[CONTEXT_SIZE:]
        context_key = ",".join(context)
        if context not in contexts:
            contexts.append(context)
            contexts_dict[context_key] = [",".join(pure_state)]
        else:
            contexts_dict[context_key].append(",".join(pure_state))

    print("TARGET --> " + str(target))
    print("Found " + str(len(contexts)) + " contexts that lead to the target")
    print(
        "Found "
        + str(count_states(contexts_dict) + (len(filtered) - len(filtered_with_target)))
        + " states in reachable attractors"
    )
    print(
        "Of these, "
        + str(count_states(contexts_dict))
        + " contain entities from the target"
    )
    print()
    return contexts, contexts_dict


table_data_df = pd.DataFrame()


def generate_table(
    target_desc,
    intersection_pos_set,
    union_pos_set,
    intersection_neg_set,
    union_neg_set,
):
    """Accumulate positive/negative union/intersection data for all targets."""
    global table_data_df

    all_strings = sorted(
        set(table_data_df.columns.get_level_values(0)).union(
            union_pos_set, union_neg_set
        )
    )
    columns = [
        (entity, category)
        for entity in all_strings
        for category in ("POS", "NEG")
    ]

    if table_data_df.empty:
        table_data_df = pd.DataFrame(columns=pd.MultiIndex.from_tuples(columns))
    else:
        missing_columns = set(columns) - set(table_data_df.columns)
        for column in missing_columns:
            table_data_df[column] = 0
        table_data_df = table_data_df[columns]

    new_row = {column: 0 for column in table_data_df.columns}
    for entity in all_strings:
        if entity in intersection_pos_set:
            new_row[(entity, "POS")] = 2
        elif entity in union_pos_set:
            new_row[(entity, "POS")] = 1

        if entity in intersection_neg_set:
            new_row[(entity, "NEG")] = 2
        elif entity in union_neg_set:
            new_row[(entity, "NEG")] = 1

    table_data_df = pd.concat(
        [table_data_df, pd.DataFrame([new_row], index=[target_desc])]
    ).fillna(0)

    def highlight_cells(value):
        if value == 2:
            return "background-color: black; color: white"
        if value == 1:
            return "background-color: gray; color: white"
        return ""

    display(table_data_df.style.applymap(highlight_cells))


def save_table_to_file(filename):
    table_data_df.to_csv(filename, index=True)


def write_slicing_params(context_text, state, target):
    """Write params.pl for one context/attractor-state/target combination."""
    with open("params.pl", "w", encoding="utf-8") as param_file:
        param_file.write(PROLOG_ENVIRONMENT)
        param_file.write(PROLOG_ENTITIES)
        param_file.write(f'mycontext("[{context_text}]").\n\n')
        param_file.write(f"mytarget([{state}]).\n")
        param_file.write(f"mypos([{','.join(target.present)}]).\n")
        param_file.write("myneg([]).")


def cleanup_temporary_slicing_files():
    for pattern in (
        "tmp-slice*.txt",
        "tmp-legenda*.txt",
        "tmp-slicingrun*.txt",
    ):
        for filename in glob.glob(pattern):
            os.remove(filename)


def dynamic_negative_slicing_analysis():
    """Run BioReSolve dynamic negative slicing for every paper target."""
    output_dir = os.path.join("Results", "Final", "slicing", "negative", DOT_NAME)
    os.makedirs(output_dir, exist_ok=True)
    summary_path = os.path.join(output_dir, "summary_all_paper_targets.txt")

    with open(summary_path, "w", encoding="utf-8") as outfile:
        for target_count, target in enumerate(targets, start=1):
            sliced_computations_pos = []
            sliced_computations_neg = []

            print(f"TARGET COUNT: {target_count}/{len(targets)}")
            contexts, contexts_dict = target_computations(target)

            union_pos_set = set()
            intersection_pos_set = set()
            union_neg_set = set()
            intersection_neg_set = set()
            first_slice = True
            total = count_states(contexts_dict)
            counter = 1

            for context in contexts:
                context_text = ",".join(context)
                target_states = contexts_dict[context_text]
                for state_index, state in enumerate(target_states, start=1):
                    print(f"TEST CASE: {counter}/{total}")
                    counter += 1
                    print(
                        "CONTEXT: "
                        + context_text
                        + "      ATTRACTOR STATE: "
                        + f"{state_index}/{len(target_states)}"
                    )
                    print("STATE: " + state)

                    write_slicing_params(context_text, state, target)

                    with PrologMQI() as mqi:
                        with mqi.create_thread() as prolog_thread:
                            prolog_thread.query(f'["{BIORESOLVE_FILE}"]')
                            result = prolog_thread.query(
                                "main_do(negslice,EKs,ListReactNumbR,"
                                "ListEpos,ListEneg,ListCS)."
                            )

                    tmp_pos_set = set(chain.from_iterable(result[0]["ListEpos"]))
                    tmp_neg_set = set(chain.from_iterable(result[0]["ListEneg"]))
                    sliced_computations_pos.append(tmp_pos_set)
                    sliced_computations_neg.append(tmp_neg_set)
                    union_pos_set.update(tmp_pos_set)
                    union_neg_set.update(tmp_neg_set)

                    if first_slice:
                        intersection_pos_set = tmp_pos_set
                        intersection_neg_set = tmp_neg_set
                        first_slice = False
                    else:
                        intersection_pos_set = intersection_pos_set.intersection(
                            tmp_pos_set
                        )
                        intersection_neg_set = intersection_neg_set.intersection(
                            tmp_neg_set
                        )

            cleanup_temporary_slicing_files()

            union_pos_set = sorted(union_pos_set)
            intersection_pos_set = sorted(intersection_pos_set)
            union_neg_set = sorted(union_neg_set)
            intersection_neg_set = sorted(intersection_neg_set)

            outfile.write(
                "SET OF ENTITIES IN SLICED COMPUTATIONS FOR TARGET "
                + str(target)
                + ":\n"
            )
            outfile.write("         UNION POSITIVE: " + str(union_pos_set) + "\n")
            outfile.write(
                "         INTERSECTION POSITIVE: "
                + str(intersection_pos_set)
                + "\n"
            )
            outfile.write("         UNION NEGATIVE: " + str(union_neg_set) + "\n")
            outfile.write(
                "         INTERSECTION NEGATIVE: "
                + str(intersection_neg_set)
                + "\n\n"
            )
            outfile.flush()

            print("UNION POSITIVE:", union_pos_set)
            print("INTERSECTION POSITIVE:", intersection_pos_set)
            print("UNION NEGATIVE:", union_neg_set)
            print("INTERSECTION NEGATIVE:", intersection_neg_set)
            print()

            generate_table(
                str(target.present),
                intersection_pos_set,
                union_pos_set,
                intersection_neg_set,
                union_neg_set,
            )

            target_tag = "_".join(target.present)
            with open(
                os.path.join(output_dir, f"pos_sliced_computations_to_{target_tag}.json"),
                "w",
                encoding="utf-8",
            ) as file_handle:
                json.dump(
                    [list(values) for values in sliced_computations_pos],
                    file_handle,
                    indent=4,
                )

            with open(
                os.path.join(output_dir, f"neg_sliced_computations_to_{target_tag}.json"),
                "w",
                encoding="utf-8",
            ) as file_handle:
                json.dump(
                    [list(values) for values in sliced_computations_neg],
                    file_handle,
                    indent=4,
                )

    save_table_to_file("table_results_neg.csv")


def export_target_contexts():
    """Export initial contexts associated with each target-containing attractor."""
    context_output_dir = os.path.join(
        "Results", "Final", "context_to_target", DOT_NAME
    )
    os.makedirs(context_output_dir, exist_ok=True)

    for target in targets:
        contexts, _ = target_computations(target)
        if not contexts:
            continue

        dataframe = pd.DataFrame(contexts).sort_values(
            by=list(range(CONTEXT_SIZE - 1, -1, -1)),
            ignore_index=True,
        )
        print("CONTEXTS THAT LEAD TO THE TARGET:")
        print(dataframe)
        print()

        target_tag = "_".join(target.present)
        dataframe.to_csv(
            os.path.join(context_output_dir, f"contexts_to_{target_tag}.csv"),
            index=False,
            header=False,
        )


def main():
    global G
    G = nx.DiGraph(nx.nx_pydot.read_dot(DOT_PATH))
    print("LTS nodes:", len(G.nodes))
    print("LTS edges:", len(G.edges))

    export_target_contexts()
    dynamic_negative_slicing_analysis()


if __name__ == "__main__":
    main()
