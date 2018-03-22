"""
This file contains methods to automatically

1. Generate query names
2. Generate query parameters
3. Extract specific queries from a sumitted python file

"""


def gen_all_q_names(nb_queries=10):
    """
    Generate list of query names
    """
    return [gen_q_name(i) for i in range(nb_queries)]


def gen_q_name(q_idx):
    res = "query_{:02d}".format(q_idx+1) # One-based indexing
    return res


def gen_all_q_method(module, all_q_names):
    """
    Extract the desired methods from the given module

    These 'desired methods' are specified by the q_names
    """
    all_q_method = {}
    for q_name in all_q_names:
        try:
            print("Loading method: {} from module {}".format(q_name, module.__name__))
            all_q_method[q_name] = getattr(module, q_name)
        except BaseException as error:
            method_name = gen_all_q_method.__name__
            print('An exception occurred in method {}:\n{}\n'.format(method_name, error))
    return all_q_method


def gen_all_q_colnam(all_q_names):
    """
    Generate a dict containing all the column names of the solution dataframes.
    """

    all_q_colnam = {}
    all_q_colnam[all_q_names[0]] = ['tname', 'HomeRun']
    all_q_colnam[all_q_names[1]] = ['nameFirst', 'nameLast', 'birthYear', 'birthMonth', 'birthDay']
    all_q_colnam[all_q_names[2]] = ['nameFirst', 'nameLast', 'tname']
    all_q_colnam[all_q_names[3]] = ['tname', 'rank', 'W', 'L', 'nameFirst', 'nameLast']
    all_q_colnam[all_q_names[4]] = ['tname']
    all_q_colnam[all_q_names[5]] = ['tname', 'yearID', 'rank', 'W', 'L']
    all_q_colnam[all_q_names[6]] = ['nameLast', 'nameFirst']
    all_q_colnam[all_q_names[7]] = ['birthState', 'avg_weight', 'avg_height', 'avg_HomeRun', 'avg_Saves']
    all_q_colnam[all_q_names[8]] = ['yearID', 'tname', 'HomeRun']
    all_q_colnam[all_q_names[9]] = ['yearID', 'tname', 'rank', 'Games']

    assert len(set(all_q_colnam)) == len(all_q_names)

    return all_q_colnam


def gen_all_q_params(all_q_names = None):

    if all_q_names is None:
        all_q_names = gen_all_q_names() # Assuming default situation

    all_q_params = {}

    # Query 1
    q_01_p_01 = {}

    all_q_params[all_q_names[0]] = [q_01_p_01]

    # Query 2
    q_02_p_01 = {'datum': '1980-01-16'}
    q_02_p_02 = {'datum': '1985-01-16'}

    all_q_params[all_q_names[1]] = [q_02_p_01, q_02_p_02]

    # Query 3
    q_03_p_01 = {}

    all_q_params[all_q_names[2]] = [q_03_p_01]

    # Query 4
    q_04_p_01 = {'datum_x': '1980-01-01',
                 'datum_y': '1980-01-01'}
    q_04_p_02 = {'datum_x': '2000-01-01',
                 'datum_y': '2001-01-01'}

    all_q_params[all_q_names[3]] = [q_04_p_01, q_04_p_02]

    # Query 5
    q_05_p_01 = {}

    all_q_params[all_q_names[4]] = [q_05_p_01]

    # Query 6
    q_06_p_01 = {'salaris': 20000}
    q_06_p_02 = {'salaris': 40000}
    q_06_p_03 = {'salaris': 60000}

    all_q_params[all_q_names[5]] = [q_06_p_01, q_06_p_02, q_06_p_03]

    # Query 7
    q_07_p_01 = {}

    all_q_params[all_q_names[6]] = [q_07_p_01]

    # Query 8
    q_08_p_01 = {'jaar': 1990,
                 'max_lengte': 75}
    q_08_p_02 = {'jaar': 2010,
                 'max_lengte': 60}

    all_q_params[all_q_names[7]] = [q_08_p_01, q_08_p_02]

    # Query 9
    q_09_p_01 = {'jaar': 1990}
    q_09_p_02 = {'jaar': 1995}
    q_09_p_03 = {'jaar': 2010}

    all_q_params[all_q_names[8]] = [q_09_p_01, q_09_p_02, q_09_p_03]

    # Query 10
    q_10_p_01 = {'jaar': 1968}
    q_10_p_02 = {'jaar': 1989}
    q_10_p_03 = {'jaar': 2001}

    all_q_params[all_q_names[9]] = [q_10_p_01, q_10_p_02, q_10_p_03]

    assert len(set(all_q_params)) == len(all_q_names)

    return all_q_params