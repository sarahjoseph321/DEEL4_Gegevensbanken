"""
This script contains all methods necessary for running
a submission for the db18 project, provided if all
conventions were followed.
"""

import importlib.util as iu
import json
import pandas as pd

import basics as b
from fs_tools import *
from specs import gen_all_q_names, gen_all_q_method


# Actual execution
def prepare_execution(fname, mode=None):
    """
    From a given filename, deduce a filesystem and
    extract a module that contains the desired methods.
    """
    fs = create_fs(fname)

    if mode in {'solution', 'sol'}:
        fs['dir']['out'] = fs['dir']['sol']

    make_empty_dir(fs['dir']['out'])

    module = load_external_script(fs['file']['script'], mod_name=fs['identifier'])

    return fs, module


def before_execution(fname, all_q_colnam=None, all_q_params=None):
    fs, module = prepare_execution(fname)

    if all_q_colnam is None:
        all_q_colnam = json.load(open(fs['file']['all_q_colnam'], 'r'))
    if all_q_params is None:
        all_q_params = json.load(open(fs['file']['all_q_params'], 'r'))

    all_q_names = gen_all_q_names(len(set(all_q_colnam)))
    all_q_method = gen_all_q_method(module, all_q_names)

    return fs, all_q_names, all_q_method, all_q_colnam, all_q_params


def run_external_script(fname, connection, all_q_colnam=None, all_q_params=None):
    fs, all_q_names, all_q_method, all_q_colnam, all_q_params = before_execution(fname,
                                                                                 all_q_colnam,
                                                                                 all_q_params)

    run_all_queries(fs,
                    all_q_names,
                    all_q_method,
                    connection,
                    all_q_colnam,
                    all_q_params)
    return


# Running scripts
def load_external_script(fname, mod_name=None):
    """
    Import an external .py script as a module from which methods can be called.
    """

    mod_name = mod_name if mod_name is not None else "student_solution"  # Name the module

    spec = iu.spec_from_file_location(mod_name, fname)
    module = iu.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Add helper methods, since they are not explicitly in the script
    module.run_query = b.run_query
    module.res_to_df = b.res_to_df
    module.pd = pd

    return module


def run_single_function(q_method, connection, q_colnam, q_param, fname_csv):
    """
    Run the function f, and save the resulting pandas DataFrame to a csv

    :param q_method:        Function to be executed,
                                i.e.: a query as implemented in the
                                      external script
    :param connection:      Connection object to mysql database
    :param q_colnam:        Column names of the resulting dataframe
    :param q_param:         Parameter(s) (as dictionary) for q_method,
                                i.e.: parameters for the query
    :param fname_csv:       Filename of the resulting csv

    :return:
    """

    method_name = run_single_function.__name__

    try:
        df = q_method(connection, q_colnam, **q_param)
        save_df(df, fname_csv)

    except BaseException as error:
        print('Exception occurred in method {}:\n{}\n'.format(method_name, error))


def run_single_query(fs,
                     q_method,
                     connection,
                     q_colnam,
                     q_params,
                     q_idx=-1):
    """
    Run a single query.

    This means executing the submitted implementation of a given query,
    for each parameter settings that we provide. This function also immediately
    saves the results in the correct csv files.

    :param fs:              Filesystem dictionary
    :param q_method:        Method of the external script that runs the
                            desired query.
    :param q_params:        List of parameter dictionaries. We run the query for
                            each parameter dictionary.
    :param connection:      Connection object to the mysql database
    :param q_colnam:        Column names of the dataframe that
                            q_method/the query will generate
    :param q_idx:           Index of the query being executed
    :return:
    """

    for p_idx, param_dict in enumerate(q_params):
        fname_csv = gen_result_fname(fs, q_idx=q_idx, p_idx=p_idx)

        run_single_function(q_method,
                            connection,
                            q_colnam,
                            q_param=param_dict,
                            fname_csv=fname_csv)

    return


def run_all_queries(fs,
                    all_q_names,
                    all_q_method,
                    connection,
                    all_q_colnam,
                    all_q_params):
    """
    Run all queries (specified by all_q_names) in the external script.

    Queries not implemented in the external script, will not be present in
    all_q_method, and hence result in an error.

    :param fs:              Filesystem dictionary
    :param all_q_names:     List of names of the methods in the external script
                            that we want to run
    :param all_q_method:    Dict of methods in the external script that
                            correspond to queries we want to run. This dict
                            is composed on beforehand! If a method does not
                            exist in the external script, this dict will not
                            possess the corresponding key.
    :param connection:      Connection object to the mysql database
    :param all_q_colnam:    Dict of all the column names for each query
    :param all_q_params:    Dict of lists of dicts of parameters.
    :return:
    """
    method_name = run_all_queries.__name__

    for q_idx, q_name in enumerate(all_q_names):
        try:
            q_colnam = all_q_colnam[q_name]
            q_method = all_q_method[q_name]
            q_params = all_q_params[q_name]

            run_single_query(fs,
                             q_method,
                             connection,
                             q_colnam,
                             q_params,
                             q_idx=q_idx)

        except BaseException as error:
                print('An exception occurred in method {}:\n{}\n'.format(method_name,error))
    return


# Saving csv
def save_df(df, fname):
    """
    Save dataframe to csv file

    :param df:
    :param fname:
    :return:
    """
    df.to_csv(fname, index=False)
    return
