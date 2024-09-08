# lnk2j
Easy extraction of LNK files to json or jsonl

- Uses LibParse3 to extract individual lnks 
- Recursively search directories and extracts lnks
- Appends file timestamp MAC times
- Optional output as json or jsonl

usage: lnk2j.py [-h] -i INPUT  [-f {json,jsonl}] [-o OUTPUT] <br>
required: -i/--input (file or directory
