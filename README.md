
# Text Processing and Cleaning for BRAC 2005 Closure and Realignment Impacts by Economic Area

The pdf document `2005proposal.pdf` is from the 2005 Base Realignment and Closure (BRAC) Commission.  This is a group that proposes military base changes in a process designed to insulate decisions from political interference.  Bases can be "realigned" - that is, gain or loose employment, they can be "closed" all together, or be unaffected.  The tables organize bases by which Metropolitan Statistical Area (Note that while MOST entries are MSAs, there are some others, including counties and metropolitan divisions. Leave them all in under the header of "msas") they are a part of, followed by the proposed changes (details listed earlier in the document). The text and data are cleaned in this repository is utilized for the project in my other repository: `msa-brac-employment-spatial`.

The PDF document is included only for your reference - the file we will be working from is named 2005proposal.pdf.txt, and is the result of parsing the PDF document to extract text.  It did not come out completely clean, however. In this project, my goal is to study the text output, compare it to the source PDF, then write a script that takes in the text document and outputs a CSV document. We will parse only the table, shown as the table from page 3-48 in the PDF document.

# Files

### - Text to be processed
#### 1. `2005proposal.pdf`: Pdf to display the table output.
#### 2. `2005proposal.pdf.txt`: Actual text file to be parsed to produce the csv table.

### - Codes
#### 1. `TextProcessing.py`: Program to process the text for the final output.

### - Output
#### 1. `Table.csv`: CSV table that displays BRAC 2005 Closure and Realignment Impacts by Economic Area.

