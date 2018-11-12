"""
Scrap Github star history of given repository.

Requires a Github API token to use.
"""
import csv
import pandas as pd
from github import Github


def year_month(ser):
    keys = ["{}-{}".format(dt.year, dt.month) for dt in ser]
    return keys


def scrape(repo_name, token):
    # Auth with access token
    g = Github(token)
    # Grab the repo in question
    r = g.get_repo(repo_name)
    # Get a handle to the paginated list of stargazers
    stargazers = r.get_stargazers_with_dates()
    star_dates = []
    # Iterate over the paginated list (which will make API calls in the background as needed)
    for sg in stargazers:
        ts = sg.starred_at
        star_dates.append(ts)

    # Group those stargazers by when they starred the repo and get counts by month
    df = pd.DataFrame({'date': star_dates})
    group_list = year_month(df["date"])
    counts = df.groupby(group_list).count()
    sorted_counts = counts.sort_index()

    # Format for output
    indices = sorted_counts.index.values
    years, months = zip(*[x.split("-") for x in indices])
    vals = sorted_counts["date"].tolist()
    rows = list(zip(years, months, vals))

    # Write to csv
    safe_name = repo_name.replace("/", "-")
    filename = "{}-github-star-history.csv".format(safe_name)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

    print('Done writing to {}'.format(filename))


if __name__ == '__main__':
    token = 'INVALID TOKEN'
    repo_name = 'INVALID REPO'
    scrape(repo_name, token)
