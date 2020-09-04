# VRT Events Subtitle Available

## Synopsis

This service listens to `openOtAvailableEvent` and `closedOtAvailableEvent` messages coming in on a Rabbit queue.
It will transform these in `makeSubtitleAvailableRequest` messages and publish them to a Rabbit exchange.

## Prerequisites

- Git
- Docker (optional)
- Python 3.6+
- Access to the [meemoo PyPi](http://do-prd-mvn-01.do.viaa.be:8081)

## Usage

1. Clone this repository with:

   `$ git clone https://github.com/viaacode/vrt-events-subtitle-available.git`

2. Change into the new directory.

3. Set the needed config:

    Included in this repository is a `config.yml` file detailing the required configuration.
    There is also an `.env.example` file containing all the needed env variables used in the `config.yml` file.
    All values in the config have to be set in order for the application to function correctly.
    You can use `!ENV ${EXAMPLE}` as a config value to make the application get the `EXAMPLE` environment variable.

### Running locally

**Note**: As per the aforementioned requirements, this is a Python3
application. Check your Python version with `python --version`. You may want to
substitute the `python` command below with `python3` if your default Python version
is < 3. In that case, you probably also want to use `pip3` command.

1. Start by creating a virtual environment:

    `$ python -m venv env`

2. Activate the virtual environment:

    `$ source env/bin/activate`

3. Install the external modules:

    ```
    $ pip install -r requirements.txt \
        --extra-index-url http://do-prd-mvn-01.do.viaa.be:8081/repository/pypi-all/simple \
        --trusted-host do-prd-mvn-01.do.viaa.be
    ```

4. Run the tests with:

    `$ pytest -v --cov=app`

5. Run the application:

    `$ python main.py`


### Running using Docker

1. Build the container:

   `$ docker build -t vrt-events-subtitle-available .`

2. Run the container (with specified `.env` file):

   `$ docker run --env-file .env --rm vrt-events-subtitle-available:latest`