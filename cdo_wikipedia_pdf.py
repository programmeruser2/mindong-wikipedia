# uses https://gist.github.com/ztl8702/1c77d1f3c2cc6f73633efd1de390a496/raw/f61f2e57e2f3265008786661dfa20d8218450656/cdo_text.json
import requests
import json
import argparse

parser = argparse.ArgumentParser(description='Generate a PDF and/or HTML file for the Min Dong Wikipedia')
parser.add_argument('--url', default='https://gist.github.com/ztl8702/1c77d1f3c2cc6f73633efd1de390a496/raw/f61f2e57e2f3265008786661dfa20d8218450656/cdo_text.json', help='Dump URL')
parser.add_argument('--pages', type=int, default=-1, help='Number of pages to process')
parser.add_argument('--formats', default='html,pdf', help='Output formats')
args = parser.parse_args()
print(type(args.pages))
print(f'url={args.url}\npages={args.pages}\nformats={args.formats}')

formats = args.formats.split(',')
data_url = args.url
raw = requests.get(data_url).text
data = json.loads(raw)
html = '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><style>.keep-together { page-break-inside: avoid; } .break-before { page-break-before: always; } .break-after { page-break-after: always; }</style><div class="break-after">__TABLE_OF_CONTENTS__</div>' # __TABLE_OF_CONTENTS__ is table of contents
newline = '\n' # newline literals can't be put in f-strings
toc = ''
curr_contents = []
processed_pages = 0
def make_contents_list(contents):
    return '<br/>'.join([f'<a href="#{i}">{i}</a>' for i in contents])
def add_toc_page():
    global toc, curr_contents
    contents_class = 'break-before' if toc != '' else ''
    toc += f'<div class="{contents_class}">{make_contents_list(curr_contents)}</div>'
    curr_contents = []
for index, page in enumerate(data):
    section_class = 'break-before' if index != 0 else ''
    html += f'<div id="{page["title"]}" class="{section_class}"><h1>{page["title"]}</h1>{page["text"].replace(newline, "<br/>")}</div>\n'
    curr_contents.append(page['title'])
    if len(curr_contents) == 66:
        add_toc_page()
    processed_pages += 1
    if processed_pages == args.pages:
        print('stopping at', processed_pages)
        if len(curr_contents) != 0:
            add_toc_page()
        break
    
#print(toc)
html = html.replace('__TABLE_OF_CONTENTS__', toc, 1)
print('done processing html, either writing to processing pdf...')
if 'html' in formats:
    with open('out.html', 'w+', encoding='utf-8') as f:
        f.write(html)
    print('done writing, processing pdf...')
if 'pdf' in formats:
    import pdfkit
    pdfkit.from_string(html, 'out.pdf')
#print('done processing pdf, uploading file...')
#import os
#os.system('curl --upload-file out.pdf https://transfer.sh/out.pdf')
print('\ndone!')