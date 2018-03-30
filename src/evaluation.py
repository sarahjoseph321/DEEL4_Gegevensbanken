"""
This script contains all methods necessary for evaluation
of csv s corresponding to outputs for the queries.
"""
import json
import pandas as pd
from fs_tools import *
from specs import *
from reports import *


# Full evaluation
def evaluate_script(script_fname, all_q_params = None):
    fs = create_fs(script_fname)
    if all_q_params is None:
        all_q_params = json.load(open(fs['file']['all_q_params'], 'r'))

    sol_dir = fs['dir']['sol']
    out_dir = fs['dir']['out']

    sol_dfs = extract_dfs_from_dir(sol_dir)
    out_dfs = extract_dfs_from_dir(out_dir)

    assert set(sol_dfs) >= set(out_dfs)
    mutual_keys = list(set(sol_dfs) & set(out_dfs))
    mutual_keys.sort()

    scores = {}
    report = {}
    full_report = ""

    sol_keys = list(set(sol_dfs))
    sol_keys.sort()
    for k in sol_keys:

        q_idx, p_idx = gen_idx_from_appendix(k)
        q_param = extract_q_param(all_q_params, q_idx, p_idx)

        if k in mutual_keys:
            df_true = sol_dfs[k]
            df_subm = out_dfs[k]

            scores[k], report[k] = evaluate_df(df_true, df_subm)

            full_report += gen_q_report(q_idx, q_param, score=scores[k], report=report[k])
        else:
            full_report += gen_q_report(q_idx, q_param, crash=True)

    return full_report


def extract_q_param(all_q_params, q_idx, p_idx):
    """
    Reverse operation
    """
    q_name = gen_q_name(q_idx)

    return all_q_params[q_name][p_idx]


# Load csv from disk
def load_df(fname):
    return pd.read_csv(fname)


def extract_dfs_from_dir(folder):
    """
    Collect relevant .csv files into DataFrames

    Given a certain folder, we extract the
    relevant .csv files and load them into dataframes.

    The dataframes are saved in a dictionary, the encoded part
    of the filename (e.g., q_02_p_01) i extracted as keys.
    """

    csv_files = [f for f in os.listdir(folder) if f.endswith('.csv')]
    csv_files.sort()
    keys = [extract_appendix_from_fname(fname) for fname in csv_files]

    keys_files = zip(keys, csv_files)
    dfs = {}

    for k, f in keys_files:
        full_fname = os.path.join(folder, f)
        dfs[k] = load_df(full_fname)

    return dfs


# Score two DataFrames
def evaluate_df(df_true, df_subm):
    """
    Score submitted dataframe wrt the true dataframe

    Policy:
        - If everything is perfect, 100%
        - Else, we look at the F1 score. This score takes into account
          whether the submitted solution contains everything it should,
          while it also penalizes including too much records.
          We then multiply this by 0.9, since the F1 score does not take
          the order into account. If you got everything correct, but forgot
          to order, you obtain a score of 90%.
    """

    score, report = f1_dfs(df_true, df_subm)

    if score == 1 & is_sorted(df_true, df_subm):
        report = {'Perfect match': 'Congratulations!'}
    else:
        score *= 0.9

    return score, report


def f1_dfs(df_true, df_subm):
    """
    Computes the F1 score of the submitted DataFrame compared to true DataFrame
    """

    # Convert NULL/ NaN to 0, otherwise our TP/FP/FN go haywire.
    df_true = df_true.fillna(0)
    df_subm = df_subm.fillna(0)

    # Convert to sets
    true_set = get_set_of_tuples(df_true)
    subm_set = get_set_of_tuples(df_subm)

    # Calculate F1 score
    TP, FP, FN = tp_fp_fn(true_set, subm_set)

    precision = calc_precision(TP, FP)
    recall = calc_recall(TP, FN)

    F1 = calc_f1(precision, recall)

    report = compile_report_dict(TP, FP, FN, precision, recall, F1)

    return F1, report


def is_sorted(df_true, df_subm):
    """
    A rough check to see if a DataFrame is sorted.

    This check is only conducted whenever a perfect F1 score is
    achieved. Therefore, at least the relative order of the first and
    last tuple returned in the submission should be consistent with the
    one provided in the solution.

    Albeit rough, since this happens if and only if a perfect F1 score has been
    achieved, it should suffice.
    """

    first_tuple_subm = tuple(df_subm.values[0])
    final_tuple_subm = tuple(df_subm.values[-1])

    check = idx_tuple_in_df(first_tuple_subm, df_true) < idx_tuple_in_df(final_tuple_subm, df_true)
    return check


def tp_fp_fn(true_set, subm_set):
    """
    Calculate TP, FP and FN when comparing the true set of tuples and
    the submitted set of tuples by the students.
    """

    true_pos = true_set.intersection(subm_set)
    fals_pos = subm_set - true_set
    fals_neg = true_set - subm_set

    TP = len(true_pos)
    FP = len(fals_pos)
    FN = len(fals_neg)

    return TP, FP, FN


def calc_precision(TP, FP):
    """
    Calculate precision from TP and FP
    """

    if TP + FP != 0:
        precision = TP / (TP + FP)
    else:
        precision = 0
    return precision


def calc_recall(TP, FN):
    """
    Calculate recall from TP and FN
    """
    if TP + FN != 0:
        recall = TP / (TP + FN)
    else:
        recall = 0
    return recall


def calc_f1(precision, recall):
    """
    Calculate F1 from precision and recall
    """
    if (precision + recall) != 0:
        F1 = 2 * (precision * recall) / (precision + recall)
    else:
        F1 = 0
    return F1


def compile_report_dict(TP, FP, FN, precision, recall, F1):
    """
    Generate a dictionary of all the metrics, to be used to generate a report.
    """
    remark = """
    Your result was not a perfect match. Therefore your score is calculated as (F1*0.9).
    If you had a perfect F1 score, this means that you returned all tuples perfectly,
    but forgot to order them.
    """

    res = {'TP': TP,
           'FP': FP,
           'FN': FN,
           'precision': precision,
           'recall': recall,
           'F1': F1,
           'Remark': remark}
    return res


def idx_tuple_in_df(tuple_x, df):
    """
    Find the first row index of tuple_x in df

    """
    for i,v in enumerate(df.values):
        if tuple_x == tuple(v):
            res = i
            break
        else:
            res=None
    return res


def get_set_of_tuples(df):
    """
    Converts DataFrame to set of tuples.

    Set conversion ensures that order does not matter anymore.
    """
    set_of_tuples = set(tuple(line) for line in df.values)
    return set_of_tuples


