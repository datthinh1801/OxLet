# Oxford-API
## Usage
```
usage: oxford_api.py [-h] [-w [WORDS]] [-f [INFILE]] [-o [OUTFILE]]

optional arguments:
  -h, --help            show this help message and exit
  -w [WORDS], --words [WORDS]
                        a list of words/phrases separated by commas (e.g. sustainable, take a toll)
  -f [INFILE], --file [INFILE]
                        the name of the file to read from (e.g. newwords.txt)
  -o [OUTFILE], --output [OUTFILE]
                        the filename to write the results to (e.g. output.txt)
``` 

### Examples
#### Reading new vocabs from a file
I have a file (named `input.txt`) containing my new vocabulary as followed:
```
inquire
insist
straightforward
sort out
```

I want the results to be written to another file called `output.txt`. The command will be:  

Windows:
```
py oxford_api.py -f input.txt -o output.txt
```  

Linux:
```
python3 oxford_api.py -f input.txt -o output.txt
```  

> You don't need to create the `output.txt` file before hand.

#### Reading new vocabs directly on console
Windows:
```
py oxford_api.py -w "inquire, insist, straightforward, sort out" -o output.txt
```

Linux:
```
python3 oxford_api.py -w "inquire, insist, straightforward, sort out" -o output.txt
```
