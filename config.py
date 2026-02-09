# Dubizzle Scraper Configuration

# API Constants
ALGOLIA_APP_ID = "WD0PTZ13ZS"
ALGOLIA_API_KEY = "cef139620248f1bc328a00fddc7107a6"
ALGOLIA_BASE_URL = f"https://{ALGOLIA_APP_ID}-dsn.algolia.net/1/indexes/*/queries"

# Search Indexes
PRIMARY_INDEX = "motors.com"
SORTBY_ADDED_DESC_INDEX = "by_added_desc_motors.com"

# Scraper Settings
DEFAULT_HITS_PER_PAGE = 25
DEFAULT_TIMEOUT = 30
MIN_DELAY = 1.0
MAX_DELAY = 3.0

# Paths
COOKIES_FILE = "cookies.json"
DEFAULT_OUTPUT_JSON = "results.json"
DEFAULT_OUTPUT_CSV = "results.csv"

# Browser Headers (to look real)
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://uae.dubizzle.com/",
    "Origin": "https://uae.dubizzle.com",
    "x-algolia-api-key": ALGOLIA_API_KEY,
    "x-algolia-application-id": ALGOLIA_APP_ID
}
