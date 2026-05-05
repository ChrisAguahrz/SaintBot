import os
family = 'wikipedia'
mylang = 'sw'
usernames = {}
usernames['wikipedia'] = {}
usernames['wikipedia']['sw'] = os.getenv('WIKI_USERNAME', 'Gayle-Bot')
authenticate = {}
authenticate['wikipedia'] = {}
authenticate['wikipedia']['sw'] = (os.getenv('WIKI_USERNAME', 'Gayle-Bot'), os.getenv('WIKI_PASSWORD', 'CountryBot@it3ipj55bu65vg6vjq57i8dq4olhsrp2'))
