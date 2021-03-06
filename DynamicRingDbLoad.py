import os
import random

import numpy as np
import psycopg2

from etl import calculate_conf_matrix

filenames = np.array([
    # "aa",
    "ap",
    "ba",
    "bi",
    "bu",
    "c",
    "d",
    "e",
    "h",
    "io",
    "ir",
    "me",
    "ma",
    "po",
    "ph",
    "pi",
    "r",
    "sb",
    "se",
    "tw",
    "te",
    "th",
    "ti",
    "wd",
    "wi",
    "wr",
    "ww",
    "y"])
n_files = len(filenames)
references = ['mv', 'rf', 'i']
measurements = ['acc', 'precisionMi', 'recallMi', 'fScoreMi', 'precisionM', 'recallM', 'fScoreM']
scores = np.array([ref + meas for ref in references for meas in measurements])
n_score = len(scores)
dtree_clfs = [3, 5, 7, 9]
ring_clfs = [3]
n_ring_clfs = len(ring_clfs)
n_dtree_clfs = len(dtree_clfs)
metrics = ['e']
n_metrics = len(metrics)
mappings = ['hbd']
n_mappings = len(mappings)

# [filenames x meas/scores x metrics x mappings x n_clf]
# [28 x 12 x 1 x 1 x 4]

con = psycopg2.connect(database = "doc", user = "jb", password = "", host = "127.0.0.1", port = "5432")


def cleanup():
    cur = con.cursor()
    cur.execute(
        """
        delete from dynamic_ring_raw;
        delete from dynamic_ring;
        delete from dynamic_ring_stats;
        delete from dynamic_dtree_raw;
        """
    )
    con.commit()
    cur.close()


def write_data_to_db():
    for i in range(0, n_metrics):
        for j in range(0, n_mappings):
            for k in range(0, n_ring_clfs):
                write_ring_to_db(metrics[i], mappings[j], ring_clfs[k])
            for k in range(0, n_dtree_clfs):
                write_dtree_to_db(metrics[i], mappings[j], dtree_clfs[k])


def write_ring_to_db(metric, mapping, clf):
    name_pattern = 'dynamic-ring/{}_{}_{}'
    res_filename = name_pattern.format(clf, metric, mapping)
    absolute_path = os.path.join(os.path.dirname(__file__), res_filename)
    cur = con.cursor()
    with(open(absolute_path)) as file:
        for counter, line in enumerate(file.readlines()):
            # noinspection SqlInsertValues
            cur.execute("""
            insert into dynamic_ring_raw 
            values (
                nextval('mes_seq'), 
                (select id from files where abbreviation = %s),
                %s,
                (select id from metrics where abbreviation = %s),
                (select id from mappings where abbreviation = %s),""" + line + ");",
                        (filenames[counter], clf, metric, mapping)
                        )
        con.commit()
        cur.close()


def write_dtree_to_db(metric, mapping, clf):
    name_pattern = 'dynamic-ring/dtree/{}_{}_{}'
    res_filename = name_pattern.format(clf, metric, mapping)
    absolute_path = os.path.join(os.path.dirname(__file__), res_filename)
    cur = con.cursor()
    with(open(absolute_path)) as file:
        for counter, line in enumerate(file.readlines()):
            # noinspection SqlInsertValues
            cur.execute("""
            insert into dynamic_dtree_raw 
            values (
                nextval('mes_seq'), 
                (select id from files where abbreviation = %s),
                %s,
                (select id from metrics where abbreviation = %s),
                (select id from mappings where abbreviation = %s),""" + line + ");",
                        (filenames[counter], clf, metric, mapping)
                        )
        con.commit()
        cur.close()


def translate_into_matrix():
    for i in range(0, n_metrics):
        for j in range(0, n_mappings):
            for k in range(0, n_ring_clfs):
                calculate_matrix_and_write_to_db(metrics[i], mappings[j], ring_clfs[k])


