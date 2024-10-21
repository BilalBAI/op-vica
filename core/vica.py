import pandas as pd
import numpy as np
import random

from data_processor import process_data

import rpy2.robjects as ro
import rpy2.robjects.pandas2ri as pandas2ri
# Load R VICA modules
ro.r['source']('./vica.R')

proposal_filter = ro.globalenv['proposal_filter']
final_voting_result = ro.globalenv['final_voting_result']
proposal_result_merge = ro.globalenv['proposal_result_merge']
Similar_matriix = ro.globalenv['Similar_matriix']
Community_detection = ro.globalenv['Community_detection']
Logistic_reg_single = ro.globalenv['Logistic_reg_single']
Logistic_reg_multiple = ro.globalenv['Logistic_reg_multiple']
CT_Logistic_reg_single = ro.globalenv['CT_Logistic_reg_single']
CT_fun = ro.globalenv['CT_fun']
CT_Logistic_reg_multiple = ro.globalenv['CT_Logistic_reg_multiple']
Centrality_statistics = ro.globalenv['Centrality_statistics']
# ro.r('install.packages("", repos="https://cloud.r-project.org")')


def process_data_and_convert_to_r(df_token_house_top_200, df_citizen_house, df_summary):
    print("-------- Process Data and Convert to R -------- ")
    # further process data and convert to r
    prop_token_t = df_token_house_top_200[df_token_house_top_200['voted_choice'].isin([
        'FOR', 'AGAINST'])]
    prop_cit_t = df_citizen_house[df_citizen_house['voted_choice'].isin([
                                                                        'FOR', 'AGAINST'])]
    voting_res_filter = df_summary[df_summary['proposal_choice'].isin([
        'FOR', 'AGAINST'])]
    # activate pandas-to-R convertion
    pandas2ri.activate()

    # convert pandas DataFrame to R data.frame
    prop_token_t = pandas2ri.py2rpy(prop_token_t)
    prop_cit_t = pandas2ri.py2rpy(prop_cit_t)
    voting_res_filter = pandas2ri.py2rpy(voting_res_filter)

    # The dataframe is available in R now.
    # Pass the converted R object into the R environment
    ro.globalenv['prop_token_t'] = prop_token_t
    ro.globalenv['prop_cit_t'] = prop_cit_t
    ro.globalenv['voting_res_filter'] = voting_res_filter

    # Filter out the addresses with fewer participations in proposal_csv.
    prop_token_filter_t = proposal_filter(prop_token_t, 5)
    prop_cit_filter_t = proposal_filter(prop_cit_t, 5)

    voting_res_filter_final_t = final_voting_result(voting_res_filter)

    # Organize the final voting results and add them to the original data
    # Since there are two rows of data for each proposal_id in the voting res filter,
    # representing the votes for 'For' and 'Against,'
    # we now need to compare the numbers and reach a final conclusion.

    prop_token_filter_add_t = proposal_result_merge(
        voting_res_filter_final_t, prop_token_filter_t)

    prop_cit_filter_add_t = proposal_result_merge(
        voting_res_filter_final_t, prop_cit_filter_t)
    print('Success\n')
    return (prop_token_filter_t, prop_cit_filter_t,
            prop_token_filter_add_t, prop_cit_filter_add_t)


def run_vica_single(proposals_votes, proposals_votes_add):
    # run VICA model for a single entity
    # Calculate the similarity matrix
    print("Calculate the similarity matrix")
    M_tranc = Similar_matriix(proposals_votes_add, 3)
    # # Save the array
    # np.save('M_tranc.npy', M_tranc)
    # # Load the array back into memory
    # M_tranc = np.load('M_tranc.npy')

    print("Community detection")
    # Community detection
    random.seed(1)
    community = Community_detection(M_tranc, 0.1, 3)

    # Assign the group information to Louvain_member
    Louvain_member = community[1]

    print("Logistic Regression")
    # Logistic Regression
    log_eff = Logistic_reg_single(
        proposals_votes_add, Louvain_member, False)
    ad_log_eff = Logistic_reg_single(
        proposals_votes_add, Louvain_member, True)

    print("Counterfactual Logistic Regression")
    # Counterfactual Logistic Regression
    log_eff_rev = CT_Logistic_reg_single(
        proposals_votes, Louvain_member, False)
    ad_log_eff_rev = CT_Logistic_reg_single(
        proposals_votes, Louvain_member, True)
    print('Success\n')
    return {
        "similarity_matrix": M_tranc,
        "community_detection": community,
        "louvain_member": Louvain_member,
        "logistic_regression": {
            "factual": {
                "logit_effect": log_eff,
                "adjusted_logit_effect": ad_log_eff,
            },
            "counterfactual": {
                "logit_effect": log_eff_rev,
                "adjusted_logit_effect": ad_log_eff_rev,
            }
        }}


