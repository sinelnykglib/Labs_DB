from pymongo import MongoClient
import csv
from bson.son import SON
import chardet
from flask import render_template


client = MongoClient('mongodb://mongodb:27017/', unicode_decode_error_handler='ignore')
# client = MongoClient('mongodb://localhost:27017/', unicode_decode_error_handler='ignore')
database = client['ZNOdata']
collection = database['znodata']

def DB_mong(filename, year):
    print(f"Writing data from {filename} to MongoDB")
    with open(filename, 'rb') as rawdata:
        result = chardet.detect(rawdata.read(10000))
    enc = result.get('encoding')
    i = 0
    with open(filename, 'r', encoding=enc) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        fieldnames = [key.lower() for key in reader.fieldnames]
        reader.fieldnames = fieldnames
        for row in reader:
            try:
                if i > 4000: break
                i += 1
                outid = row['outid']
                row['_id'] = outid
                row['year'] = year
                row = {key: value.replace(',', '.') if isinstance(value, str) else value for key, value in
                        row.items()}
                collection.insert_one(row)
            except Exception as e:
                print(e)

        print("MongoDB - finished!")
        print(f'Count: {collection.count_documents({})}')

def getAvgSub(subject,examyear,region_name):
    rg = {'subject':subject,'year':examyear}
    if region_name != 'Усі регіони':
        rg['regname'] = region_name
    creatine = [
        {
            '$match': rg
        },
        {"$group": {
            "_id": {
                "year": "$year",
                "regname": "$regname"
            },
            'averagebal': {'$avg': {'$toDouble': f'${subject}ball100'}}
        }},
        {"$sort": SON([("_id.regname", 1), ("_id.year", 1)])}
    ]

    protein = collection.aggregate(creatine)
    protein = []
    for doc in protein:
        o_3 = []
        o_3.append(doc["_id"]["regname"])
        o_3.append(doc["_id"]["year"])
        o_3.append(doc["averagebal"])
        if protein[2] is None: continue
        protein.append(o_3)
    return protein

def addNewStudent(outid, birth, year, sextypename, classprofilename, classlangname, regtypename,
                  regname, areaname, tername, eoname=None, eotypename=None, eoparent=None, eoregname=None, eoareaname=None, eotername=None):
    shkila = {
        '_id': outid,
        'outid': outid,
        'birth': birth,
        'year': year,
        'sextypename': sextypename,
        'classprofilename': classprofilename,
        'classlangname': classlangname,
        'regtypename': regtypename,
        'eoname': eoname,
        'eotypename': eotypename,
        'eoparent': eoparent,
        'eoregname': eoregname,
        'eoareaname': eoareaname,
        'eotername': eotername,
        'regname': regname,
        'areaname': areaname,
        'tername': tername,
    }

    for key, value in shkila.items():
        if value == '':
            shkila[key] = None

    try:
        collection.insert_one(shkila)
    except Exception as e:
        print(e)
        raise e

def deleteStudent(outid):
    collection.delete_one({"outid": outid})

def updateStudent(outid, birth, year, sextypename, classprofilename, classlangname, regtypename,
                  eoname=None, eotypename=None, eoparent=None, eoregname=None, eoareaname=None, eotername=None):
    lsd = {}
    tmp = ['birth','year','sextypename','classprofilename','classlangname','regtypename','eoname',
           'eotypename','eoparent','eoareaname','eoregname','eotername']
    gpd = [birth, year, sextypename, classprofilename, classlangname, regtypename,
            eoname, eotypename, eoparent, eoareaname, eoregname, eotername]

    for i in range (len(tmp)):
        if gpd[i] is not None and gpd[i] != '':
            lsd[tmp[i]] = gpd[i]
    if lsd:
        collection.update_one(
            {"outid": outid},
            {"$set": lsd}
        )

def addTest(student_id, teststatus, ball100, ball12, ball, adaptscale, ptname, subject_name, saab):
    L_t = {}
    
    taurine = ['teststatus','ball100','ball12','ball','adaptscale','ptname']

    for _ in range(len(taurine)):
        taurine[_] = saab+taurine[_]

    caffeine = [teststatus, ball100, ball12, ball, adaptscale, ptname]

    for _ in range(len(taurine)):
        if caffeine[_] != '':
            L_t[taurine[_]] = caffeine[_]
        else:
            L_t[taurine[_]] = None

    L_t[saab] = subject_name

    if L_t:
        collection.update_one(
            {"outid": student_id},
            {"$set": L_t}
        )
    #print(f'addTest query: {L_t}')
    return render_template('formtests_1.html', tests=L_t)


def updateTest(student_id, teststatus, ball100, ball12, ball, adaptscale, ptname, saab):
    lsd = {}

    bcaa = ['teststatus', 'ball100', 'ball12', 'ball', 'adaptscale', 'ptname']
    
    for _ in range(len(bcaa)):
        bcaa[_] = saab+bcaa[_]

    cla = [teststatus, ball100, ball12, ball, adaptscale, ptname]

    for _ in range(len(cla)):
        if cla[_] is not None and cla[_] !='':
            lsd[bcaa[_]] = cla[_]
    if lsd:
        collection.update_one(
            {"outid": student_id},
            {"$set": lsd}
        )
    print(f'updateTest query: {lsd}')

def deleteTest(outid, sub):
    query = {'outid': outid}
    update = {'$unset':
                {sub+'test': "null",
                sub+'teststatus': "null",
                sub+'ball100': "null",
                sub+'ball12': "null",
                sub+'ball': "null",
                sub+'adaptscale': "null",
                sub+'ptname': "null",
                sub+"ptregname": "null",
                sub+"ptareaname": "null",
                sub+"pttername": "null",
                 sub+'lang': "null",
                 sub+'dpalevel': "null",
                 sub+"subtest": "null"
    }
              }
    collection.update_one(query, update)
