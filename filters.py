"""
    This file contains the filters to be used in the HubSpot API calls.
    The only type of association that can be used for this call is the association to Contacts.

    initial_filter = filters to be used in the first call to the API. Words in search cannot include whitespaces.
    exlude_words = words to be excluded from the search. Words in search cannot include whitespaces.
    people_to_exlude = list of HubSpot owner IDs to be excluded from the search. Google for "how to find HubSpot owner ID".
    properties = list of properties to be displayed in the output. You need to name the properties exactly as they are in HubSpot otherwhise they won't be in the output.
    look_for_new_zoom_calls = filter to look exactly for new zoom calls. If you want to look for calls from other sources, you can remove / change this filter.
    sorting = sorting to be used in the API call. This is used to get the last call. If you want to get the first call, you can remove / change this filter but the code won't work anymore.
"""

initial_filter = ['example1','example2']

exlude_words = ['your_company_name']

people_to_exlude = ['9348743']

properties =   [
            # These properties are required, you can add more if you want
            "hs_call_duration",
            "hs_call_title",
            "hubspot_owner_id",
            "hs_object_id",

            # These properties are optional, you can remove them if you want
            'hs_call_from_number',
            'hs_call_recording_url',
            'hs_call_status',
            'hs_lastmodifieddate',
            'hs_timestamp'
        ]

# filter to look exactly for new zoom calls
look_for_new_zoom_calls = [
    {
        "filters": [
            {
                "propertyName": "hs_call_source",
                "operator": "EQ",
                "value": "ZOOM"
            }
        ]
    }
]

# always get the last call
sorting = [
    {
        "propertyName": "hs_createdate",
        "direction": "DESCENDING"
    }
]