"""
This script collects everything useful for generating a report

"""


# Generate report
def gen_q_report(q_idx, q_param, score=None, report=None, crash = False):
    msg = gen_q_sep()

    # Generate an informative heading of this query report
    msg += gen_q_heading(q_idx, q_param)

    # Generate a breakdown of the score
    if crash:
        msg += gen_crash_message()
    else:
        msg += gen_score_txt(score, report)

    return msg


def gen_crash_message():
    """
    Returns the message included in the report when no csv file was found

    :return:
    """
    msg = """
    Crash!\n
    No .csv file was generated for this query with these parameters.\n
    Please check the execution report for more runtime information.
    """

    return msg


def gen_q_heading(q_idx, q_param):
    """
    Generate the heading of a single-query report
    """

    q_msg = "Result for query: {:02d}\n\n".format(q_idx+1) #One-based indexing for fnames
    p_msg = gen_param_txt(q_param)

    q_head = q_msg + p_msg

    return q_head


def gen_param_txt(q_param):
    """
    From dict of query parameters, generate a summary text
    """

    # Initial message
    p_msg = "With parameters:\n"

    # Print q_param
    p_msg += print_dict(q_param)

    return p_msg


def gen_score_txt(score, report, crash = False):
    # Initial message
    s_msg = "Overall score: {}%\nBreakdown:\n".format(score * 100)

    # Print all the rest of the provided information
    s_msg += print_dict(report)

    return s_msg


def gen_q_sep():
    sep = "\n\n\n---  ---  --- -- ---  ---  ---\n\n"
    return sep


def print_dict(dict_to_print):
    """
    Formatted print of dictionary
    """

    assert type(dict_to_print) is dict

    # Init message
    msg = ""

    if len(set(dict_to_print)) > 0: # Otherwise crashes for empty dict

        # Generate template for formatting
        max_keylength = len(max(dict_to_print.keys(), key=len))
        template = "\t{0:" + str(max_keylength) + "} = {1}\n"

        for k, v in dict_to_print.items():
            msg += template.format(k, v)
    else:
        pass

    return msg