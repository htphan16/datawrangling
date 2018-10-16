"""
To experiment with this code freely you will have to run this code locally.
Take a look at the main() function for an example of how to use the code. We
have provided example json output in the other code editor tabs for you to look
at, but you will not be able to run any queries through our UI.
"""
import json
import requests
import pprint as pp

BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"


# query parameters are given to the requests.get function as a dictionary; this
# variable contains some starter parameters.
query_type = {  "simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {'limit': 100, 'page': 2, "inc": "releases"},
                "recordings": {'limit': 100, 'page': 2, "inc": "recordings"},
                "works": {'limit': 100, 'page': 2, "inc": "works"}
                }


def query_site(url, params, uid='', fmt="json"):
    """
    This is the main function for making queries to the musicbrainz API. The
    query should return a json document.
    """
    params["fmt"] = fmt

    r = requests.get(url + uid, params=params)
    print("requesting", r.url)
    print(r)
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    """
    This adds an artist name to the query parameters before making an API call
    to the function above.
    """
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    """
    After we get our output, we can use this function to format it to be more
    readable.
    """
    if type(data) == dict:
        print(json.dumps(data, indent=indent, sort_keys=True))
    else:
        print(data)


def main():
    """
    Below is an example investigation to help you get started in your
    exploration. Modify the function calls and indexing below to answer the
    questions on the next quiz.

    HINT: Note how the output we get from the site is a multi-level JSON
    document, so try making print statements to step through the structure one
    level at a time or copy the output to a separate output file. Experimenting
    and iteration will be key to understand the structure of the data!
    """

    # Query for information in the database about bands
    results = query_by_name(ARTIST_URL, query_type["simple"], "Nirvana")
    print(results)
    # Isolate information from the 4th band returned (index 3)
    print("\nARTIST:")
    pretty_print(results["artists"][4]['disambiguation'])

    # Query for releases from that band using the artist_id
    artist_id = results["artists"][0]["id"]
    artist_data = query_site(ARTIST_URL, query_type["releases"], artist_id)

    releases = artist_data["releases"]

    # Print information about releases from the selected band
    print("\nONE RELEASE:")
    pretty_print(releases[0], indent=2)

    release_titles = [r["title"] for r in releases]
    print("\nALL TITLES:")
    for t in release_titles:
        print(t)

    artist_recordings = query_site(ARTIST_URL, query_type["recordings"], artist_id)
    recordings_titles = [r["title"] for r in artist_recordings['recordings']]
    print(recordings_titles)

    artist_aliases = query_site(ARTIST_URL, query_type["aliases"], artist_id)
    aliases = [r["name"] for r in artist_aliases['aliases']]
    print(aliases)

    artist_works = query_site(ARTIST_URL, query_type["works"], artist_id)
    works_titles = [r["title"] for r in artist_works['works']]
    print(works_titles)

if __name__ == '__main__':
    main()