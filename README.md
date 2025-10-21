# Pipeline-TEI2HTML
This repository contains the steps of the pipeline adapted to the needs of the MEGV project to process the result of the inference of a set of files from the ANOM COL-E collection. The objective is to :
- delete the content of DigitizationArtefactZone and StampZone that are useless.
- compile all the .tei files resulting from the inference with a python script of the digital facsimiles of the archives per folder.
- correct these files and format them so that they are compatible with the XML format.
- compile all the .tei files obtained per folder into a single XML-TEI file containing the entire selected corpus.
- if this XML-TEI corpus file is too large to be displayed correctly by a browser, divide it using a python script into several XML-TEI files.
- From this XML-TEI file containing the selected corpus, obtain one or more HTML pages which will make it easier to consult the results for the first time, by carrying out a full-text search.


# How to use 

To use this pipeline: 
## Phase 1: PYTHON: Compilation of data and file - XML-TEI corpus
- Add your inferred folders to "Pipeline-TEI2HTML/PYTHON/data".
- If necessary, change the information contained in the ‘’Pipeline-TEI2HTML/PYTHON/tei_header.xml‘’ file
- in your Terminal :
  - activate a virtual environment such as yaltaienv, if you have installed the rtk environment on your computer.
  - go to "Pipeline-TEI2HTML/PYTHON", then run the various scripts one after the other:

    0_remove_artefact_zones.py
      => Deletes the content of DigitizationArtefactZone and StampZone, preserve other zones.

    1_clean_tei.py
      => Cleans the .tei file by removing all tags, restructures by adding simple TEI tags <p> and <lb/>
    
    2_compile_tei_by_file.py
      => Group files by folder

    3_correct_tei.py
      => Adds namespace and standard TEI structure

    4_validation_tei.py
      => Validates XML compliance
    
    5_compile_files2corpus.py
      -> Compile the complete corpus

    if necessary (more than 500 000 lines in your XML-TEI file will crash your HTML page) :
    
    6_divide_xml.py
      => Divide the corpus into manageable parts

You should have one or more XML-TEI files created at the end of this first phase, in "Pipeline-TEI2HTML/PYTHON/output".

## Phase 2: WEB INTERFACE: Conversion to HTML format
- Open the .xpr file "Pipeline-TEI2HTML/PipeLine_COL-E.xpr" in Oxygen XML.
- In "Pipeline-TEI2HTML/Web_interface", open the script "tei2html.xsl".
- Click on "Configure transformation scenarios", select and tick "tei2html" in the list displayed, then "Edit".
- A page opens: 
In the XSLT tab
XML URL: search your folders for the path to your XML-TEI corpus file (or files), which should be "Pipeline-TEI2HTML/PYTHON/output"
XSL URL: search for the path to the tei2html. xslt script, which must be "Pipeline-TEI2HTML/Web_interface/tei2html.xsl"
 Click on the Output tab, opposite "Save as", and enter the output path you want for your HTML page(s), which must be "Pipeline-TEI2HTML/Web_interface/output/".

# Licences

CC-BY-NC.

<a rel="license" href="https://creativecommons.org/licenses/by/2.0"><img alt="Creative Commons License" style="border-width:0" src="https://upload.wikimedia.org/wikipedia/commons/d/d3/Cc_by-nc_icon.svg" /></a><br /> 
