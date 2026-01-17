"""
for m_select test_subdiff
"""

import gzip
import json
import glob
import re

table_list = []
for bmt_filepath in glob.glob('../../table/*.bmt'):
    with gzip.GzipFile(bmt_filepath) as f:
        d = json.load(f, strict=False)
        table_name = d['name']
        if  'おすすめ譜面表' in table_name or 'BMS Search' in table_name:
            continue
        table_list.append((bmt_filepath, d['tag']))
table_list.sort(key=lambda x: x[1])

subdiff_data = {}

for bmt_filepath, table_tag in table_list:
    with gzip.GzipFile(bmt_filepath) as f:
        d = json.load(f, strict=False)

        table_name = d['name']

        for d2 in d['folder']:
            subdiff_name = d2['name']

            if table_name == 'Satellite Recommend':
                subdiff_name += "*"
            elif table_name == 'Satellite (Voting)':
                subdiff_name += "?"
            elif table_name == 'Satellite (Rejected)':
                subdiff_name += "'"
            else:
                m = re.match(r'(?P<level>[EFHN]★\d+\.\d+)\.\.\.\d+\.\d+', subdiff_name)
                if m != None:
                    subdiff_name = m.group('level') + '…'

                m = re.match(r'(?P<short>[EFHN]★)\.\.\.(?P<level>\d+\.\d+)', subdiff_name)
                if m != None:
                    subdiff_name = m.group('short') + '…' + m.group('level')

                m = re.match(r'(?P<level>[EFHN]★\d+\.\d+)\.\.\.$', subdiff_name)
                if m != None:
                    subdiff_name = m.group('level') + '…'

            # print(subdiff_name)
            for d3 in d2['songs']:
                if 'md5' in d3:
                    key = ('md5', d3['md5'])
                elif 'sha256' in d3:
                    key = ('sha256', d3['sha256'])
                else:
                    print(subdiff_name, d3)
                    raise Exception

                if key not in subdiff_data:
                    subdiff_data[key] = []
                subdiff_data[key].append(subdiff_name)

# filter
p1 = r'^sU(?P<year>\d{4})/(?P<month>\d{2})$'
p2 = r'^sl\d+$'
p3 = r'^sl\d+\*$'
for key, value in subdiff_data.items():
    for i, subdiff_name in enumerate(value):
        m = re.match(p1, subdiff_name)
        if m != None:
            if len(value) > 1:
                value.pop(i)
                break
            else:
                value[i] = 'sU'
                break

    has_sl_rec = False
    for i, subdiff_name in enumerate(value):
        m = re.match(p3, subdiff_name)
        if m != None:
            has_sl_rec = True
            break
    if has_sl_rec:
        for i, subdiff_name in enumerate(value):
            m = re.match(p2, subdiff_name)
            if m != None:
                value.pop(i)
                break

md5_list = []
sha256_list = []

for key, value in subdiff_data.items():
    subdiff = '"' + ' / '.join(value) + '"'
    t = f'["{key[1]}"] = {subdiff},'
    if key[0] == 'md5':
        md5_list.append(t)
    elif key[0] == 'sha256':
        sha256_list.append(t)
    else:
        raise Exception

lua_list = []
lua_list.append('return {')
lua_list.append('  md5 = {')
lua_list += [ f'    {s}' for s in md5_list ]
lua_list.append('  },')
lua_list.append('  sha256 = {')
lua_list += [ f'    {s}' for s in sha256_list ]
lua_list.append('  },')
lua_list.append('}')

with open('subdiff.lua', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lua_list))

