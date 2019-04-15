import csv
import requests

from auth import user, passwd

FLAGS = None

def main(_):
    per = dict()
    with open(FLAGS.per, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            package, si, fp, cs, ll, rt, ps = row
            per[package] = [si, fp, cs, ll, rt, ps]

    with open(FLAGS.raw, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            package, s, si_raw, _, fp_raw, cs_raw, ll_raw, rt_raw = row
            ss, se = eval(s)
            si, fp, cs, ll, rt, ps = per[package]
            date = '2019-04-14'
            data = {'package_name': package,
                    'experiment_date': date,
                    'scene_start': ss,
                    'scene_end': se,
                    'raw_si': si_raw,
                    'raw_fp': fp_raw,
                    'raw_cs': cs_raw,
                    'raw_ll': ll_raw,
                    'raw_rt': rt_raw,
                    'ps': ps,
                    'per_si': si,
                    'per_fp': fp,
                    'per_cs': cs,
                    'per_ll': ll,
                    'per_rt': rt}
            r = requests.post(FLAGS.api, auth=(user, passwd), json=data)
            print(r.text)



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--raw')
    parser.add_argument('-p', '--per')
    parser.add_argument('-a', '--api')

    FLAGS, _ = parser.parse_known_args()

    main(_)

