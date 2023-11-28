# Deletion of Zoom calls script for HubSpot

This script will delete incoming recorded Zoom calls in HubSpot which match a certain defined criteria.<br>
The code runs every minute of the day. <br>
See filters.py to see the filter criteria. To add more, just append to the end of the list the new word, the code will take care of the rest.<br>

* [Calls documentation](https://developers.hubspot.com/docs/api/crm/calls)
* [SEARCH request documentation](https://developers.hubspot.com/docs/api/crm/search)

## What it does

1. Search HubSpot calls using the filters.
2. Cycle through the IDs and delete those that matched the IF statements.
3. Delete calls if the list is not null and wait 1 minute to start loop again.

## How it runs
Right now it's deployed in the `kbs-data-cluster` and you can check the current logs in this [datadog page](https://app.datadoghq.eu/logs?query=service%3Ahubspot-tools%20env%3Aproduction%20&cols=host%2Cservice&index=%2A&messageDisplay=inline&stream_sort=desc&viz=stream&from_ts=1682431786552&to_ts=1682435386552&live=true).

## How to run it

Start the docker container and run it.<br>
The Docker container will include also a CRON job that will activate the script every min during work hours and during the week only.

## Starting the Docker container

Navigate with to the directory containing the `Dockerfile`.<br>
`docker build .`<br>
`docker run hs_zoom_calls`<br>
`docker logs -f hs_zoom_calls --since 60m`
