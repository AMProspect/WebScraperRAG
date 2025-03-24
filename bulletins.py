from browserclass import Browser
import time
from login_cred import username as u
from login_cred import password as p
from companies import c

skip_companies = ["AvantStay, Inc.", "CBRE/Cisco","Chick-fil-A Flow Through Agreement", "Chubb Small Commercial Pilot slide deck",
                          "City Facilities Management Flow Through Agreement", "Country Financial Best Practices",
                          "Country Financial Workflow", "City Facilities Management Flow Through Agreement",
                          "Go Wireless", "Havenbrook Homes", "Hippo Insurance", "HomeSafe Alliance", "Lidl US Operation LLC", 
                          "MB2 Dental", "Pearce Services, LLC", "PNC Trust Real Estate", "Shelter Insurance Company - TN",
                          ]


if __name__ == "__main__":
    browser = Browser("./driver/chromedriver.exe")
    print("Openning Browser.")
    browser.open_page("https://servpro.interactgo.com/Interact/Pages/Section/ContentListing.aspx?subsection=3524")
    time.sleep(1)

    print("Logging In")
    browser.login_servpronet(u, p)
    time.sleep(3)
    print("Logged In.")

    print()

    for page in range(0, len(c)):
        for company in c[page]:
            
            # Skip skip_companies 
            if company in skip_companies:
                continue

            # Check if "Chubb Insurance Group" folder has been made
            if browser.company_folder_exists("Chubb Insurance Group") == True:
                continue

            # Download Bulletin, Create Company Folder, Add file to folder
            if browser.company_folder_exists(company.replace("/", " - ")) == False:

                try:
                    browser.download_bulletins(company, page)
                except Exception as e:
                    print(f"\n***********\nFailed because of misclick: \n\n{e}\n\nTrying Again\n***********")
                    browser.download_bulletins(company, page)

                if company == "Chubb Symbility Change - Summer 2023 - PowerPoint Deck":
                    company = "Chubb Insurance Group"

                company = company.replace("/", " - ")
                browser.create_company_folder_with_pdf(company)


    time.sleep(1)

    print("Closing Browser.")
    browser.close_browser()