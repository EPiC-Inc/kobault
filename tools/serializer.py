import csv

with open("pathfinder_spells.tsv", 'r') as spell_file:
    spell_csv = csv.DictReader(spell_file, delimiter='\t')

