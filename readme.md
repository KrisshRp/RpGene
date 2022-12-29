<div align="center">
  <img style="width: 75px;" src="./Bin/Assets/images/dna.png">
</div>
<div align="center">
  <h1> RpGene </h1>
</div>

**`Documentation`** |
------------------- |
[![Documentation](https://img.shields.io/badge/api-reference-blue.svg)](#) |

### [RpGene](#) : `A soft-tool for automated gene extraction, gene sequencing analysis and dataset` 

The information on gene sequences is accessible in a variety of databases that are accessible online, like `NCBI` , `DEG` , `OGEE` and many more. The extraction of information on genes however, is a challenging task to extract from these databases. In the context of machine learning one of the most fundamental demands is the data to be well-organized and usable format. Converting information about gene sequences from sequences into datasets consisting of features derived from sequences in a proper format is a difficult task for researchers. In this study, we have created a soft tool called RpGene based on Python that can perform automatizing the extraction of sequence data of genes from the NCBI database, and analyzing the data using e-Path, and presenting the user with an optimally optimized dataset that can be utilized for dataset generation in context of machine learning and other statistical studies. Our soft tool vastly decreases the time and effort required for dataset generation from gene sequence information and automates the entire process. It finally calculates the sequence features from CodonW integration and outputs a read to go dataset for further studies.

## 1. Download the reposatory
```via git download```
### Clone the reposatory
```shell
  git clone https://github.com/KrisshRp/RpGene.git
```
## 2. Enter the folder
```shell
  cd ./RpGene
```
## 3. Install the dependencies
```
  pip install -r requirements.txt
```
## 4. Provide Input Data
Update the `./RpGene/Temp/jsonDatabase/database.json` with your preferable `"organism name"` , `"NCBI accession id"` and `"ePath gene locus tags"`
## 5. Run the script

```shell
  python main.py
```
## 6. Output
*If chrome driver is downloaded*
```python
Chrome Driver is up-to-dated
```
*Else*
```python
Downloading Chrome Driver [108.0.5359.71]
100% [...................................] 6904173 / 6904173
```
```python
https://www.ncbi.nlm.nih.gov/nuccore/CP005082.1
running script
--------------[Mycobacterium tuberculosis Beijing/NITR203]--------------
> [CP005082.1] :: sending request to server
> [CP005082.1] :: sending request to servere ->  3.24MB
> [CP005082.1] :: sending request to server
> [CP005082.1] :: sending request to servere ->  13.24MB
> [CP005082.1] :: 4155 -- J112_21090 -- [4410381, 4410525] [603]          
> [CP005082.1] :: J112_12470 added 1057
```