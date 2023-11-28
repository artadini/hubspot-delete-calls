import hubspot
from hubspot.crm.objects.calls import PublicObjectSearchRequest, ApiException, BatchInputSimplePublicObjectId
import time
from datetime import datetime

# filters added in a separate file
from filters import initial_filter,properties,look_for_new_zoom_calls,sorting,exlude_words,people_to_exlude

"""
Flow of this script.

1. Search HubSpot calls using the filters in filters.py.
2. Cycle through the IDs and delete those that matched the stated filters in the IF block and append the IDs which match the filters to the list.
3. Delete calls in the list.
4. Wait 1 minute to start the loop again.

"""

# HubSpot API key
HS_PRIVATE_KEY = ''

print(f"Starting HubSpot Calls Deletion Script at: {datetime.now()}")

# start of loop
while True:
    print('\n--- Starting Now ---\n')
    hs_key = HS_PRIVATE_KEY
    client = hubspot.Client.create(access_token=hs_key)

    hs_ids_to_remove = []
    last_zoom_call_created_at = []
    initial_filter = list(map(lambda x: x.lower(), set(initial_filter)))
    people_to_exlude = list(map(lambda x: x, set(people_to_exlude)))

    # 1. Search HubSpot calls using the filters.
    public_object_search_request = PublicObjectSearchRequest(filter_groups=look_for_new_zoom_calls,limit=100,sorts=sorting,properties=properties)
    try:
        new_zoom_calls = client.crm.objects.calls.search_api.do_search(public_object_search_request=public_object_search_request)
        new_zoom_calls = new_zoom_calls.to_dict()
    except ApiException as e:
        print("\nException when calling search_api->do_search: %s\n" % e)

    # 2. Cycle through the IDs and delete those that matched the IF statements.
    for i in new_zoom_calls['results']:

        title = i['properties']['hs_call_title'].lower()
        id = i['properties']['hs_object_id']
        call_duration = i['properties']['hs_call_duration']
        owner_id = i['properties']['hubspot_owner_id']

        # get ID based on a call duration less than 5 minutes
        if call_duration != None:
            duration = call_duration
            duration_int = int(duration)
            if duration_int < 300000:
                hs_ids_to_remove.append(id)
        
        # get ID based on a call duration which is empty
        if call_duration == None:
            hs_ids_to_remove.append(id)

        # get ID based on null in the call owner
        if owner_id == None:
            hs_ids_to_remove.append(id)
        
        # get ID based on the set filters
        if any(word in title for word in initial_filter) and not any(word in title for word in exlude_words):
            hs_ids_to_remove.append(id)

        # identify the owners that should be excluded
        if owner_id != None:
            if any(word in owner_id for word in people_to_exlude):
                hs_ids_to_remove.append(id)
        
        if owner_id == None:
            hs_ids_to_remove.append(id)

    # 3. Delete calls if the list is not null.
    dedup_calls_to_delete_response = list(set(hs_ids_to_remove))
    length_dedup_calls_to_delete_response = len(dedup_calls_to_delete_response)

    if length_dedup_calls_to_delete_response > 0:
        print('Following IDs found for deletion: %s'%(hs_ids_to_remove))
        if length_dedup_calls_to_delete_response > 1:
            batch_input_simple_public_object_id = BatchInputSimplePublicObjectId(inputs=dedup_calls_to_delete_response)
            try:
                delete_api_response = client.crm.objects.calls.batch_api.archive(batch_input_simple_public_object_id=batch_input_simple_public_object_id)
            except ApiException as e:
                print("\nException when calling batch_api->archive: %s\n" % e)
        else:
            print("\n1 call deleted. Now going to sleep until the next minute.\n")
            print("\nCall to be deleted:",dedup_calls_to_delete_response)
            try:
                delete_api_response = client.crm.objects.calls.basic_api.archive(call_id=dedup_calls_to_delete_response[0])
            except ApiException as e:
                print("\nException when calling basic_api->archive: %s\n" % e)
    else:
        print('No matching calls, loop finished.')
        pass

    # 4. wait 1 minute to start loop again
    print(f"Loop finished at: {datetime.now()}")
    time.sleep(60)
