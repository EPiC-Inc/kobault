from urllib.request import urlopen

from bs4 import BeautifulSoup as Soup

#ANCHOR - set up URLs and parsers
URL = "https://www.aonprd.com/"

class_page = urlopen(f"{URL}Classes.aspx")
class_links = Soup(class_page, 'lxml')
classes = []

# race_page = urlopen(f"{URL}races")
# race_soup = Soup(race_page, 'html.parser')

#ANCHOR - start parsing
# Classes:
links = class_links.find(id="ctl00_MainContent_AllClassLabel")
links = links.find_all('a') # type: ignore
for link in links:
    link = link.get('href').replace(" ", "%20")
    print(f"{URL}{link}")
    current_link = urlopen(f"{URL}{link}")
    current_class = Soup(current_link, 'lxml')
    #NOTE - this gets the class features table (which should be the first table to pop up)
    print(current_class.find(class_="inner"))


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
