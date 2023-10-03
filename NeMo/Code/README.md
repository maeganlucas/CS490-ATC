# ASR WebApp
**This project is still very much a WIP, so take setup and install instructions with a grain of salt. I will do my best to keep them up to date as I add more dependencies and setup/running steps to the project.**

## Dependency Setup
First, clone the repository if you haven't already
```
git clone https://github.com/AVanDeBrook/asr-webapp.git
```
### JavaScript Dependencies
**The JavaScript-side dependencies are already set up** i.e. they are already linked in the HTML templates (`source/templates`) and/or downloaded (`source/static/vendor`).
The JavaScript side of the app uses the following libraries (these are all the most recent versions at the time of writing this):

* [Leaftlet v1.9.3](https://leafletjs.com/)
* [JQuery v3.7.0](https://jquery.com/)
* [Leaftlet Rotated Marker Plug-in v0.2.0](https://github.com/bbecquet/Leaflet.RotatedMarker)

### Python Dependencies
`Cython` needs to be installed and setup first
```
pip install -U Cython
```
then all other dependencies call be installed from the requirements file
```
pip install -r requirements/requirements.txt
```

Unfortunately, the OpenSky API is not available through PyPI and needs to be installed as an editable package. [Follow the instructions on their GitHub for Python installation](https://github.com/openskynetwork/opensky-api/blob/master/README.md#python-api).

## Project Setup

### API Secret Management
The project is configured to load secrets (i.e. API secret keys, username/password credentials, etc.) from a `secrets.py` file in the `source` folder. **The git repo is configured to ignore this file by default (see [`.gitignore`](./.gitignore#L5)).**

The secrets are organized as classes with attributes corresponding to the API secrets.

```python
# APIs that use or require username/password creds end with `Credentials`
class <PascalCaseAPIName>Credentials(object):
    USERNAME = "<username>"
    PASSWORD = "<password>"

# APIs that use or require an API key or secret end with `Secret`
class <PascalCaseAPIName>Secret(object):
    SECRET = "<api-secret>"
```

For example, the [OpenSky API](https://openskynetwork.github.io/opensky-api/) uses a username and password for access to certain endpoints in their REST API
```python
class OpenSkiCredentials(object):
    USERNAME = "<username>"
    PASSWORD = "<password>"
```
where `<username>` and `<password>` are the username and password, respectively for your OpenSky Network account (or the account you are using to access the API).

A note for the security conscious: this project does not store or log these credentials anywhere except the `secrets.py` file (read the code if you don't believe me).
If you're uncomfortable using your account to access these APIs then (1) create a dummy account for API access (2) change your password after use or (3) just don't store your secrets in `secrets.py` (everything should continue to work without them).

At the moment the project works both with and without the secrets being set up (using import guarding), but I would recommend setting them up anyway in case one or more of the APIs change from free use to registered user only.

## Running the Project
After the dependencies are installed and set up wherever necessary, the project can be run by the following:
```
flask --app source run
```
or in debug mode
```
flask --app source run --debug
```

Flask should print the IP address and port that it is running on to `stdout` (usually `localhost:5000`).
Copy and paste this into your browser and the index page should load, then you can browse and use the app as desired.

## Data Sources
[Modified] List of US Airports - https://data.humdata.org/dataset/ourairports-usa

Real-time Flight Data - https://opensky-network.org/

Icons - https://fontawesome.com/icons
