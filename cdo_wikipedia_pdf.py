# uses https://gist.github.com/ztl8702/1c77d1f3c2cc6f73633efd1de390a496/raw/f61f2e57e2f3265008786661dfa20d8218450656/cdo_text.json
import requests
import json
data_url = 'https://gist.github.com/ztl8702/1c77d1f3c2cc6f73633efd1de390a496/raw/f61f2e57e2f3265008786661dfa20d8218450656/cdo_text.json'
raw = requests.get(data_url).text
data = json.loads(raw)
html = '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><style>.keep-together { page-break-inside: avoid; } .break-before { page-break-before: always; } .break-after { page-break-after: always; }</style><div class="break-after">__TABLE_OF_CONTENTS__</div>' # __TABLE_OF_CONTENTS__ is table of contents
newline = '\n' # newline literals can't be put in f-strings
toc = ''
curr_contents = []
def make_contents_list(contents):
    return '<br/>'.join([f'<a href="#{i}">{i}</a>' for i in contents])
for index, page in enumerate(data):
    section_class = 'break-before' if index != 0 else ''
    html += f'<div id="{page["title"]}" class="{section_class}"><h1>{page["title"]}</h1>{page["text"].replace(newline, "<br/>")}</div>\n'
    curr_contents.append(page['title'])
    if len(curr_contents) == 66:
        contents_class = 'break-before' if toc != '' else ''
        toc += f'<div class="{contents_class}">{make_contents_list(curr_contents)}</div>'
        curr_contents = []
#print(toc)
html = html.replace('__TABLE_OF_CONTENTS__', toc, 1)
print('done processing html, writing to file...')
with open('out.html', 'w+', encoding='utf-8') as f:
    f.write(html)
print('done writing, processing pdf...')
import pdfkit
pdfkit.from_file('out.html', 'out.pdf')
#print('done processing pdf, uploading file...')
#import os
#os.system('curl --upload-file out.pdf https://transfer.sh/out.pdf')
print('\ndone!')