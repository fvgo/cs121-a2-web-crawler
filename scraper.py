import re
from urllib.parse import urlparse

# taken from the read me :

def scraper (url: str, resp: utils.response.Response) -> list:
    """
    (This is the meat of the crawler) Implement the scraper function in scraper.py. 
    
    The scraper function receives a URL and corresponding Web response (for example, the 
    first one will be "http://www.ics.uci.edu" and the Web response will contain the page 
    itself). Your task is to parse the Web response, extract enough information from the 
    page (if it's a valid page) so as to be able to answer the questions for the report, 
    and finally, return the list of URLs "scrapped" from that page. 
    
    Some important notes:
    - Make sure to return only URLs that are within the domains and paths mentioned above! 
    (see is_valid function in scraper.py -- you need to change it)

    - Make sure to defragment the URLs, i.e. remove the fragment part.

    - You can use whatever libraries make your life easier to parse things. Optional dependencies 
    you might want to look at: BeautifulSoup, lxml (nudge, nudge, wink, wink!)
        https://beautiful-soup-4.readthedocs.io/en/latest/
        https://lxml.de/


    Optionally, in the scraper function, you can also save the URL and the web page on 
    your local disk.

    @param url: the URL that was added to the frontier, and downloaded from the cache.
    It is of type str and was an url that was previously added to the
    frontier.

    @param resp: the response given by the caching server for the requested URL.
    The response is an object of type Response (see utils/response.py)
    """
    pass
    # NOTE: same function as below?? but readme.md was more specific with the
    # return type and parameter requirements

    


######

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    return list()

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
