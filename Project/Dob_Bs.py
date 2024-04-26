import requests
from bs4 import BeautifulSoup
import re

def DOB_Extraction(url):

  try:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    age_and_dob_div = soup.find(lambda tag: tag.name == 'div' and 'Age:' in tag.text)
    # Extract the text from the Age and DOB div
    age_and_dob_text = age_and_dob_div.text.strip()

    # Use regular expression to extract the DOB
    dob_match = re.search(r'\(DOB:\s*([0-9/]+)\)', age_and_dob_text)

    if dob_match:
        return dob_match.group(1)
    else:
        return "NA"
  except:
     return 'Error'


if __name__ == "__main__":
  url = "https://mspsor.com/Home/OffenderDetails?id=fe724fd2-1037-4cc8-b3ba-00a1bf30640b"
  DOB_Extraction(url)

   

