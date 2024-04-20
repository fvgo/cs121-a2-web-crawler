import re
from urllib.parse import urlparse
import urllib.robotparser  # parse robots.txt file

# new imports for attempt at extract_next_links implementation
from bs4 import BeautifulSoup
from urlparse import urldefrag

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
        https://realpython.com/beautiful-soup-web-scraper-python/
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

    # VVVV attempt at using beautifulsoup [has not been tested]

    hyperlinks_list = list()

    # ref: https://realpython.com/beautiful-soup-web-scraper-python/
        # URL = "https://realpython.github.io/fake-jobs/"
        # page = requests.get(URL)
        # soup = BeautifulSoup(page.content, "html.parser")

    if (resp.status == 200):    # status code indicates you got the page

        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')  # parse html content

        # find all '<a>' tags (hyperlinks) with 'href' attribute
        for hyperlink in soup.find_all('a', href=True):
            
            href_value = hyperlink.get('href')

            """
            https://pymotw.com/2/urlparse/

            To simply strip the fragment identifier from a URL, as you might need to do to find a base page name from a URL, use urldefrag().

            from urlparse import urldefrag
            original = 'http://netloc/path;parameters?query=argument#fragment'
            print original
            url, fragment = urldefrag(original)
            print url
            print fragment
            The return value is a tuple containing the base URL and the fragment.

            $ python urlparse_urldefrag.py

            http://netloc/path;parameters?query=argument#fragment
            http://netloc/path;parameters?query=argument                    <-- NOTE: get this one??
            fragment
            """

            defragmented_url = urllib.parse.urldefrag(href)[0]

            """
            https://pymotw.com/2/urlparse/

            Joining

            In addition to parsing URLs, urlparse includes urljoin() for constructing absolute URLs from relative fragments.

            from urlparse import urljoin
            print urljoin('http://www.example.com/path/file.html', 'anotherfile.html')
            print urljoin('http://www.example.com/path/file.html', '../anotherfile.html')
            In the example, the relative portion of the path ("../") is taken into account when the second URL is computed.

            $ python urlparse_urljoin.py

            http://www.example.com/path/anotherfile.html
            http://www.example.com/anotherfile.html
            """

            url = urllib.parse.urljoin(resp.url, defragmented_url)  # construct absolute url (?)
            
            # NOTE: where to use resp.raw_response.url ??

            if is_valid(url):    # check if url is valid to crawl
                hyperlinks_list.append(url)

            elif resp.status in [301, 302]:
                # indicates that the resource has been moved to a different URL.
                redirect_url = resp.headers.get('Location')
                hyperlinks_list.append(redirect_url)

            elif resp.status in [403, 404] :
                # cannot find request or forbidden
                pass

            elif resp.status == 500:
                # internal server error, retry the url later ?  not sure on this one
                hyperlinks_list.append(resp.url)
    
        

    else:   # if resp.status is not 200
        print(f"Error: {resp.error}")


    return hyperlinks_list  # return list of valid links to crawl

    # ^^^^

    return list()

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        # check for calendar pattern in url
        calendar_pattern = (
        r"\b\d{4}/\d{1,2}/\d{1,2}\b"  # paths like /2024/04/18
        + r"|\b(year|month|day)=\d+\b"   # strings like ?year=2024&month=04&day=18
        )
        #return re.match()
        
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())
            """Extra file types to ignore
            r".*\.(css|js|bmp|gif|jpe?g|ico|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz"
            + r"|flv|3gp|ts|webm"
            + r"|aac|flac|m4a"
            + r"|svg|webp|heic"
            + r"|json|xml|odt|ods|odp"
            + r"|xz|gzip|war|apk"
            + r"|php|py|bat|sh"
            + r"|ttf|woff|woff2|icon)$", parsed.path.lower())
    """

    except TypeError:
        print ("TypeError for ", parsed)
        raise


"""


# this will check if the robots.txt file allows crawling for any user agent
def robots_check(url, user_agent = '*'):
    # get robots.txt url
    parsed_url = urllib.parse.urlparse(url)
    robots_txt_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"


    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(url)
    try:
        rp.read()
    except Exception as e:
        print('robots.txt not found')
        return False
    if rp.can_fetch(user_agent, url_to_check):
        return True
    else:
        return False

"""
