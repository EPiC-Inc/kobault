from json import dumps
from urllib.request import urlopen

from bs4 import BeautifulSoup as Soup
from lxml import etree
from lxml.html import fromstring

#ANCHOR - set up URLs and parsers
URL = "https://www.aonprd.com/"

with open('pathfinder_conditions.html', 'rb') as cond_file:
    conditions_page = cond_file.read().decode('utf-8')
cond_soup = Soup(conditions_page, 'lxml')

conditions = {}

dom = etree.HTML(str(cond_soup), parser=None)
found_conditions = dom.xpath("//a[contains(@name, 'TOC-')]")
for condition in found_conditions:
    condition_name = ''.join(condition.getparent().itertext()).strip()
    condition = condition.getparent().getparent()
    #''.join(condition.itertext())
    print(''.join(condition.itertext()))


#['__new__', '__repr__', '__iter__', '__bool__', '__len__', '__getitem__', '__setitem__', '__delitem__', '__contains__', '_init', '__deepcopy__', '__copy__', 'set', 'append', 'addnext', 'addprevious', 'extend', 'clear', 'insert', 'remove', 'replace', '__reversed__', 'index', 'get', 'keys', 'values', 'items', 'getchildren', 'getparent', 'getnext', 'getprevious', 'itersiblings', 'iterancestors', 'iterdescendants', 'iterchildren', 'getroottree', 'getiterator', 'iter', 'itertext', 'makeelement', 'find', 'findtext', 'findall', 'iterfind', 'xpath', 'cssselect', 'tag', 'attrib', 'text', 'tail', 'prefix', 'sourceline', 'nsmap', 'base', '__doc__', '__hash__', '__str__', '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__', '__init__', '__reduce_ex__', '__reduce__', '__getstate__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']








quit()
class_page = urlopen(f"{URL}Classes.aspx")
class_links = Soup(class_page, 'lxml')
classes = {}

# race_page = urlopen(f"{URL}races")
# race_soup = Soup(race_page, 'html.parser')

#ANCHOR - start parsing
# Classes:
links = class_links.find(id="ctl00_MainContent_AllClassLabel")
links = links.find_all('a') # type: ignore
for link in links:
    link = link.get('href').replace(" ", "%20")
    if link.endswith("Companion"):
        print("End of player classes")
        break
    print(f"{URL}{link}")
    current_link = urlopen(f"{URL}{link}")
    current_class = Soup(current_link, 'lxml')

    dom = etree.HTML(str(current_class), parser=None)
    class_name = dom.xpath('//*[@id="ctl00_MainContent_DataListTypes_ctl00_LabelName"]/h1/text()')[0].strip()
    print(class_name)

    class_table = dom.xpath('//*[@id="ctl00_MainContent_DataListTypes_ctl00_LabelName"]/table')
    class_table = class_table[0]

    #NOTE - the spells per day heading trips this up a lot since it's on a different row :[
    start = 0
    while ((class_table[start][0].text is None) or not (class_table[start][0].text.strip())):
        start += 1
    headers = class_table[start][0].text
    # print(start, headers)

    classes[class_name] = {}
    for level in range(start, len(class_table)):
        level_label = "you should not be able to see this - let Emmett know if you do"
        for i, column in enumerate(range(0, len(class_table[start]))):
            current_feature = class_table[level][column].text
            #print(current_feature, end=' | ')
            match i:
                case 0:
                    level_label = current_feature
                    classes[class_name][level_label] = {}
                case 1:
                    classes[class_name][level_label]["base_attack_bonus"] = current_feature
                case 2:
                    classes[class_name][level_label]["save_fortitude"] = current_feature
                case 3:
                    classes[class_name][level_label]["save_reflex"] = current_feature
                case 4:
                    classes[class_name][level_label]["save_will"] = current_feature
                case 5:
                    classes[class_name][level_label]["new_features"] = current_feature
                case _:
                    #TODO - spell slots
                    pass
        #print()
# Oh that's a lot of stuff
with open('classes.json', 'w') as class_file:
    class_file.write(dumps(classes))
    

# all_spells_page = urlopen(f"{URL}/spells")
# soup = Soup(all_spells_page, 'html.parser')

# spells_to_parse = []

