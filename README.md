# OxLet
A tool to generate vocabulary lists which eases the process of creating Quizlet study sets.  

<p align="center">
  <img height=100 width=100 src="https://user-images.githubusercontent.com/44528004/125007263-10fc2200-e08a-11eb-953c-90c47264fd67.png">
</p>  
<p align="center">
  <img src="https://github.com/datthinh1801/Oxford-API/actions/workflows/dependencies.yml/badge.svg">
  <img src="https://github.com/datthinh1801/OxLet/actions/workflows/functionalities.yml/badge.svg">
</p>  

## Installation guide (CLI)
```
git clone https://github.com/datthinh1801/OxLet.git
cd OxLet
pip install -r requirements.txt
```  
> This tool also has a web interface, [here](https://oxlet.herokuapp.com/).  


## Usage
```
usage: oxlet.py [-h] [-w [WORDS]] [-f [INFILE]] [-o [OUTFILE]]

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
#### Read new words from a file
I have a file (named `input.txt` residing in the same directory of this tool) containing my new words as follows:  
```
inquire
insist
straightforward
sort out
```

I want the results to be written to another file called `output.txt` which resides in the same directory of this tool. The command will be:  
Windows:
```
py oxlet.py -f input.txt -o output.txt
```  

Linux/MacOS:
```
python3 oxlet.py -f input.txt -o output.txt
```  

> You don't need to create the `output.txt` file beforehand. This tool will do it for you.

#### Read new words directly
Windows:
```
py oxlet.py -w "inquire, insist, straightforward, sort out" -o output.txt
```

Linux/MacOS:
```
python3 oxlet.py -w "inquire, insist, straightforward, sort out" -o output.txt
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

## Currently supported
| Element | Is Supported? |
|---|---|
| Terminology | Yes |
| Pronunciation | Yes |
| Word form | Yes |
| Definition | Yes |
| Example | Yes |  

| Dictionary | Is Supported? |
|---|---|
| Oxford Learner's Dictionary | Yes |
| Cambridge Dictionary | Yes |
| Macmillan Dictionary | No |
| Longman Dictionary | No |
| Merriam-Webster Dictionary | No |

## Integrate to Quizlet
This tool uses `|` as the separator between the terminology and the definition, `\n\n` (a blank line) between 2 different words. Therefore, if you are about to use this output file for [Quizlet](https://quizlet.com/latest), you should do as the followings:
- Create a new study set (or add to an existing one).  
  ![image](https://user-images.githubusercontent.com/44528004/122899307-e9ad1180-d375-11eb-91d4-45d6b24cd6ec.png)  

- Click `Import from Word, Excel, Google Docs, etc.`.  
  ![image](https://user-images.githubusercontent.com/44528004/122899407-01849580-d376-11eb-8e4c-4e4124d782a5.png)  
  
  
- Specify the separator.  
  ![image](https://user-images.githubusercontent.com/44528004/122899600-28db6280-d376-11eb-94ca-53915302f08f.png)  
  
- Finally, copy the whole contents of the `output.txt` to the textbox in Quizlet and you are done!  

As an example, Quizlet perfectly understand the format of this tool.  
![image](https://user-images.githubusercontent.com/44528004/123089609-5d701c80-d451-11eb-9f3f-262ed617707e.png)


#### Happy learning 🎉

