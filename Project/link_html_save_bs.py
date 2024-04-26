import requests
from bs4 import BeautifulSoup

def sub_registery_html_page(url, web_page_save_path):
# Define the URL
 

  # Send a GET request to the URL
  response = requests.get(url)

  # Check if the request was successful (status code 200)
  if response.status_code == 200:
      # Parse the HTML content using BeautifulSoup
      soup = BeautifulSoup(response.text, "html.parser")

      # Save the parsed HTML content to a file
      with open(web_page_save_path, "w", encoding="utf-8") as html_file:
          html_file.write(soup.prettify())

      print("Webpage saved as 'offender_page.html'")
  else:
      print("Failed to fetch the webpage. Status code:", response.status_code)

if __name__ == "__main__":
    url = r"https://sor.csosa.net/GenerateBulletinPublic.aspx?id=lQ0IdDIciRXtQt1EpscK5w%3d%3d"
    web_page_save_path = "offender_page2.html"
    sub_registery_html_page(url, web_page_save_path)