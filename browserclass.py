import time 
import re
import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from login_cred import username as u
from login_cred import password as p
from typing import List, Tuple, Dict, Union, Optional
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from retrying import retry
from selenium.common.exceptions import ElementClickInterceptedException


class Browser:
    browser, service = None, None

    def __init__(self, driver: str):
        self.service = Service(driver)
        self.chrome_options = Options()

        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Set download_dir relative to the script's location
        self.download_dir = os.path.join(script_dir, "Data")  # Specify your download directory

        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,  # Disable download prompt
            "plugins.always_open_pdf_externally": True
        }

        self.chrome_options.add_experimental_option("prefs", prefs)

        self.browser = webdriver.Chrome(service=self.service, options=self.chrome_options)

    # Open a URL
    def open_page(self, url: str):
        self.browser.get(url)
    
    # Close the browser
    def close_browser(self):
        self.browser.close()

    # Type out text in input field (Used for Login)
    def add_input(self, by: By, value: str, text: str):
        field = self.browser.find_element(by=by, value=value)
        field.send_keys(text)
        time.sleep(1)

    # Click Login Button
    def click_button(self, by: By, value: str):
        button = self.browser.find_element(by=by, value=value)
        self.browser.execute_script("arguments[0].removeAttribute('target');", button)
        button.click()
        time.sleep(1)
    
    # Log into Servpro Website
    def login_servpronet(self, username: str, password: str):
        self.add_input(by=By.ID, value='Username', text=username)
        self.add_input(by=By.ID, value='Password', text=password)
        self.click_button(by=By.CLASS_NAME, value='btn.btn-primary.override_width_100')

    # Get the name of every company available and returns a list of them. 
    def get_company_list(self) -> List[List[str]]:

        comps = []

        for i in range(1,12):
            c = []
            self.click_button(by=By.XPATH, value=f"//a[@data-page='{i}']")

            table = self.browser.find_elements(by=By.ID, value="cat-search")

            for company in (table[0].text).split("\n"):
                if len(company) >= 3 and "continued" not in company:
                    c.append(company)
            
            comps.append(c)

        return comps


    
    # Download Bulletin for each company
    # @retry(stop_max_attempt_number=3, wait_fixed=1000, retry_on_exception=ElementClickInterceptedException)
    def download_bulletins(self, company: str, page: int):

        
        # Go back to search page
        self.open_page("https://servpro.interactgo.com/Interact/Pages/Section/ContentListing.aspx?subsection=3524")

        print()
        print(f"Fethcing {company} Bulletin")
        
        time.sleep(2)

        # Special Cases
        if company == "Chubb Symbility Change - Summer 2023 - PowerPoint Deck":
            company = "Chubb Insurance Group"
            self.open_page("https://servpro.interactgo.com/page/11891")
            time.sleep(2)
        
        elif company == "American Family Insurance Claims Service (AFICS)":
            self.open_page("https://servpro.interactgo.com/page/3492")
            time.sleep(2)
        
        elif company == "Nationwide Insurance":
            self.open_page("https://servpro.interactgo.com/page/3636")
            time.sleep(2)


        else:
            # Go to proper group page if necessary
            if page+1 == 11:
                self.click_button(by=By.XPATH, value=f"//a[@data-page='{8}']")
                time.sleep(1)

            if page+1 != 1:
                self.click_button(by=By.XPATH, value=f"//a[@data-page='{page+1}']")
                time.sleep(1)
            
            # Click on specific company tab 
            self.click_button(by=By.XPATH, value=f'//a[@title="{company}"]')

            time.sleep(2)

        print("Got into Company Page")
        ## Get to download page
        if company not in ["Chubb Symbility Change - Summer 2023 - PowerPoint Deck", "American Family Insurance Claims Service (AFICS)", "Nationwide Insurance"]:
            # Find Bulletin Link and click on it
            button = self.browser.find_elements(by=By.XPATH, value=f"//a[contains(@href, '/Interact/Pages/Content/Document')]")

            # check for the right link to click on. Most of the time they have a structure like this ####-(S)F
            for option in button:
                if re.search(r"\d{4,}-.?F", option.text):
                    self.browser.execute_script("arguments[0].removeAttribute('target');", option)
                    option.click()
                    break
                    
        
        time.sleep(2)

        print("Got to Download Page")
        ### Download File
        files = self.browser.find_elements(by=By.XPATH, value=f"//a[contains(@href, '/Utilities/Uploads/Handler/Uploader')]")
        for file in files:
            if file.get_attribute('href') and '.pdf' in file.get_attribute('href'):

                file.click()
                time.sleep(5)

                downloaded_file = max([self.download_dir + "/" + f for f in os.listdir(self.download_dir)], 
                                        key=os.path.getctime)  # Get the most recent file
            
                company = company.replace("/", " - ")
                new_filename = os.path.join(self.download_dir, f"{company}.pdf")  # Set your desired name
                os.rename(downloaded_file, new_filename)
                break
        
        print("Downloaded File")

        time.sleep(2)

        return


    def company_folder_exists(self, company_name: str):
        """
        Check if a folder with the company name exists in the base directory.
        
        Args:
            company_name (str): The name of the company to check.
            base_dir (str): The base directory to look in (default is your Data folder).
        
        Returns:
            bool: True if the folder exists, False otherwise.
        """
        company_path = os.path.join("./Data", company_name)
        return os.path.isdir(company_path)


    def create_company_folder_with_pdf(self, company_name: str):
        """
        Create a folder for the company and ensure a file named '<company_name>.pdf' is in it.
        
        Args:
            company_name (str): The name of the company.
            base_dir (str): The base directory where the company folder will be created.
        
        Returns:
            str: Path to the created/moved PDF file.
        """
        # Create the company folder
        company_dir = os.path.join("./Data", company_name)
        os.makedirs(company_dir, exist_ok=True)  # Creates folder if it doesn’t exist

        # Define the target PDF filename
        pdf_filename = f"{company_name}.pdf"
        target_pdf_path = os.path.join(company_dir, pdf_filename)

        # Check if the file exists in the base directory (e.g., after a download)
        source_pdf_path = os.path.join("./Data", pdf_filename)
        if os.path.exists(source_pdf_path):
            # Move the file to the company folder
            shutil.move(source_pdf_path, target_pdf_path)
            print(f"Moved {pdf_filename} to {company_dir}")
        else:
            # If the file doesn’t exist, create an empty one (or handle as needed)
            with open(target_pdf_path, "w") as f:
                f.write("")  # Creates an empty file; adjust if you have content
            print(f"Created empty {pdf_filename} in {company_dir}")

        return target_pdf_path


if __name__ == "__main__":
    browser = Browser(".\driver\\chromedriver.exe")
#     print("Openning Browser.")
#     browser.open_page("https://servpro.interactgo.com/Interact/Pages/Section/ContentListing.aspx?subsection=3524")
#     time.sleep(1)

#     print("Logging In")
#     browser.login_servpronet(u, p)
#     time.sleep(5)
#     print("Logged In.")

#     print()

#     print("Getting Company List.")
#     groups = browser.get_company_list()
#     time.sleep(1)

#     save_file = "./companies.py"
#     # Write the variable assignment to companies.py
#     with open(save_file, "w") as f:
#         f.write(f"companies = {groups}\n")

#     print(f"Saved list to {save_file}")

#     # browser.download_bulletins(groups)
#     # browser.download_bulletins([[], ["BPL Plasma Inc."]])

#     time.sleep(1)

#     print("Closing Browser.")
#     browser.close_browser()

    # browser.create_company_folder_with_pdf("7-Eleven, Inc.")
