import json, csv, os, numpy, zipfile, shutil
from Lib import codon

def convartURL(baseurl = "", key= ""):
    return(f"{baseurl}/?term={key.replace(' ', '+').replace('/', '%2F')}")

def backDoorUrl(ncbiuid, choice = 'FASTA Nucleotide'):
    choices = {"FASTA Nucleotide":"fasta_cds_na", "FASTA Protein":"fasta_cds_aa"}
    return(
            f"https://ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report={choices[choice]}&id={ncbiuid}&conwithfeat=on&hide-sequence=on&hide-cdd=on&ncbi_phid=null"
        )

def csvtojson(file):
    species = {"Organism" : "","Gene_Locus" : [], "Accession" :""}
    for row in csv.reader(open(file)):
        if row[-1] is not species["Organism"] : species["Organism"] = row[-1]
        species["Gene_Locus"].append(row[1])
    Accession = json.load(open("./Accession.json"))
    species["Accession"] = Accession[species["Organism"]]
    return(species)

def dumpSequence(Sequence):
    Sequence = Sequence.replace(" ", "")
    chunks, chunk_size = len(Sequence), 60
    dum = "\n".join([ Sequence[i:i+chunk_size] for i in range(0, chunks, chunk_size) ])
    return(f"{dum}\n\n")

def dumpFile(fileName, context, mode="a+"):
    with open(f'{fileName}.txt', mode) as file:file.write(context)

def dumpLine(line):
    temp = line.replace("\n","").replace(" ","").replace("*****"," ").split("\t")
    del(temp[-1])
    return(temp)

def jsontocsv(csvFilename="./jsonoutput.csv", jsondata=None, jsonfilename="", mode="w"):
    if jsondata == None and jsonfilename == "":
        return(print("please provide the json data"))
    elif jsonfilename != "":
        jsondata = json.load(open(jsonfilename))
    with open(csvFilename, mode, newline='') as csvFile:
        csv_writer = csv.writer(csvFile)
        count = 0
        for data in jsondata:
            if mode != "a+" and count == 0:
                header = data.keys()
                csv_writer.writerow(header)
                count += 1
            csv_writer.writerow(data.values())
    return(True)

def csvtojson(filename = ""):
    if filename == "":return(print("please provide the csv data"))
    with open(filename, mode ='r')as file:
        csvFile = list(csv.reader(file))
        jsondata = []
        for lines in csvFile[1:]:
            temp = {}
            for title, element in zip(csvFile[0], lines):
                temp[title] = element
            jsondata.append(temp)
        return(jsondata)

def csvtoarray(filename = "", seperateTarget=True):
    if filename == "":return(print("please provide the csv data"))
    with open(filename, "r") as file:
        csvFile = list(csv.reader(file))
        dataSet = []
        target = []
        targetIndex = -1
        if seperateTarget: 
            try:targetIndex = csvFile[0].index("target" or "Target" or "TARGET")
            except:return(print("No key named 'target' found"))
            for lines in csvFile[1:]:
                target.append(0 if lines[-1] != "EG" else 1)
        for lines in csvFile[1:]:
            dataSet.append([round(float(i), 4) if i != " " else 0 for i in lines[1:targetIndex]+lines[targetIndex+1:]])
        
        if seperateTarget:return(numpy.array(dataSet), numpy.array(target))
        else:return(numpy.array(dataSet))

def csvAppend(filename = "", data={}):
    try:oldData = csvtojson(filename)
    except:oldData = []
    oldData.append(data)
    jsontocsv(filename, oldData)

def choiceKey(strain, choice):
    choices = ["complete genome", "complete sequence", "chromosome"]
    if choice == "complete genome":
        return(f"{strain} complete genome")
    elif choice == "complete sequence":
        return(f"{strain} complete sequence")
    elif choice == "chromosome":
        return(f"{strain} chromosome")

def codonAnalysis(sequence, choice=["T3s", "C3s", "A3s", "G3s", "cai", "cbi", "fop", "enc", "GC3s", "GC", "Len_sym", "Len_aa", "hydropathy", "aromaticity"]):
    cseq = codon.CodonSeq(sequence)
    temp = cseq.silent_base_usage()
    data = {i: temp[i] for i in temp.index}
    temp = cseq.bases2()
    data = data | {i: temp[i] for i in temp.index}
    data["cai"] = cseq.cai()
    data["cbi"] = cseq.cbi()
    data["fop"] = cseq.fop()
    data["enc"] = cseq.enc()
    data["hydropathy"] = cseq.hydropathy()
    data["aromaticity"] = cseq.aromaticity()
    return ({i: round(data[i], 5) for i in choice}, data)

def putUpData(filepath=None, fileobject=None):
    if fileobject == None and filepath==None:
        return(print("fileobject or filepath can not be null"))
    elif filepath!= None:
        fileobject = open(filepath, "r").read()
    tempList = fileobject.replace("\n", "").split(">lcl|")[1:]
    tempList2 = []
    for genome in tempList:
        temp={"locus_tag":"","protein_id":"","hypothetical protein":False}
        for j in genome.split("]")[:-1]:
            if "locus_tag" in j:
                temp["locus_tag"] = j.replace("[","").split("locus_tag=")[-1]
            if "protein_id" in j:
                temp["protein_id"] = j.replace("[","").split("protein_id=")[-1]
            if "hypothetical protein" in j:
                temp["hypothetical protein"] = True
        temp["sequence"] = genome.split("]")[-1].replace(" ", "")
        tempList2.append(temp)
    return(tempList2)

def putDownData(jsonFile=[], downFilePath ="", accession=""):
    if jsonFile == []:return(print("fileobject or filepath can not be null"))
    if downFilePath == "": return(print("fileobject or filepath can not be null"))
    for data in jsonFile:
        seqText = "\n"+dumpSequence(data["sequence"])
        dumpFile(f"{downFilePath}", f">lcl|{accession} [locus_tag={data['locus_tag']}] [protein_id={data['protein_id']}] {'[protein=hypothetical protein]' if data['hypothetical protein'] == True else ''} {seqText}")

def createZip(folderpath = "", fileName=""):
    with zipfile.ZipFile(f"./Temp/dump/{fileName}.zip", "w") as zip:
        for root, directories, files in os.walk(folderpath):
            for file in files:
                shutil.copy(os.path.join(root, file),file)
                zip.write(file)
                os.remove(file)
                print(os.path.join(root, file))
    return(f"./Temp/dump/{fileName}.zip")
