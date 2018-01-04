# Etsy Listing Diff Tool
This is a simple tool to track changes in Etsy shop inventories.

The tool fetchs listings from the shops specified in a configuration file and 
outputting added and removed listings to the console. It also saves a copy
of the shops listings to a JSON file.

## Usage
**Note**: This assumes you have either
[Python 3.6](https://www.python.org/downloads/release/python-360/) or
[Docker](https://www.docker.com/) installed on your
machine.

The first thing you will need to do is obtain an API key from Etsy. 
The Etsy [API Docs](https://www.etsy.com/developers/documentation/getting_started/register)
outline this procedure.

Next, you will need to create a configuration file. This file
lets you specify which shops to monitor, and which API key to use. In order to 
create a configuration file, copy `config.ini.example` to `config.ini`, replacing
your API key and shop IDs into the appropriate fields.

Once you've created the configuration file, you can start tracking store changes.

### Python 3.6 Usage
If you happen to have Python 3.6 installed, you can simply run the diff runner.
`python diff_runner.py`

### Python 3.6 Usage
If you do not have Python 3.6 installed on your machine, but do have Docker
available, you can also run the diff tool very easily.

First, build the docker image. `docker-compose build diff`. This
builds a lightweight image with Python 3.6 installed and all files mapped to the
appropriate directories.

Then, run the container. `docker-compose run --rm diff`. This command invokes 
`python diff_runner.py` inside the container.

## Postmortem
See [POSTMORTEM.md](POSTMORTEM.md) for afterthoughts, challenges faced, and
perceived strenghts and weaknesses of this application.