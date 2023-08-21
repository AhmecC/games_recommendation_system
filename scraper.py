import requests
API_KEY = ''
BASE_URL = 'https://store.steampowered.com'


### -- Use sampled app_id's to obtain developer/publisher information -- ###
def get_requests(app_id):
    app_id = str(app_id)
    url = f"{BASE_URL}/api/appdetails?appids={app_id}"
    response = requests.get(url)
    
    data = response.json()
    if data != None:  
        A = data[app_id]['data']['developers'][0] if 'developers' in data.get(app_id, {}).get('data', {}) else None
        B = data[app_id]['data']['publishers'][0] if 'publishers' in data.get(app_id, {}).get('data', {}) else None
        return [app_id, A, B]
    else:
        return [app_id, None]  


### -- Due to steamAPI limits can only do around 200 requests every 5 minutes, this ensures i can obtain as much information as possible efficiently -- ###
chunk_size = 190
divided_lists = [df['app_id'][i:i+chunk_size].to_list() for i in range(0, len(df), chunk_size)]
files = []
for item in divided_lists:
    for x in item:
        files.append(get_requests(x))
        print('\n\n\n List Completed\n\n\n')
        time.sleep(240)
files_df = pd.DataFrame(files, columns=['app_id', 'Developer', 'Publisher']).set_index('app_id') # Merge with original df








### -- Run a second time aiming to get other missing information too -- ###
def get_requests2(app_id):
    app_id = str(app_id)
    url = f"{BASE_URL}/api/appdetails?appids={app_id}"
    response = requests.get(url)
  
    data = response.json()
    if data != None:  
        A = data[app_id]['data']['developers'][0] if 'developers' in data.get(app_id, {}).get('data', {}) else None
        B = data[app_id]['data']['publishers'][0] if 'publishers' in data.get(app_id, {}).get('data', {}) else None
        C = data[app_id]['data']['short_description'] if 'short_description' in data.get(app_id, {}).get('data', {}) else None
        tags = []
        if 'categories' in data.get(app_id, {}).get('data', {}):
            for i in data[app_id]['data']['categories']:
                tags.append(i['description'])
        if 'genres' in data.get(app_id, {}).get('data', {}):
            for i in data[app_id]['data']['genres']:
                tags.append(i['description'])
        return [app_id, A, B, C, tags]
    else:
        return [app_id, None]  
