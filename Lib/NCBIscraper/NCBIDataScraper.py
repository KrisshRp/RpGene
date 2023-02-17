import time, os, requests
from .. import Driver
from datetime import datetime
from selenium.webdriver.common.by import By
from ..module import dumpSequence, dumpFile, convartURL, backDoorUrl, codonAnalysis, csvAppend, putUpData

class NCBIscraper:
    def checkDownload(self, text):
        self.log(f"\n[{str(datetime.now())}] >> [{self.sequenceId}] :: {text}")
        while True:
            if "COMPLETE" in self.driver.find_elements(By.CLASS_NAME ,"fixedbox")[-1].text:return(True)
            if self.driver.find_elements(By.CLASS_NAME ,"fixedbox")[-1].text == "":return(False)
            yield("\r" + f"> [{self.sequenceId}] :: {text} -> {self.driver.find_elements(By.CLASS_NAME, 'fixedbox')[-1].text.split(':')[-1]}")
            time.sleep(2)
    
    def fetchTotalSequence(self):
        totalSequence = self.driver.find_element(By.ID,"viewercontent1").text
        self.BaseText = totalSequence.split("\n")[0]
        self.totalSequence = totalSequence.replace("\n", "").split(" ")[-1]
        self.totalSequence = self.totalSequence.replace("genome", "").replace("sequence", "")
        self.log(f"\n[{str(datetime.now())}] >> [{self.sequenceId}] :: Writing total sequence")
        dumpFile(self.basepath, totalSequence, mode="w")
        return(True)

    def setCustomeView(self, url):
        self.log(f"\n[{str(datetime.now())}] >> [{self.sequenceId}] :: Fatchting encoded sequence")
        # print(f"> [{self.sequenceId}] :: sending request to server")
        self.driver.get(url)
        time.sleep(3)
        try:self.driver.find_element(By.ID ,"SCDshowsel").click()
        except:
            self.driver.find_element(By.ID ,"EntrezSystem2.PEntrez.Nuccore.Sequence_ResultsPanel.Sequence_SingleItemSupl.Sequence_ViewerGenbankSidePanel.Sequence_ViewerCustomizer.Shutter").click()
            try:self.driver.find_element(By.ID ,"SCDshowcustomize").click()
            except:pass
            self.driver.find_element(By.ID ,"SCDshowsel").click()
        self.driver.find_element(By.ID ,"SCDshowseq").click()
        self.driver.find_element(By.ID ,"SCDsetview").click()
        time.sleep(3)
        if self.checkDownload("Downloading encoded sqeuence"):
            return(True)
        else:
            self.log(f"\n[{str(datetime.now())}] >> [{self.sequenceId}] :: Getting error to download encoded sequence")
            return(False)

    def fetchSequence(self):
        egList, negList, = [], []
        blockCount = 0
        sequenceBlocks = self.driver.find_elements(By.CLASS_NAME, "feature")
        self.log(f"\n[{str(datetime.now())}] >> [{self.sequenceId}] :: Writing encoded sequence")
        totalNucleotide = int(sequenceBlocks[0].text.split("\n")[0].replace(" ","").split("..")[-1])
        cds, trna, rrna= 0,0,0
        Nucleotides = requests.get(backDoorUrl(self.ncbiuid, "FASTA Nucleotide")).text
        Proteins = requests.get(backDoorUrl(self.ncbiuid, "FASTA Protein")).text
        for index, block in enumerate(sequenceBlocks):
            if "CDS" in block.get_attribute("id") or "tRNA" in block.get_attribute("id") or "rRNA" in block.get_attribute("id") :
                blockText = block.text
                hypothetical = True if "hypothetical protein" in blockText else False
                cds += 1 if "CDS" in block.get_attribute("id") else 0
                trna += 1 if "tRNA" in block.get_attribute("id") else 0
                rrna += 1 if "rRNA" in block.get_attribute("id") else 0

                #___clean text_______
                blockText = blockText.replace(" ", "").replace("<", "").replace(">", "").replace('"',"").replace("/","").replace("complement","").replace("join","").replace("(","").replace(")","")
                
                #___fetch limit______
                blockLimit = [i for i in blockText.split("\n")[0].replace("CDS","").replace("tRNA","").replace("rRNA","").split("..")]
                if len(blockLimit)>2:del(blockLimit[1])
                blockLimit = [int(i) for i in blockLimit]
                blockLimit[0] -= 1

                #___fetch block sequence___
                sequence = self.totalSequence[blockLimit[0]:blockLimit[1]]
                analysisData2 = codonAnalysis(sequence=sequence)[0]
                analysisData = {}
                seqText = "\n"+dumpSequence(sequence)

                #____fetch locus______
                blockLocus, blockOldLocus = None, None
                if "locus_tag" in blockText:
                    blockLocus = blockText.split("locus_tag")[1].split("\n")[0].replace("=","")
                if  "old_locus_tag" in blockText:
                    blockOldLocus = blockText.split("old_locus_tag")[1].split("\n")[0].replace("=","")

                #____fetch protin_____
                protinID, translation = None, None
                if "protein_id" in blockText:
                    protinID = blockText.split("protein_id")[1].split("\n")[0].replace("=","")
                if "translation" in blockText:
                    translation = "\n"+dumpSequence(blockText.split("translation")[1].replace("=","").replace("\n",""))

                #________HEG__________
                if blockOldLocus in self.Gene_Locus and hypothetical:
                    dumpFile(f"{self.basepath}_HEG", f">lcl|{self.sequenceId} [locus_tag={blockOldLocus}] [protein=hypothetical protein] {seqText}")
                    egList.append(blockOldLocus)
                    if protinID is not None and translation is not None:
                        dumpFile(f"{self.basepath}_P_HEG", f">lcl|{self.sequenceId} [locus_tag={blockOldLocus}] [protein_id={protinID}] [protein=hypothetical protein] {translation}")
                    analysisData["Locus_tag"] = blockOldLocus
                    analysisData2["target"]="EG"
                    analysisData.update(analysisData2)
                    csvAppend(f"{self.basepath}-HEG.csv", analysisData)
                elif blockLocus in self.Gene_Locus and hypothetical:
                    dumpFile(f"{self.basepath}_HEG", f">lcl|{self.sequenceId} [locus_tag={blockLocus}] [protein=hypothetical protein] {seqText}")
                    egList.append(blockLocus)
                    if protinID is not None and translation is not None:
                        dumpFile(f"{self.basepath}_P_HEG", f">lcl|{self.sequenceId} [locus_tag={blockLocus}] [protein_id={protinID}] [protein=hypothetical protein] {translation}")
                    analysisData["Locus_tag"] = blockLocus
                    analysisData2["target"]="EG"
                    analysisData.update(analysisData2)
                    csvAppend(f"{self.basepath}-HEG.csv", analysisData)

                #________EG__________
                elif blockOldLocus in self.Gene_Locus:
                    dumpFile(f"{self.basepath}_EG", f">lcl|{self.sequenceId} [locus_tag={blockOldLocus}] {seqText}")
                    egList.append(blockOldLocus)
                    if protinID is not None and translation is not None:
                        dumpFile(f"{self.basepath}_P_EG", f">lcl|{self.sequenceId} [locus_tag={blockOldLocus}] [protein_id={protinID}] {translation}")
                    analysisData["Locus_tag"] = blockOldLocus
                    analysisData2["target"]="EG"
                    analysisData.update(analysisData2)
                    csvAppend(f"{self.basepath}-EG.csv", analysisData)
                elif blockLocus in self.Gene_Locus:
                    dumpFile(f"{self.basepath}_EG", f">lcl|{self.sequenceId} [locus_tag={blockLocus}] {seqText}")
                    egList.append(blockLocus)
                    if protinID is not None and translation is not None:
                        dumpFile(f"{self.basepath}_P_EG", f">lcl|{self.sequenceId} [locus_tag={blockLocus}] [protein_id={protinID}] {translation}")
                    analysisData["Locus_tag"] = blockLocus
                    analysisData2["target"]="EG"
                    analysisData.update(analysisData2)
                    csvAppend(f"{self.basepath}-EG.csv", analysisData)

                #________HNEG__________
                elif blockOldLocus is not None  and hypothetical:
                    dumpFile(f"{self.basepath}_HNEG", f">lcl|{self.sequenceId} [locus_tag={blockOldLocus}] [protein=hypothetical protein] {seqText}")
                    negList.append(blockOldLocus)
                    if protinID is not None and translation is not None:
                        dumpFile(f"{self.basepath}_P_HNEG", f">lcl|{self.sequenceId} [locus_tag={blockOldLocus}] [protein_id={protinID}] [protein=hypothetical protein] {translation}")
                    analysisData["Locus_tag"] = blockOldLocus
                    analysisData2["target"]="NEG"
                    analysisData.update(analysisData2)
                    csvAppend(f"{self.basepath}-HNEG.csv", analysisData)
                elif blockLocus is not None and hypothetical:
                    dumpFile(f"{self.basepath}_HNEG", f">lcl|{self.sequenceId} [locus_tag={blockLocus}] [protein=hypothetical protein] {seqText}")
                    negList.append(blockLocus)
                    if protinID is not None and translation is not None:
                        dumpFile(f"{self.basepath}_P_HNEG", f">lcl|{self.sequenceId} [locus_tag={blockLocus}] [protein_id={protinID}] [protein=hypothetical protein] {translation}")
                    analysisData["Locus_tag"] = blockLocus
                    analysisData2["target"]="NEG"
                    analysisData.update(analysisData2)
                    csvAppend(f"{self.basepath}-HNEG.csv", analysisData)

                #________NEG___________
                elif blockOldLocus is not None:
                    dumpFile(f"{self.basepath}_NEG", f">lcl|{self.sequenceId} [locus_tag={blockOldLocus}]  {seqText}")
                    negList.append(blockOldLocus)
                    if protinID is not None and translation is not None:
                        dumpFile(f"{self.basepath}_P_NEG", f">lcl|{self.sequenceId} [locus_tag={blockOldLocus}] [protein_id={protinID}] {translation}")
                    analysisData["Locus_tag"] = blockOldLocus
                    analysisData2["target"]="NEG"
                    analysisData.update(analysisData2)
                    csvAppend(f"{self.basepath}-NEG.csv", analysisData)
                elif blockLocus is not None:
                    dumpFile(f"{self.basepath}_NEG", f">lcl|{self.sequenceId} [locus_tag={blockLocus}] {seqText}")
                    negList.append(blockLocus)
                    if protinID is not None and translation is not None:
                        dumpFile(f"{self.basepath}_P_NEG", f">lcl|{self.sequenceId} [locus_tag={blockLocus}] [protein_id={protinID}] {translation}")
                    analysisData["Locus_tag"] = blockLocus
                    analysisData2["target"]="NEG"
                    analysisData.update(analysisData2)
                    csvAppend(f"{self.basepath}-NEG.csv", analysisData)

                #____if locus and old locus is NONE___
                else:pass
                blockCount+=1
                yield("\r" + f"> [{self.sequenceId}] :: {blockCount} -- {blockLocus} -- {blockLimit} [{totalNucleotide-blockLimit[-1]}]{5*' '}")


        if len(egList) != len(self.Gene_Locus):
            yield("\n")
            dumpList = [locus for locus in self.Gene_Locus if locus not in egList]
            Nucleotides = putUpData(fileobject=Nucleotides)
            Proteins = putUpData(fileobject=Proteins)
            unDumpList = []
            for Nucleotide, Protein in zip(Nucleotides, Proteins):

                if Nucleotide["locus_tag"] in dumpList:
                    egList.append(Nucleotide["locus_tag"])
                    analysisData2 = codonAnalysis(sequence=sequence)[0]
                    analysisData2["target"]="EG"
                    analysisData = {"Locus_tag": Nucleotide["locus_tag"]}
                    analysisData.update(analysisData2)
                    unDumpList.append(Nucleotide["locus_tag"])
                    if Nucleotide["hypothetical protein"]:
                        dumpFile(f"{self.basepath}_HEG", f">lcl|{self.sequenceId} [locus_tag={Nucleotide['locus_tag']}] [protein=hypothetical protein] {dumpSequence(Nucleotide['sequence'])}")
                        dumpFile(f"{self.basepath}_P_HEG", f">lcl|{self.sequenceId} [locus_tag={Nucleotide['locus_tag']}] [protein_id={Nucleotide['protein_id']}] [protein=hypothetical protein] {dumpSequence(Protein['sequence'])}")
                        csvAppend(f"{self.basepath}-HEG.csv", analysisData)
                    if not Nucleotide["hypothetical protein"]:
                        dumpFile(f"{self.basepath}_EG", f">lcl|{self.sequenceId} [locus_tag={Nucleotide['locus_tag']}] {dumpSequence(Nucleotide['sequence'])}")
                        dumpFile(f"{self.basepath}_P_EG", f">lcl|{self.sequenceId} [locus_tag={Nucleotide['locus_tag']}] [protein_id={Nucleotide['protein_id']}] {dumpSequence(Protein['sequence'])}")
                        csvAppend(f"{self.basepath}-EG.csv", analysisData)
                    yield("\r" + f"> [{self.sequenceId}] :: {Nucleotide['locus_tag']} added")
                
                if Nucleotide["locus_tag"] not in egList and Nucleotide["locus_tag"] not in negList:
                    negList.append(Nucleotide["locus_tag"])
                    analysisData2 = codonAnalysis(sequence=sequence)[0]
                    analysisData2["target"]="NEG"
                    analysisData = {"Locus_tag": Nucleotide["locus_tag"]}
                    analysisData.update(analysisData2)
                    unDumpList.append(Nucleotide["locus_tag"])
                    if Nucleotide["hypothetical protein"]:
                        dumpFile(f"{self.basepath}_HNEG", f">lcl|{self.sequenceId} [locus_tag={Nucleotide['locus_tag']}] [protein=hypothetical protein] {dumpSequence(Nucleotide['sequence'])}")
                        dumpFile(f"{self.basepath}_P_HNEG", f">lcl|{self.sequenceId} [locus_tag={Nucleotide['locus_tag']}] [protein_id={Nucleotide['protein_id']}] [protein=hypothetical protein] {dumpSequence(Protein['sequence'])}")
                        csvAppend(f"{self.basepath}-HNEG.csv", analysisData)
                    if not Nucleotide["hypothetical protein"]:
                        dumpFile(f"{self.basepath}_NEG", f">lcl|{self.sequenceId} [locus_tag={Nucleotide['locus_tag']}] {dumpSequence(Nucleotide['sequence'])}")
                        dumpFile(f"{self.basepath}_P_NEG", f">lcl|{self.sequenceId} [locus_tag={Nucleotide['locus_tag']}] [protein_id={Nucleotide['protein_id']}] {dumpSequence(Protein['sequence'])}")
                        csvAppend(f"{self.basepath}-NEG.csv", analysisData)
                    yield("\r" + f"> [{self.sequenceId}] :: {Nucleotide['locus_tag']} added")
                
            dumpText = '\n'.join(dump for dump in dumpList if dump not in unDumpList)
            dumpFile(f"{self.basepath}_Dump", f"{dumpText}")

        print("\n",len(egList), len(negList))
        dumpFile(f"{self.basepath}_count-log", f"Accession : {self.sequenceId} \nE-Path gene number : {len(self.Gene_Locus)} \nNCBI Coding Seq : {len(Nucleotides)} \nFatched Coding Seq : {blockCount} \nFatched CDS Seq : {cds} \nFatched tRNA Seq : {trna} \nFatched rRNA Seq : {rrna} \nFatched NEG Seq : {len(negList)} \nFatched EG Seq : {len(egList)}")
        self.log(f"\n{str(datetime.now())} |-> Accession :{self.sequenceId} |-> E-Path gene number :{len(self.Gene_Locus)} |-> NCBI Coding Seq :{len(Nucleotides)} |-> Fatched Coding Seq :{blockCount} |-> Fatched CDS Seq :{cds} |-> Fatched tRNA Seq :{trna} |-> Fatched rRNA Seq :{rrna} |-> Fatched NEG Seq :{len(negList)} |-> Fatched EG Seq :{len(egList)}" , 
            type="datalimit")

    def log(self, log, type="general"):
        with open('./Temp/log/NCBIscrap.log' if type == "general" else './Temp/log/dbLimits.log','a+') as outfile:outfile.write(log)

    def run(self):
        print("running script")
        yield("\r" + f"\n--------------[{self.organism}]--------------\n")
        
        yield("\r" + f"> [{self.sequenceId}] :: sending request to server\n")
        self.driver.get(f"{self.url}?report=fasta")
        self.ncbiuid = self.driver.find_element(By.XPATH, "//meta[@name='ncbi_uidlist']").get_attribute("content")

        for responce in self.checkDownload("Downloading total sqeuence"):
            if responce != True or responce != False:
                yield(responce)
            elif responce == True:
                self.log(f"\n[{str(datetime.now())}] >> [{self.sequenceId}] :: Fatchting total sequence")
            elif responce == False:
                self.log(f"\n[{str(datetime.now())}] >> [{self.sequenceId}] :: Getting error to download total sequence")
                return(f"\n get error from server")
        
        self.fetchTotalSequence()
        yield("\r" + f"> [{self.sequenceId}] :: sending request to server\n")

        if self.setCustomeView(self.url):
            self.log(f"\n[{str(datetime.now())}] >> [{self.sequenceId}] :: Custom view updated")
        else:
            return("\n get error ")
        for responce in self.checkDownload("Downloading encoded sqeuence"):
            if responce != True or responce != False:
                yield(responce)
            elif responce == True:
                self.log(f"\n[{str(datetime.now())}] >> [{self.sequenceId}] :: Writing encoded sequence")
            elif responce == False:
                self.log(f"\n[{str(datetime.now())}] >> [{self.sequenceId}] :: Getting error to download encoded sequence")
                return(f"\n get error from server")
        for responce in self.fetchSequence():
            yield(responce)
        self.driver.close()

    def __init__(self, organism="", ascession="", Gene_Locus=[], choice="complete genome", driver=None, log=True, headless=False, basepath="./", proxy=None):
        self.baseUrl = "https://www.ncbi.nlm.nih.gov/nuccore"
        self.organism = organism
        self.qurl = convartURL(self.baseUrl, self.organism)

        self.sequenceId = ascession
        self.Gene_Locus = Gene_Locus
        self.url = f"{self.baseUrl}/{self.sequenceId}"
        os.makedirs(f"./Temp/scrapdata/{self.sequenceId}",mode=0o777)
        self.basepath = f"./Temp/scrapdata/{self.sequenceId}/{self.sequenceId}"

        if driver is None:
            self.driver = Driver(log=log, headless=headless, downloadPath=f"\Temp\scrapdata\{self.sequenceId}").driver
        else:self.driver = driver

        print(self.url)
        # os.system(f"cd ./Temp/scrapdata & mkdir {self.sequenceId}")
        
        dumpFile(f"{self.basepath}_gene_locus", str(self.Gene_Locus).replace("'","").replace("[","").replace("]","").replace(", "," \n"))