# tables = soup.find_all(class_="wiki-content-table")
# for level_table in tables:
#     for spell in level_table.findAll('tr')[1:]:
#         spell = spell.td.a.get('href')
#         spells_to_parse.append(spell)

# #spells_to_parse = spells_to_parse[:300:60] #TEMP
# #spells_to_parse.append('/spell:summon-draconic-spirit')
# print(len(spells_to_parse))
# for spell in spells_to_parse:
#     print(f"scraping spell {URL}{spell}")
#     spell_page = urlopen(f"{URL}{spell}")
#     soup = Soup(spell_page, 'html.parser')

#     # Get the spell's name
#     spell_name = soup.find(class_="page-title").span.contents[0]
#     #print(spell_name)

#     # Extract the body of spell information
#     soup = soup.find(id="page-content")
#     spell = soup.find_all(['p', 'ul', 'table'])

#     # Get the sourcebook
#     spell_source = spell[0].contents[0]
#     #print(spell_source)
#     spell = spell[1:] # Cut off the top of the spell data, we already used it

#     spell_level = spell[0].em.contents[0]
#     spell_level = spell_level.casefold().split()
#     # Separate and parse the spell level and magic school
#     if spell_level[1] == 'cantrip':
#         spell_type = spell_level[0]
#         spell_level = '0'
#     else:
#         spell_type = spell_level[1]
#         spell_level = spell_level[0][:spell_level[0].index('-')-2]
#     #print(spell_level, spell_type)
#     spell = spell[1:] # Cut off the top of the spell data, we already used it

#     # Get the details of the spell (casting time, range, components, duration)
#     spell_details = str(spell[0])
#     spell = spell[1:] # Cut off the top of the spell data, we already used it
#     spell_details = spell_details.replace('<br/>\n<strong>', '\n')
#     spell_details = spell_details.replace('<br/>\n', '<br/>')
#     spell_details = spell_details.replace('<br/>', '')
#     spell_details = spell_details.replace('<strong>', '')
#     spell_details = spell_details.replace('</strong>', '')
#     spell_details = spell_details[3:-4] # Get rid of the single <p></p> around it
#     spell_details = spell_details.split('\n')
#     spell_casting_time, spell_range, spell_components, spell_duration = spell_details
#     # Chop off the left side of all the details
#     # There has GOT to be an easier way to do this
#     spell_casting_time = spell_casting_time[spell_casting_time.index(":")+2:]
#     spell_range = spell_range[spell_range.index(":")+2:]
#     spell_components = spell_components[spell_components.index(":")+2:]
#     spell_duration = spell_duration[spell_duration.index(":")+2:]
#     #print(spell_casting_time, spell_range, spell_components, spell_duration)

#     # Get the class lists the spell is on
#     spell_lists = spell[-1].contents[::2]
#     spell_lists = spell_lists[1:] # Get rid of the "Spell Lists" thing. We already know what these are.
#     #print(spell_lists)
#     spell = spell[:-1]

#     # The rest should be the description
#     spell_description = spell
#     spell_description = ''.join(map(lambda s: markdownify(str(s)), spell_description))
#     spell_description = spell_description.strip()
#     spell_description = spell_description.replace("’", "\'")
#     #spell_description = spell_description.replace("’", "\'")
#     spell_description = spell_description.replace("“", "\"")
#     spell_description = spell_description.replace("”", "\"")
#     spell_description = spell_description.replace("—", "-")
#     #print(spell_description)

#     try:
#         spell_tags = "\n".join(["- "+l.contents[0].casefold() for l in spell_lists])
#     except:
#         spell_tags = '- no_spell_lists'

#     try:
#         spell_links = ', '.join([markdownify(str(l)) for l in spell_lists])
#     except:
#         spell_links = "None"
#     final = f'''---
# Level: {spell_level}
# tags:
# - spell/{spell_type}
# {spell_tags}
# ---

# <font size=\"7\">{spell_name}</font>
# [Level:: {spell_level}]

# **Casting Time:** {spell_casting_time}
# **Range:** {spell_range}
# **Components:** {spell_components}
# **Duration:** {spell_duration}

# {spell_description}

# **_Spell Lists._** {spell_links}'''

#     #print(final)
#     spell_name = spell_name.replace('/', '_')
#     with open(f"{spell_name}.md",'wb') as outfile:
#         outfile.write(final.encode('utf-8', errors='replace'))
