from browserclass import Browser
import time
from login_cred import username as u
from login_cred import password as p


if __name__ == "__main__":
    browser = Browser(r"C:\\Users\\amore\Web PDF Scraper\driver\\chromedriver.exe")
    print("Openning Browser.")
    browser.open_page("https://servpro.interactgo.com/Interact/Pages/Section/ContentListing.aspx?subsection=3524")
    time.sleep(1)

    print("Logging In")
    browser.login_servpronet(u, p)
    time.sleep(3)
    print("Logged In.")

    print()

    print("Getting Company List.")
    groups = browser.get_company_list()
    time.sleep(1)

    save_file = "./companies.py"
    # Write the variable assignment to companies.py
    with open(save_file, "w") as f:
        f.write(f"c = {groups}\n")

    print(f"Saved list to {save_file}")

    time.sleep(1)

    print("Closing Browser.")
    browser.close_browser()