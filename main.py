import json, sys
from Lib import NCBIscraper

species = json.load(open("./Temp/jsonDatabase/database.json"))[0]
obj = NCBIscraper(species['Organism'], species['Accession'], species["Gene_Locus"], log=False, headless=True)
for responce in obj.run():
    sys.stdout.write("\r"+ f"{responce}")
    sys.stdout.flush()