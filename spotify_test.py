from flask import Flask, url_for, send_from_directory, render_template, request
import urllib2
import json
from urllib2 import HTTPError

app = Flask(__name__)


def create_url_html(method_name, link_text=None):
    if not link_text:
        link_text = method_name

    url = url_for(method_name)
    return "<li><a href='{}'>{}</a></li>".format(url, link_text)


@app.route('/')
def index():
    urls = "<ul>"
    urls += create_url_html('album_search', "Find an album")
    urls += create_url_html('artist_search', "Find an artist")
    urls += create_url_html('track_search', "Find a track")
    urls += "</ul>"
    return urls


@app.route('/artist/')
@app.route('/artist/<q>/')
@app.route('/artist/<q>/<page>/')
def artist_search(q=None, page=None):
    content = "<ul>{}</ul>".format(create_url_html("index", "Home"))
    content += generic_search("artist", "artists", q, page)
    return content


@app.route('/track/')
@app.route('/track/<q>/')
@app.route('/track/<q>/<page>/')
def track_search(q=None, page=None):
    content = "<ul>{}</ul>".format(create_url_html("index", "Home"))
    content += generic_search("track", "tracks", q, page)
    return content


@app.route('/album/')
@app.route('/album/<q>/')
@app.route('/album/<q>/<page>/')
def album_search(q=None, page=None):
    content = "<ul>{}</ul>".format(create_url_html("index", "Home"))
    content += generic_search("album", "albums", q, page)
    return content


def generic_search(url_keyword, json_key, q, page):
    if q is None:
        return "Please enter a search string, e.g. <a href='http://localhost:5678/{}/abba/'>http://localhost:5678/{}/abba/</a>".format(url_keyword, url_keyword)

    if page is None:
        get_all=True
    else:
        get_all=False

    base_url = "http://ws.spotify.com/search/1/{}.json?q={}".format(url_keyword, q)

    try:
        results, response_json_obj = get_all_items(url_keyword, json_key, base_url, get_all=get_all)
    except HTTPError:
        return "Bad Request: '{}'. Please try again.".format(q)

    results += "<ol>"
    for artist_line in sorted(response_json_obj[json_key], key=lambda artist: artist['popularity'], reverse=True):
        results += u"<li>{} ({})</li>".format(artist_line['name'], artist_line['popularity'])
    results += "</ol>"

    return results


def get_json_from_url(url):
    encoded_url = url.replace(" ", "+")
    print "# Querying url {}".format(encoded_url)

    req = urllib2.Request(encoded_url, headers = {})
    http_handler = urllib2.HTTPHandler()
    response_json = urllib2.urlopen(req).read()
    print "# Result: {}". format(response_json)

    return json.loads(response_json)


def get_all_items(url_keyword, json_key, base_url, get_all=True):
    url = "{}&page={}".format(base_url, 1)
    response_json = get_json_from_url(url)

    # print response_json['artists']
    # response_json['info']['num_results']  109467
    # response_json['info']['limit']        100
    # response_json['info']['offset']       0
    # response_json['info']['query']        The
    # response_json['info']['type']         artist
    # response_json['info']['page']         1

    num_results = response_json['info']['num_results']
    limit = response_json['info']['limit']
    offset = response_json['info']['offset']
    page = response_json['info']['page']
    search_string = response_json['info']['query']

    if response_json['info']['num_results'] > 1000:
        return ("Your search for '{}' returned {} results.  Showing first 100 results only.".format(search_string, num_results),
                response_json)

    print "num_results =", num_results, ", limit =", limit, ", offset =", offset, ", page =", page

    if not get_all or num_results<limit:
        if offset+1 > num_results:
            return("There is no page {} for this {} as there are only {} results.".format(page, url_keyword, num_results), response_json)
        elif num_results < limit:
            max = offset+num_results
        elif num_results < offset+limit:
            max = num_results
        else:
            max = offset+limit

        results = "Showing page {} of {} (Artists {}-{} of {})".format(page,
            num_results/max,
                                                                       offset+1,
                                                                       max,
                                                                       num_results)
    else:
        results = "Showing all {} results".format(num_results)
        page = 2
        total_results_returned = offset+limit
        while total_results_returned < num_results:
            url = "{}&page={}".format(base_url, page)
            response_json[json_key].extend(get_json_from_url(url)[json_key])
            total_results_returned += limit
            page = page+1

    return (results, response_json)


if __name__ == "__main__":
    """Start the server
    host  -- (default '127.0.0.1')
    port  -- (default 5000)
    debug -- set to True to reload every time a change is detected: very useful! (default False)

    """
    app.run(host='localhost', port=5678, debug=True)