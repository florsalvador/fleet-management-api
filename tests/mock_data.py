"""Mock data"""

taxis_response = [
    {"id": 7249, "plate": "CNCJ-2997"},
    {"id": 10133, "plate": "PAOF-6727"},
    {"id": 2210, "plate": "FGMG-3071"},
    {"id": 1065, "plate": "GHDN-9291"},
    {"id": 7956, "plate": "CCKF-1601"},
]

locations_response = [
    {
        "date": "Sat, 02 Feb 2008 14:22:40 GMT",
        "id": 1,
        "latitude": 116.30508,
        "longitude": 39.96525,
        "taxi_id": 6418,
    },
    {
        "date": "Sat, 02 Feb 2008 14:25:54 GMT",
        "id": 2,
        "latitude": 116.3043,
        "longitude": 39.9622,
        "taxi_id": 6418,
    },
    {
        "date": "Sat, 02 Feb 2008 14:30:55 GMT",
        "id": 3,
        "latitude": 116.32259,
        "longitude": 39.96596,
        "taxi_id": 6418,
    },
]

last_location_response = [
    {
        "date": "Fri, 08 Feb 2008 16:07:16 GMT",
        "latitude": 116.11806,
        "longitude": 39.72814,
        "plate": "PAOF-6727",
        "taxi_id": 10133,
    },
    {
        "date": "Fri, 08 Feb 2008 17:37:43 GMT",
        "latitude": 116.32706,
        "longitude": 39.84801,
        "plate": "FHLB-7962",
        "taxi_id": 6598,
    }
]
