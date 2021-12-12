from urllib.parse import urlparse, parse_qs, urlencode

link = ''

parsed = urlparse(link)

query_dict = parse_qs(parsed.query)

# print(query_dict)

for key in list(query_dict): # creates a shallow copy of the items of the dictionary
    if 'utm_' in key:
        del query_dict[key]

# print(query_dict)

print(urlencode(query_dict, doseq=True))

new_url = parsed._replace(query=urlencode(query_dict, doseq=True))

print(new_url.geturl())