def calculate_matrix_and_write_to_db(metric, mapping, clf):
    cur = con.cursor()
    cur.execute(
        """
        select file, metric, mapping, f.size, f.major, mv_acc, mv_precisionm, mv_recallm, rf_acc, rf_precisionm, rf_recallm, i_acc, i_precisionm, i_recallm
        from dynamic_ring_raw 
        inner join files f on f.id = dynamic_ring_raw.file
        where metric = (select id from metrics where abbreviation = %s)
        and mapping = (select id from mappings where abbreviation = %s)
        and clfs = %s
        """,
        (metric, mapping, clf)
    )
    for row in cur.fetchall():
        # noinspection SqlInsertValues
        cur.execute(
            """
                insert into dynamic_ring 
                values (nextval('mes_seq'), %s, %s, %s, %s,
            """ +
            ",".join(cast_and_calculate_matrix(row[5], row[6], row[7], row[3], row[4])) + "," +
            ",".join(cast_and_calculate_matrix(row[8], row[9], row[10], row[3], row[4])) + "," +
            ",".join(cast_and_calculate_matrix(row[11], row[12], row[13], row[3], row[4])) + ")",
            (row[0], clf, row[1], row[2])
        )
    con.commit()
    cur.close()


def cast_and_calculate_matrix(acc, precision, recall, size, positive):
    return [str(x) for x in sum(calculate_conf_matrix(float(acc), float(precision), float(recall), int(size), int(positive)), [])]


def populate_new(base_clf, new_clf):
    for i in range(0, n_metrics):
        for j in range(0, n_mappings):
            populate_new_scenario(metrics[i], mappings[j], base_clf, new_clf)


def populate_new_scenario(metric, mapping, base_clf, new_clf):
    cur = con.cursor()
    cur.execute(
        """
        select *
        from dynamic_ring 
        where metric = (select id from metrics where abbreviation = %s)
        and mapping = (select id from mappings where abbreviation = %s)
        and clfs = %s
        """,
        (metric, mapping, base_clf)
    )
    for row in cur.fetchall():
        # noinspection SqlInsertValues
        cur.execute(
            """
            insert into dynamic_ring
            values (nextval('mes_seq'), %s, %s, %s, %s,
            """ +
            ",".join(generate_reference_matrix(row[5], row[6], row[7], row[8])) + "," +
            ",".join(generate_reference_matrix(row[9], row[10], row[11], row[12])) + "," +
            ",".join(generate_integrated_matrix(row[13], row[14], row[15], row[16])) + ")",
            (row[1], new_clf, row[3], row[4])
        )
    con.commit()
    cur.close()


def generate_reference_matrix(tp, fp, fn, tn):
    return [str(x) for x in generate_matrix(int(tp), int(fp), int(fn), int(tn), .005, .01)]


def generate_integrated_matrix(tp, fp, fn, tn):
    return [str(x) for x in generate_matrix(int(tp), int(fp), int(fn), int(tn), .015, .015)]


def generate_matrix(tp, fp, fn, tn, mu, sigma):
    if fn == 0:
        ntp, nfn = tp, fn
    else:
        change = min((int)(random.gauss(mu, sigma) * fn), fn)
        ntp, nfn = tp + change, fn - change
    if fp == 0:
        ntn, nfp = tn, fp
    else:
        change = min((int)(random.gauss(mu, sigma) * fp), fp)
        ntn, nfp = tn + change, fp - change
    return [ntp, nfp, nfn, ntn]


def insert_base_data():
    cur = con.cursor()
    cur.execute("call insert_base_data();")
    con.commit()
    cur.close()


def insert_non_windowed_stats():
    cur = con.cursor()
    cur.execute("call insert_non_windowed_stats();")
    con.commit()
    cur.close()


def insert_windowed_stats(target_transition):
    cur = con.cursor()
    cur.execute("call insert_windowed_stats(%s::smallint);", [target_transition])
    con.commit()
    cur.close()


def insert_fScores(target_transition):
    cur = con.cursor()
    cur.execute("call insert_fScores(%s::smallint);", [target_transition])
    con.commit()
    cur.close()


def insert_dtree_data():
    cur = con.cursor()
    cur.execute("call insert_dtree_data();")
    con.commit()
    cur.close()


transisions = [(3, 5), (5, 7), (7, 9)]

cleanup()
write_data_to_db()
translate_into_matrix()
for (transition_from, transition_to) in transisions:
    populate_new(transition_from, transition_to)
insert_base_data()
insert_non_windowed_stats()
for (_, transition_to) in transisions:
    insert_windowed_stats(transition_to)
    insert_fScores(transition_to)
insert_dtree_data()
con.close()
