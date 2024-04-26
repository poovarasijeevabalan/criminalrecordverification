from WebAutomationActivities import Activity
from selenium.webdriver.common.by import By

def sub_registery_html_save(link, webpage_save_path):
    activity = Activity("Chrome", maximize=True)
    driver = activity.browser()
    activity.url_navigate(link, delay_after=2)


    # Get the page source
    page_source = driver.page_source

    # Save the page source to a file
    with open(webpage_save_path, "w", encoding="utf-8") as html_file:
        html_file.write(page_source)

    # Close the browser
    driver.quit()

    print("Webpage saved as 'offender_page.html'")

if __name__ == "__main__":
    sub_registery_html_save("https://vspsor.com/Offender/Details/c69b27b5-f598-4800-b1e8-4dc06fdbfe65", "offender_page1.html")


