#get cat names names from tags
def get_cats(tags):
    supercats = []
    cats = []
    for t in tags:
        a, b, c = t.partition('::')
        supercats.append(a)
        cats.append(c)
    return (supercats, cats)

#pack data for conversion into dataframe
def pack(l, sig):
    vals = []
    for x in l:
        vals.append(x[sig])
    return vals
	
def data_pack(response):
	data = {}
	for key in response[0].keys():
		if key != 'default' and key != 'raw_name':
			data[key] = pack(response, key)
	return data

	
def data_assemble(response, file_name = 'out.xlsx'):
	data = data_pack(response.json()['ticket_field']['custom_field_options'])
	data['supercat'], data['cat'] = get_cats(data['name'])
	return data
	
def get_dict():
	import os, json, requests
	api_token = '...............'
	email = '...............'
	user = email + '/token'
	creds = (user, api_token)
	url = 'https://oneacrefund-rw.zendesk.com/api/v2/'
	url_ext = 'ticket_fields/114101151413.json'
	return data_assemble(requests.get(url + url_ext, auth = creds))

def write_file():
    fl=get_dict()

    with open('new test1.oaf', 'wb') as f:
    pk.dump(al, f)

    del al
    del f

with open('new test1.oaf', 'rb') as f:
    a=pk.load(f)

    


