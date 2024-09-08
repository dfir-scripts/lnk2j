# lnk2j
Extract single or multiple LNK files to json or jsonl

- Uses [LibParse3](https://github.com/Matmaus/LnkParse3) Python package to extract lnk metadata
- Parse individual files or recursively search directories
- Appends file timestamp MAC times to output
- Results as json or jsonl

<b>usage:<br> lnk2j.py [-h] -i INPUT  [-f {json,jsonl}] [-o OUTPUT] </b><br><br>
<b><i>required:</b><br> 
 -i --input (file or directory)<br><br>
<b>optional:</b><br>-f {json,jsonl} --format {json,jsonl}  (Output format).<br>
  -o output, --output OUTPUT (Output file name)
