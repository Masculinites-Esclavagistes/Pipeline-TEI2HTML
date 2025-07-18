# Pipeline-TEI2HTML
This repository contains the steps of the pipeline adapted to the needs of the MEGV project to process the result of the inference of a set of files from the ANOM COL-E collection. The objective is to
- to compile all the .tei files resulting from the inference with a python script of the digital facsimiles of the archives per folder.
- correct these files and format them so that they are compatible with the XML format.
- compile all the .tei files obtained per folder into a single XML-TEI file containing the entire selected corpus.
- if this XML-TEI corpus file is too large to be displayed correctly by a browser, divide it using a python script into several XML-TEI files.
- From this XML-TEI file containing the selected corpus, obtain one or more HTML pages which will make it easier to consult the results for the first time, by carrying out a full-text search.

  
# Licences

CC-BY-NC.

<a rel="license" href="https://creativecommons.org/licenses/by/2.0"><img alt="Creative Commons License" style="border-width:0" src="https://upload.wikimedia.org/wikipedia/commons/d/d3/Cc_by-nc_icon.svg" /></a><br /> 
