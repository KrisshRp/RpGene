<div align="center">
  <img style="width: 75px;" src="./Bin/Assets/images/dna.png">
</div>
<div align="center">
  <h1> RpGene </h1>
</div>

| **`Documentation`**                                                        |
| -------------------------------------------------------------------------- |
| [![Documentation](https://img.shields.io/badge/api-reference-blue.svg)](#) |

#### [RpGene](#) : `A soft-tool for automated gene extraction, gene sequencing analysis and dataset`

The information on gene sequences is accessible in a variety of databases that are accessible online, like `NCBI` , `DEG` , `OGEE` and many more. The extraction of information on genes however, is a challenging task to extract from these databases. In the context of machine learning one of the most fundamental demands is the data to be well-organized and usable format. Converting information about gene sequences from sequences into datasets consisting of features derived from sequences in a proper format is a difficult task for researchers. In this study, we have created a soft tool called RpGene based on Python that can perform automatizing the extraction of sequence data of genes from the NCBI database, and analyzing the data using e-Path, and presenting the user with an optimally optimized dataset that can be utilized for dataset generation in context of machine learning and other statistical studies. Our soft tool vastly decreases the time and effort required for dataset generation from gene sequence information and automates the entire process. It finally calculates the sequence features from CodonW integration and outputs a read to go dataset for further studies.

## 1. Clone the reposatory

```shell
git clone https://github.com/KrisshRp/RpGene.git
```

## 2. Enter the folder

```shell
cd ./RpGene
```

## 3. Install the dependencies

```
sudo python3 install.py
```

## 4. start the server

```shell
sudo python3 main.py
```

## 5. Server is running

```shell
APP_PORT = 3000
INFO:     Started server process [4889]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:3000 (Press CTRL+C to quit)
INFO:     127.0.0.1:48506 - GET / HTTP/1.1 200 OK
INFO:     127.0.0.1:48506 - GET /stylesheets/main.css HTTP/1.1 200 OK
INFO:     127.0.0.1:48528 - GET /javascripts/main.js HTTP/1.1 200 OK
INFO:     127.0.0.1:48522 - GET /images/dna.png HTTP/1.1 200 OK
INFO:     127.0.0.1:33926 - GET /images/DNA-helix.mp4 HTTP/1.1 200 OK
INFO:     127.0.0.1:40292 - GET / HTTP/1.1 200 OK
```

## 6. visit the server by navigating

```shell
http://127.0.0.1:3000
```

or

```shell
http://localhost:3000
```

<div align="center">
  <img style="max-width:500px;" src="./Bin/Assets/images/output_ss/portal_SS.png">
</div>

## 7. Provide Input Data

Fill all the inputs `"organism name"` , `"NCBI accession id"` and `"ePath gene locus tags"`

<div align="center">
  <img style="max-width:500px;" src="./Bin/Assets/images/output_ss/portal_SS1.png">
</div>

Then click the "Submit" button

<div align="center">
  <img style="max-width:500px;" src="./Bin/Assets/images/output_ss/portal_SS2.png">
</div>

After that click the "Run" to start the script

#

## 8. Output

_If chrome driver is downloaded_

```python
Chrome Driver is up-to-dated
```

_Else_

```python
Downloading Chrome Driver [108.0.5359.71]
100% [...................................] 6904173 / 6904173
```

In the Console the output showls like

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

In the Portal the output showls like

<div align="center">
  <img style="max-width:500px;" src="./Bin/Assets/images/output_ss/portal_SS3.png">
</div>

Lastly click the "download" button to download the sequence data in a zip format
