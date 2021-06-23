# OxLet
A tool to generate a vocabulary list to create a Quizlet study set, using Oxford API.  

<p align="center">
  <img height=150 width=150 src="https://www.oxfordlearnersdictionaries.com/us/external/images/home_2020/OLD_home_productsOALD.png?version=2.1.31">
</p>  
<p align="center">
  <img src="https://github.com/datthinh1801/Oxford-API/actions/workflows/dependencies.yml/badge.svg">
  <img src="https://github.com/datthinh1801/OxLet/actions/workflows/python-ci.yml/badge.svg">
</p>  

## Installation guide
### Step 1: Download Python 3
Go to the [download](https://www.python.org/downloads/) page of Python and download the latest version of Python 3 of your operating system. Then follow the instruction of the installation setup wizard to install Python 3 for your computer.  

### Step 2: Download this tool
Then, open your terminal (or command prompt in Windows 10) and execute the following command to download this tool.   
```
git clone https://github.com/datthinh1801/Oxford-API.git
```  

A preferred way to download this tool is to go to the [release tab](https://github.com/datthinh1801/Oxford-API/releases) ***(👈 click the link)*** of this repository and download the latest version.
> `zip` file will be supported on multiple platforms, whereas `tar.gz` works best on Unix-based OS only (e.g. MacOS, Linux, Ubuntu, etc.).  

***If you download the tool from the **Release** tab, you should extract it before moving on to the next steps.***

### Step 3: Install prerequisites
On your terminal, execute the following commands to install the prerequisites:  
```
cd Oxford-API
pip install -r requirements.txt
```  

If you're not familiar with terminal and don't know how to `cd`, do the followings:
- Open the directory **Oxford-API**.  
- Right click on a space within the directory.  
- Select **Open with terminal** or something like that.  
- Execute the command `pip install -r requirements.txt` on the terminal.

Now, you are ready to go.

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

### Parameters explaination
| Parameter | Meaning |
|---|---|
| `-w` | A list of words that you want to look up. These words shoud be separated by commas or a comma followed by a space and enclosed in a pair of quotes _(either single quotes `' '` or double quotes `" "` are ok)_. |
| `-f` | Specify the name of input file containing your new words *(e.g. `input.txt`, `my_words.txt`, etc.)*. |
| `-o` | Specify the name of the output file *(e.g. `output.txt`, `words.txt`, etc.)*. |  

> **Note that:** `-o` is required while only one of the `-w` and the `-f` should be selected at a time.  

> **For non-tech user:** In order to create a vocabulary list from a file, you need to copy that file into the same directory (folder) of this tool.  

### Format of the input file (if used)
#### File extension
The input file should be a text file (`.txt`) for the best performance.  
#### File format
The format of the contents of the input file should be **one word/phrase per line**, and no separators such as `,` or `.` is required.  

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
py oxford_api.py -f input.txt -o output.txt
```  

Linux:
```
python3 oxford_api.py -f input.txt -o output.txt
```  

> You don't need to create the `output.txt` file beforehand. This tool will do it for you.

### Read new words directly on console
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

## Currently supported elements
| Element | Is supported ? |
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

