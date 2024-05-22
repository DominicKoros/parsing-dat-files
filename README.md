# parse dat files

> [!IMPORTANT]
> read this if you get an error, if not skip to "How to use!" part

## What to do when you get "command not found: python" or "command not found: pip"
for what ever reason when python upgraded to version 3 they decided to change the command and added a 3 to the end of it `python3`(same goes for pip)
### How can this be fixed? Just replace all `python` OR `pip` commands with `python3` OR `pip3`!
here are all of the commands, in order again
1. `pip3 install -r requirements.txt`
2. `python3 app.py "name of .dat file"`


## How to use!
### Install the Requirements.
1. open up a terminal in the same folder as the code
2. run the following `pip install -r requirements.txt` (this downloads and installs 2 projects this code depends on)

 
### Running the File
1. then we can run `python app.py "name of .dat file"`
     - an example of this would be `python app.py to_be_parsed.dat`
2. if everything goes well it should say succsess and give you the name of the excel file it created. TADA!
