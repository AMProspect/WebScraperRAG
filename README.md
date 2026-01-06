# WebScraperRAG

## How to run the code

1. check to see if you have python installed.

    Open up a command line by searching "Command Prompt" in the windows search bar
    Once it's opened, type "python --version"
        if numbers come up, then you have it downloaded
    
    if you don't have python downloaded, open the "Microsoft Store" app
    In the store, search "Python 3 11" and download "Python 3.11"

2. Travel to the folder in command line.

    Once you download the zip file, find somewhere on your computer to open it up. Once you open the folder, right-click the file path and click "Copy adress as text"

    open up a "Command Prompt" Window and type "cd (your file path here)"

    The line where you are typing should now be the path that you entered

3. Donwload all necesarry packages.

    If you have Python downloaded you should have access to the "pip" command 
    which allows you to install python packages

    I have a list of packages you used in "requirements.txt" 

    once you are in the project folder in the command prompt, run the command 
    "pip install -r requirements.txt" 

    This will install all of the packages you need.

4. Edit .env file with you open ai API key (Note, this is if you want to run my chat interface. If you only care about using the webscraper, then skip this step).

    in file explorer, click on .env file and open it with notepad (or some other text editor).
    (if you dont see this file, click on the "view" tab in the file explorer window, look at the Show/hide section on the right, and make sure "hidden items" is checked). 

    In there, you should find a line that says "OPENAI_API_KEY=".

    Add you open ai key to this line. (Chris should know what it is).

5. (Part 1) - Update browserclass.py.

    Go to "https://servpro.interactgo.com/Interact/Pages/Section/ContentListing.aspx?subsection=3524" and check how many pages of companies there are. (At the time of making this there are 12)

    Once you find this number, open browserclass.py with a text editor. Near the top, there is a variable called "num_pages"

    Change the number to however many pages of companies there are on the website.

5. (Part 2) - Update login credentials (If needed)

    If you changed your login credentials, then open "login_cred.py" in a text editor and change the username and password variables.

6. Run get_companies.py

    This function gets the names of all of the companies on the website.

    run it by typing "python get_companies.py"

    (Note: When you run these functions, a window will pop up and you can see that it is working)

7. Run bulletins.py

    This function goes to each company link and downloads the bulletin. (This takes a long time)

    run this by typing "python bulletins.py".

    If you want to get every companies bulletin, make sure to delete all of the companies from the "Data" file. If you want to re-scrape only a few, then delete only those files from the "Data" file. The way it works is if the company is already in the data file, it wont get the bulletin for that company.

    Make sure to keep on eye on this part because sometimes it crashes. If this happens, run it again using "python bulletins.py" and it will continue where it left off.

8. Check to make sure there are no bad files.

    Sometimes there will be a few files that didn't download properly for a few different reasons (Crash or a company hasn't published the bulletin yet)

    To find these bad files, run "python populate_database.py". This creates a database for you to ask chat gpt questions from. 

    When you run this, it will start ingesting the files from our "Data" file (You will see the lines poping up in the command line saying Loading: XYZ Company). The program will stop running if it comes across a bad file. (Bad file = corrupt pdf file). You can see which company it failed on by checking the last file that was being ingested in the command line. Go to that company folder and try opening the pdf to make sure this is the problem.
    
    You will have to go to the companies page and downlaod it manually and put it into the company folder. Make sure to name the pdf 
    "(company_name) - Servpro.pdf" That is the naming convention we agreed on.

    If you go to manually download it and the bulletin page is not published (I've seen them say 'coming soon'), then open "bulletins.py" in a text editor and add that company to the "skip_companies" list at the top of the file. Make sure to delete the company folder from the "Data" file if you added it to the skip companies list. 

    If there are no corrupt files, this function should run through without erroring out. 

9. Ask Chat GPT a question from the documents

    run the following in the command prompt "python query_data.py '(your question here)'"


### Final Notes
    When edditing a file in text editor, make sure to save your changes.
    If you need any help or if something doesn't work, don't hesitate reach out.
    It's been fun working on this project with you guys and I hope people find it helpful!
