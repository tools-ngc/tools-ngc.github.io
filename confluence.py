from atlassian import Confluence
import json
from json2html import *


confluence = Confluence(
    url='https://bigmac.northgrum.com/confluence/',
    username='M62890',
    password='Waterpolo3!',
    verify_ssl=False)

with open('DARPA.json') as json_file:
    data = json.load(json_file)
    #print(data['mto'])
    test = data['mto']
    for entries in test:
        print(entries['name'])
    pagecontent = json2html.convert(json = data['mto'])
    #print(pagecontent)

#pageid = (confluence.get_page_id("DARPA", "DARPAScraper Results"))
#pagecontent = '<table class="confluenceTable"><tbody><tr><th class="confluenceTh">test321</th><th class="confluenceTh"> </th></tr><tr ><td class="confluenceTd">h</td><td class="confluenceTd"> </td></tr><tr><td class="confluenceTd">k</td><td class="confluenceTd"> </td></tr></tbody></table>'

#update = confluence.update_page(pageid, 'DARPAScraper Results', pagecontent, parent_id=None, type='page', representation='storage', minor_edit=False)

#print(update)