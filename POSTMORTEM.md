# Etsy Listing Diff Tool - Postmortem
This serves as a follow-up to the Etsy diff tool project, recapping challenges
faced, perceived strengths and weaknesses, tradeoffs made, miscellaneous notes.

### Challenges Faced
The first challenge of note was navigating Etsy's API documentation. The API 
documentation grouping endpoints into broad categories. For instance, `/shops`
and `/shops/:shopid` fall under **Shops**, while `/listings` and
`/listings/:listingid` appear under **Listings**. On the otherhand,
`/shops/:shopid/listings/active` falls under the **Listings**
category. If we followed the previous heuristic, it seems like this endpoint
should appear under **Shops**. In reality, the categories represent the data being
returned. In taht case, `/shops/:shopid/listings/active` makes total sense under
**Listings**.

### Perceived Strengths
`EtsyDiff` is an atomic object, allowing for easy parallelization, should we ever
need to scale our diffing. Using a library like `concurrent.futures` makes this
very simple. The current code would likely need some added exception handling, as
a parallelized approach would more than likely hit rate limits.

The pattern used to catch a variety of exceptions and reraise them as
`EtsyException` allows us to control flow from a single pipeline, as opposed to 
repeatedly handling throughout. Right now, I just swallow exceptions, but in the
future, logging or messaging mechanisms could be implemented.

### Perceived Weaknesses
Formatting of output in `EtsyDiff.generate_output()` isn't great. There has to be
a better way to format that output instead of multiple print statements or a 
multi-line string, but I can't think of one right now.

The overall structure of the application leaves a bit to be desired too. `lib` is
a bit sparse, while the project's root directory has a lot of content. I ultimately
decided to draw a line, with `lib` containing the classes, and root maintaining
the supporting functions used to instantiate those classes.

### Tradeoffs
This platform was written in Python 3.6, using PEP498 string literals (f strings)
for some of the outputs. Because 3.6 is failry new, and I can't guarantee all
users will have it available, I included a Docker image. Using an image allows me
to manage dependencies and file structures very easily. The disadvantage here is,
users are required to have Docker on their machines. I could have taken a virtual
environment approach, but then I would lose out control over the filesystem.

Another tradeoff is persisting full JSON responses in flat files. I had initially
hoped to save just listing IDs, but quickly realized this approach wouldn't work
when trying to output titles of removed items. Since these items were removed, I
wouldn't be able to reconcile the titles from list of fetched listings. It was
then that I decided to stash the entire response. The responses aren't huge, disc
space is cheap, and we can always remove files in the future. On the otherhand,
storing a subset of data would limit our ability to further analyze these files
in the future if we so decide.

### Misc Note
It is worth noting that such an application does violate Etsy API 
[Terms of Use](https://www.etsy.com/developers/terms-of-use#uses).

> Use automated systems designed to access, analyze, or scrape our website, including our API, unless expressly authorized by us.

Since this is a practical exercise that is very limited in scope, and isn't
_really_ automated, I opted to proceed anyway.

I omitted my `config.ini` since it does list my API key.

I used the following shop IDs for testing:
`7456355,8952192,6566866,9255258,11840579,9439471,13006140,16335993,7185240,11179509`

These IDs were taking from [Etsy's Top Selling Shops](https://www.etsy.com/market/top_selling_shops)