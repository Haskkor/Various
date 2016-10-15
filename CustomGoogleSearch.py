import datetime as dt
import json, sys
from apiclient.discovery import build


if __name__ == '__main__':
    """
    Custom search from Google API
    """
    date = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    output_fname = 'result_' + date + '.json'
    search_term = "flight paris auckland"
    num_requests = 1
    search_engine_id = '000131698311187267455:pvrxzsjqn-c'
    api_key = 'AIzaSyBDi8VT0DWJOiK8b3ditTZUfzHF1_4MELY'
    # API name and version
    service = build('customsearch', 'v1', developerKey=api_key)
    # CustomSearch API returns the cse Resource
    collection = service.cse()
    output_f = open(output_fname, 'ab')
    for i in range(0, num_requests):
        start_val = 1 + (i * 10)
        # Make an HTTP request object
        request = collection.list(q=search_term, num=10, start=start_val,
                                  cx=search_engine_id)
        response = request.execute()
        output = json.dumps(response, sort_keys=True, indent=2)
        output_f.write(output)
    output_f.close()

# API : https://console.developers.google.com/apis/credentials?project=flightpricetracking-145507
# Create a project
# Enable the API
# Create a key
# CS : https://cse.google.com/cse/setup/basic?cx=000131698311187267455:pvrxzsjqn-c
# Create a custom search
