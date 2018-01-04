import requests
import os
import json

DATA_DIR = 'data'


class EtsyException(Exception):
    pass


class EtsyDiff():
    def __init__(self, shop_id):
        """
        Constuct the EtsyDiff object.

        :param shop_id: Unique ID of a particular shop
        """
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        self.shop_id = shop_id
        self.datafile = os.path.join(DATA_DIR, f'{self.shop_id}.json')
        self.listings = {}
        self.old_listings = {}

    def diff_listings(self):
        """
        Compare listing IDs from the API response to those saved in the file.

        :param listing_ids: Incoming listing IDs
        :returns: tuple of lists in the shape of (added IDs, removed IDs)
        """
        # Cast both the incoming and existng listing ID lists to Set
        new_set = set(self.listings.keys())
        old_set = set(self.old_listings.keys())

        # Diff new vs old and old vs new.
        # New vs old gives us added listings.
        # Old vs new gives removed listings.
        added = list(new_set.difference(old_set))
        removed = list(old_set.difference(new_set))

        return (added, removed)

    def fetch_listings(self):
        """
        Fetch listings for a given shop.

        :returns: JSON decoding of requests.Response object.
        """
        url = f'https://openapi.etsy.com/v2/shops/{self.shop_id}/listings/active'
        payload = {'api_key': self.api_key}

        try:
            # Perform a GET request
            response = requests.get(url, params=payload)

            # Raise HTTPError for non-ok (4xx or 5xx) response codes
            response.raise_for_status()

            # Convert the Response object to JSON
            parsed_response = response.json()
        except requests.exceptions.HTTPError as http_exception:
            # If we threw HTTPError, convert to EtsyException and raise.
            raise EtsyException(http_exception)
        except ValueError as json_exception:
            # ValueError is thrown if res.json() fails. In that case. raise
            # our EtsyException.
            raise EtsyException(json_exception)
        else:
            # If we've made it this far, we return the JSON decoded listings
            return parsed_response

    def generate_output(self, added, removed):
        """
        Print a diff to standard out.

        :param added: list of added item IDs
        :param removed: list of removed item IDs
        """
        print(f'Shop ID {self.shop_id}')

        hasChanges = False
        for listing in added:
            hasChanges = True

            title = self.listings[listing]['title']
            print(f'+ added listing {listing} "{title}"')

        for listing in removed:
            hasChanges = True

            title = self.old_listings[listing]['title']
            print(f'- removed listing {listing} "{title}"')

        if not hasChanges:
            print("No Changes since last sync")

        print()

    def process_listings(self, response):
        """
        Process Listings. This is the heart of operations.

        :param response: JSON decoded request.Response object
        """
        self.listings = self.unfurl_listing(response['results'])
        self.write_listings()

        added_ids, removed_ids = self.diff_listings()

        self.generate_output(added_ids, removed_ids)

    def read_listings(self):
        """
        Read listing IDs from this shop's flat file

        :returns: list of listing IDs
        """
        try:
            with open(self.datafile, 'r') as f:
                return json.load(f)
        except FileNotFoundError as file_exception:
            return {}

    def run(self):
        try:
            self.old_listings = self.read_listings()

            # Fetch the listings
            response = self.fetch_listings()

            if response['count'] == 0:
                # If there are no listings, raise EtsyException
                raise EtsyException(f'No Listings: {str(self.shop_id)} has not listings')

            self.process_listings(response)
        except EtsyException as ex:
            print(ex)

    def set_api_key(self, api_key):
        self.api_key = api_key

    def unfurl_listing(self, results):
        """
        Unfurl listings. That is, convert the list of listings to a dictionary,
        using listing ids as keys. This lets us do a O(1) lookup on the keys
        when outputting the diff.

        :param results: list of listings from the GET request
        :returns: dict of listings
        """
        return {str(listing['listing_id']): listing for listing in results}

    def write_listings(self):
        """
        Write listing IDs from this shop's flat file

        :param keys: list of new listing IDs
        """
        try:
            with open(self.datafile, 'w') as f:
                json.dump(self.listings, f)
        except (TypeError, FileNotFoundError) as write_exception:
            # If for some reason we can't serialize the list of IDs or open the
            # shop's flat file, raise EtsyException
            raise EtsyException(type_exception)
