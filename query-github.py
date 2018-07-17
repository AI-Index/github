"""
Scrap Github for statistics on several repositories of interest
https://www.python-boilerplate.com/py3+argparse

Requires a Github API token to use.
"""
import argparse
import csv
from github import Github

# May be used later for additional detailed stats
# each may be called on a repository object
# methods = [
#     'get_stargazers',
#     'get_stargazers_with_dates',
#     'get_stats_code_frequency',
#     'get_stats_commit_activity',
#     'get_stats_contributors',
#     'get_stats_participation',
#     'get_stats_punch_card',
#     'get_subscribers',
#     'get_tags',
#     'get_teams',
#     'get_watchers',
# ]

# Pieces of information we want to retrieve for each repository
info = [
    'name',
    'homepage',
    'created_at',
    'default_branch',
    'description',
    'forks_count',
    'id',
    'language',
    'last_modified',
    'size',  # KB - Approximate
    'stargazers_count',
    'subscribers_count',
]

# Repositories we want to track
# See https://arxiv.org/pdf/1803.04818.pdf for a larger list
repos = [
    'pytorch/pytorch',
    'tensorflow/tensorflow',
    'tensorflow/tfjs',
    'scikit-learn/scikit-learn',
    'BVLC/caffe',
    'keras-team/keras',
    'Microsoft/CNTK',
    'PaddlePaddle/Paddle',
    'apache/incubator-mxnet',
    'Theano/Theano',
    'deeplearning4j/deeplearning4j',  # New monorepo
    'chainer/chainer',
]


def main(args):
    # Auth with access token
    g = Github(args.token)

    filename = 'github-data.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Full Name'] + info)
        for r_name in repos:
            r = g.get_repo(r_name)
            row_data = [r_name]
            for i in info:
                row_data.append(getattr(r, i))
            writer.writerow(row_data)

    print('Done writing to {}'.format('github-data.csv'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--token", action="store", dest="token")

    args = parser.parse_args()
    main(args)