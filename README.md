# HubSpot Tool: Filter and Delete Calls

In the heart of a high-paced sales environment, volumes of calls are made daily.
Within this multitude, a challenge arises - discerning calls that need to be removed or outright deleted.
To address this, a technical solution was conceived: a granular filter designed for precision. This tool serves to systematically sift through the calls, eliminating unnecessary noise and optimising the system. It stands ready to enhance your sales process efficiency.

## What it does
This script will delete incoming recorded from the default souce: Zoom.<br>
The code runs by default every 15 minutes, please amend this in main.py.<br>
See filters.py to change the filter criteria.<br>
<br><br>

## How it runs
1. Search HubSpot calls using the filters in filters.py.
2. Cycle through the IDs and delete those that matched the stated filters in the IF block and append the IDs which match the filters to the list.
3. Delete calls in the list.
4. Wait 1 minute to start the loop again.

### Deployment suggestions
You can deploye this using [GitHub actions](https://github.com/features/actions) or e.g. run it in your Kubernetes cluser if you need a higher runtime frequency.

## How to run it

Start the docker container and run it.<br>
The Docker container will include also a CRON job that will activate the script every min during work hours and during the week only.

### Starting the Docker container

Navigate with to the directory containing the `Dockerfile`.<br>
`docker build .`<br>
`docker run hs_zoom_calls`<br>
`docker logs -f hs_zoom_calls --since 60m`

## Additional documentation
* [Calls API documentation](https://developers.hubspot.com/docs/api/crm/calls)
* [Search API documentation](https://developers.hubspot.com/docs/api/crm/search)
* [HubSpot Owner ID](https://legacydocs.hubspot.com/docs/methods/owners/get_owners)
