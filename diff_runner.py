import configparser
from lib.etsy_diff import EtsyDiff


def get_api_key(config):
    """
    Get this user's API key from the .ini file. This function doesn't do much
    now, but provides a clean mechanism for any future validation/munging.

    :param config: ConfigParser object
    :returns: API key
    """
    return config['api']['key']


def get_shop_ids(config):
    """
    Get shop IDs from the config file. This helper function splits the comma
    separated shop ID string from the .ini file and strips leading and trailing
    whitespace as required. Ideally there won't be whitespace, but since the
    .ini is user generated, we can't guarantee anything.

    :param config: ConfigParser object
    :returns: list of shop IDs, trimmed of whitespace
    """
    shop_id_string = config['shops']['ids']
    shop_id_list = shop_id_string.split(',')
    return [shop_id.strip() for shop_id in shop_id_list]


def run():
    """
    Run the diff. First we read from the .ini file, then we instantiate EtsyDiff
    on each shop ID, generating the diff and saving updated listing JSON as
    required.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')

    api_key = get_api_key(config)
    shop_ids = get_shop_ids(config)

    # Right now, we simply iterate over the IDs, creating an EtsyDiff object for
    # each. If rate limits weren't an issue, we could parallelize this fairly
    # easily with concurrent.futures.
    for shop_id in shop_ids:
        diff = EtsyDiff(shop_id)
        diff.set_api_key(api_key)
        diff.run()

if __name__ == "__main__":
    run()
