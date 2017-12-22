import re
from datetime import timedelta
import requests
import requests_cache


expiry = timedelta(hours=999999999)
requests_cache.install_cache(expire_after=expiry)


def get_html(url, cache=True):
    """Gets the HTML of a webpage, decoded as UTF-8 and handles any HTTP errors"""
    if cache:
        try:
            # GET the webpage
            request = requests.get(url)
            html = request.content.decode('utf-8')

            # HLTV has a custom error page for HTTP errors
            if len(re.findall('error-desc', html)) > 0 or len(re.findall('error-500', html)) > 0:
                return None

        # Handle any other errors
        except:
            print(f"URL error for {url}")
            #tabulate('errors', [[url, 'Unknown']], False)
            return None
        return html
    else:
        with requests_cache.disabled():
            try:
                # GET the webpage
                request = requests.get(url)
                html = request.content.decode('utf-8')

                # HLTV has a custom error page for HTTP errors
                if len(re.findall('error-desc', html)) > 0 or len(re.findall('error-500', html)) > 0:
                    return None

            # Handle any other errors
            except:
                print(f"URL error for {url}")
                #tabulate('errors', [[url, 'Unknown']], False)
                return None
        return html