def run_vica_multiple(proposals_votes_1, proposals_votes_2,
                      proposals_votes_add_1, proposals_votes_add_2):
    # Logistic Regression
    print("Logistic Regression")
    log_eff_both_t = Logistic_reg_multiple(
        proposals_votes_add_1, proposals_votes_add_2)
    # Counterfactual Logistic Regression
    log_eff_both_rev_t = CT_Logistic_reg_multiple(
        proposals_votes_1, proposals_votes_2)
    print('Success\n')
    return {
        "logistic_regression": {
            "factual": {
                "logit_effect": log_eff_both_t,
            },
            "counterfactual": {
                "logit_effect": log_eff_both_rev_t,
            }
        }}


def run_vica_all(prop_token_filter, prop_cit_filter, prop_token_filter_add, prop_cit_filter_add):
    # run VICA model
    print("-------- Run Token House -------- ")
    token_house = run_vica_single(prop_token_filter, prop_token_filter_add)
    print("-------- Run Citizen House -------- ")
    citizen_house = run_vica_single(prop_cit_filter, prop_cit_filter_add)
    print("-------- Run Both Houses -------- ")
    both_houses = run_vica_multiple(prop_token_filter, prop_cit_filter,
                                    prop_token_filter_add, prop_cit_filter_add)
    return {
        "token_house": token_house,
        "citizen_house": citizen_house,
        "both_houses": both_houses,
    }


def results_to_df(results: dict, date='2024-07-01'):
    # run summary statistics for vica results
    df_re = pd.DataFrame(
        columns=['entity', 'scenario_type', 'regression_type', 'value'])

    for h in results.keys():
        for i in results[h]['logistic_regression'].keys():
            for j in results[h]['logistic_regression'][i].keys():
                log_reg_eff = results[h]['logistic_regression'][i][j]
                temp = pd.DataFrame(log_reg_eff, columns=['value'])
                # lable and concat to df_re
                temp['entity'] = h
                temp['scenario_type'] = i
                temp['regression_type'] = j
                df_re = pd.concat([df_re, temp], axis=0)
    df_re['Date'] = date
    return df_re


def run_stats(results: dict, date='2024-07-01'):
    # run summary statistics for vica results
    df_stats = pd.DataFrame()

    for h in results.keys():
        for i in results[h]['logistic_regression'].keys():
            for j in results[h]['logistic_regression'][i].keys():
                # remove na and run Centrality_statistics
                log_reg_eff = results[h]['logistic_regression'][i][j]
                stats = Centrality_statistics(
                    log_reg_eff[~np.isnan(log_reg_eff)])
                # convert from R to Py DataFrame
                pandas2ri.activate()
                temp = pandas2ri.rpy2py(stats)
                # lable and concat to df_stats
                temp['Entity'] = h
                temp['Scenario_Type'] = i
                temp['Regression_Type'] = j
                df_stats = pd.concat([df_stats, temp], axis=0)
    df_stats['Date'] = date
    return df_stats


def run():
    # Process from raw data (only if raw data has been updated)
    df_token_house_top_200, df_citizen_house, df_summary = process_data()

    # further process data and convert to R
    (prop_token_filter, prop_cit_filter, prop_token_filter_add,
     prop_cit_filter_add) = process_data_and_convert_to_r(df_token_house_top_200, df_citizen_house, df_summary)

    # run VICA
    results_dict = run_vica_all(
        prop_token_filter, prop_cit_filter, prop_token_filter_add, prop_cit_filter_add)

    # Get states
    df_stats = run_stats(results_dict)

    return results_dict, df_stats


if __name__ == "__main__":
    run()
