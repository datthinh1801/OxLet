# OxLet
A tool to generate a vocabulary list which eases the process of creating a Quizlet study set, using Oxford API.  

<p align="center">
  <img height=150 width=150 src="https://www.oxfordlearnersdictionaries.com/us/external/images/home_2020/OLD_home_productsOALD.png?version=2.1.31">
</p>  
<p align="center">
  <img src="https://github.com/datthinh1801/Oxford-API/actions/workflows/dependencies.yml/badge.svg">
  <img src="https://github.com/datthinh1801/OxLet/actions/workflows/functionalities.yml/badge.svg">
</p>  

## Installation guide
### Step 1: Download Python 3
Go to the [download](https://www.python.org/downloads/) page of Python and download the latest version of Python 3 for your operating system. Then follow the instruction of the installation wizard to install Python 3 for your computer.  
> Note that there are 2 major versions which are **Python 2** and **Python 3**. Make sure you select **Python 3** and download it.

### Step 2: Download this tool
Go to the [release tab](https://github.com/datthinh1801/Oxford-API/releases) ***(👈 click this)*** and click the icon ![image](https://user-images.githubusercontent.com/44528004/123025868-836fcf80-d405-11eb-9c6b-15c390b8cfb6.png) of the latest version to download the compressed file of this tool.  

Then, you need to decompress (or extract) the downloaded file before moving on to **step 3**.  

### Step 3: Install dependencies
After downloading the tool, follows this instruction to install it.
#### Windows
![](https://github.com/datthinh1801/OxLet/blob/main/media/win10_install.gif)  

#### MacOS
![](https://github.com/datthinh1801/OxLet/blob/main/media/OxLet_Mac_installation.gif)  

> Now you're ready to use.

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

### Parameters explaination
| Parameter | Meaning |
|---|---|
| `-w` | A list of words that you want to look up. Every 2 words shoud be separated by a comma or a comma followed by a space and all word must be enclosed in a pair of quotes _(either single quotes `' '` or double quotes `" "` are ok)_. |
| `-f` | Specify the name of the input file containing your new words. |
| `-o` | Specify the name of the output file. |  

> **Note that:** `-o` is required while only one of the `-w` and the `-f` should be selected at a time.   

### Format of the input file (if used)
#### File extension
The input file should be a text file (`.txt`) for the best performance.  
#### File format
The format of the contents of the input file should be **one word per line** or **one phrase per line**, and no separators such as `,` or `.` is required.  

For example:  
```
inquire
insist
straightforward
sort out
```

## Examples
### Read new words from a file
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

### Read new words directly
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

### Demo
This demo reads new words from a file but you can feed new words to the tool directly using the `-w` followed by a doubly-quoted string of your new words like the above example.  
#### Windows
![](https://github.com/datthinh1801/OxLet/blob/main/media/OxLet_Win_demo.gif)  

#### MacOS
![](https://github.com/datthinh1801/OxLet/blob/main/media/OxLet_mac.gif)  
> **Note that:** You only need to run the `pip install -r requirements.txt` at the first time you download the tool. In following times, you just need to run the `python3 oxlet.py 

## Currently supported elements
| Element | Is supported ? |
|---|---|
| Terminology | Yes |
| Pronunciation | No |
| Word form | Yes *(to some extent, as idioms and phrasal verbs are yet supported)* |
| Definition | Yes |
| Example | Yes |  

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

