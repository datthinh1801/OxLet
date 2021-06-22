# Oxford-API
## Installation guide
Go to the [download](https://www.python.org/downloads/) page of Python and download the latest version of Python 3 of your operating system.  

Then, execute the following commands, one-by-one, to install:  
```
git clone https://github.com/datthinh1801/Oxford-API.git
cd Oxford-API
pip install -r requirements.txt
```  

Another option is to go to the [release](https://github.com/datthinh1801/Oxford-API/releases) tab of this repository and download the latest version.
> `zip` file will be supported on multiple platforms, whereas `tar.gz` works best on Unix-based OS only (e.g. MacOS, Linux, Ubuntu, etx.).  


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
> **For non-tech user:** In order to create a vocabulary list from a file, you need to copy that file into the directory (folder) of this tool.

### Examples
#### Reading new vocabs from a file
I have a file (named `input.txt` residing in the same directory of this tool) containing my new vocabulary as followed:  
```
inquire
insist
straightforward
sort out
```

I want the results to be written to another file called `output.txt` which resides in the same directory of this tool. The command will be:  
Windows:
```
py oxford_api.py -f input.txt -o output.txt
```  

Linux:
```
python3 oxford_api.py -f input.txt -o output.txt
```  

> You don't need to create the `output.txt` file beforehand. This tool will do it for you.

#### Reading new vocabs directly on console
Windows:
```
py oxford_api.py -w "inquire, insist, straightforward, sort out" -o output.txt
```

Linux:
```
python3 oxford_api.py -w "inquire, insist, straightforward, sort out" -o output.txt
```  

The output file will be:
```
inquire|(verb) ask for information from someone
e.g. he inquired about cottages for sale

insist|(verb) demand something forcefully, not accepting refusal
e.g. she insisted on carrying her own bag

straightforward|(adjective) uncomplicated and easy to do or understand
e.g. in a straightforward case no fees will be charged

sort_out|(verb) arrange things systematically in groups or according to type
e.g. she sorted out the clothes, some to be kept, some to be thrown away

```  

### Currently supported elements
| Element | Is supported ?|
|---|---|
| Terminology | Yes |
| Pronunciation | No |
| Word form | Yes *(to some extent, as idioms and phrasal verbs are still not supported)* |
| Definition | Yes |
| Example | Yes |  

## Integrate to Quizlet
This tool uses `|` as the separator between the terminology and the definition, `n\n` (a blank line) between 2 different words. Therefore, if you are about to use this output file for [Quizlet](https://quizlet.com/latest), you should do as the followings:
- Create a new study set (or add to an existing one).  
  ![image](https://user-images.githubusercontent.com/44528004/122899307-e9ad1180-d375-11eb-91d4-45d6b24cd6ec.png)  

- Click `Import from Word, Excel, Google Docs, etc.`.  
  ![image](https://user-images.githubusercontent.com/44528004/122899407-01849580-d376-11eb-8e4c-4e4124d782a5.png)  
  
  
- Specify the separator.  
  ![image](https://user-images.githubusercontent.com/44528004/122899600-28db6280-d376-11eb-94ca-53915302f08f.png)  
  
- Finally, copy the whole contents of the `output.txt` to the textbox in Quizlet and you are done!  

#### Happy learning 🎉

