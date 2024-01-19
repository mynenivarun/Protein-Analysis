import requests
import json
import csv

fl = 'pa.csv'

with open(fl, 'r') as csvfile: 
    csvreader = csv.reader(csvfile) 
      
    for row in csvreader:
        id = row[0]
        link = 'https://rest.uniprot.org/uniprotkb/search?query='+id

        values = []
        NA_id = []
        pid = ''
        sid = ''
        meth = ''
        res = ''


        r = requests.get(link)
        body = json.loads(r.text)

        if r.status_code == 200:
            pid = body['results'][0]['primaryAccession']
            print(f'Protien ID of {id} : {pid}')
            for entry in body['results'][0]['uniProtKBCrossReferences']:
                if entry['database'] == 'PDB':
                    sid = entry['id']

                for prop in entry['properties']:
                    if prop['key'] == 'Method':
                        meth = prop['value']
                    if prop['key'] == 'Resolution':
                        res = prop['value']
                    tup = [id,pid,sid,meth,res]
                    values.append(tup)
        else :
            print(f'ID Not Found : {id}')
            NA_id.append(id)

cs = ['ESM_ID','Protien_ID','PDB_ID','Method','Resolution']

fo = 'pa-out.csv'

myFile = open(fo, 'w')
writer = csv.writer(myFile)
writer.writerow(cs)
for list in values:
    writer.writerow(list)
myFile.close()