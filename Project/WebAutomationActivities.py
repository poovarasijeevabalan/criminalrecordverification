import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
import pandas as pd

class Activity:
    def __init__(self, browser_type, maximize, **kwargs):
        """Initialize the Activity class.

        Parameters:
        - browser_type (str): Type of browser to be used ("Edge" or "Chrome").
        - maximize (bool): Whether to maximize the browser window or not.
        - **kwargs: Additional keyword arguments, such as 'ignore_ssl'.
        """
        self.browser_type = browser_type
        self.ignore_ssl = kwargs.get('ignore_ssl', False)
        self.maximize = maximize

    def round_int(self, number):
        """Round a number to the nearest integer.

        Parameters:
        - number (float): The number to be rounded.

        Returns:
        - int: The rounded integer value.
        """
        if int(number) < number:
            return int(number) + 1
        else:
            return int(number)
        
    def assign_attributes(self, kwargs, attributes):
        """Assign attributes based on provided keyword arguments.

        Parameters:
        - kwargs (dict): The keyword arguments provided.
        - attributes (list): List of attribute names to assign.

        This method is used internally by other methods to assign attributes from keyword arguments.
        """
        self.delay_before = kwargs.get('delay_before', 0.3) if 'delay_before' in attributes else None
        self.delay_after = kwargs.get('delay_after', 0) if 'delay_after' in attributes else None
        self.continue_on_error = kwargs.get('continue_on_error', True) if 'continue_on_error' in attributes else None
        self.timeout = self.round_int(kwargs.get('timeout', 1)) if 'timeout' in attributes else None


    def browser(self):
        """Launch the specified browser.

        Returns:
        - WebDriver: Instance of the browser driver.
        """
        if self.browser_type == "Edge":
            edge_options = EdgeOptions()
            edge_options.use_chromium = True  
            if self.ignore_ssl:
                edge_options.add_argument('--ignore-certificate-errors')  
            self.driver = webdriver.Edge(options=edge_options)

        elif self.browser_type == "Chrome":
            chrome_options = ChromeOptions()
            if self.ignore_ssl:
                chrome_options.add_argument('--ignore-certificate-errors')
                chrome_options.add_argument('--ignore-certificate-errors-spki-list')
            self.driver = webdriver.Chrome(options=chrome_options)

        if self.maximize:
            self.driver.maximize_window()
        return self.driver
        
    def url_navigate(self, url, **kwargs):
        """Navigate to a specified URL.

        Parameters:
        - url (str): The URL to navigate to.
        - **kwargs: 
            - delay_before (float): Default delay before value is 0.3 seconds.
            - delay_after (float): Default delay after value is 0 seconds.
        """
        attributes = ['delay_before', 'delay_after']
        self.assign_attributes(kwargs, attributes)

        time.sleep(self.delay_before)
        self.driver.get(url)
        time.sleep(self.delay_after)

    def click(self, xpath, **kwargs):
        """Perform a click operation on a web element.

        Parameters:
        - xpath (str): The XPath of the element to click.
        - **kwargs: 
            - delay_before (float): Default delay before value is 0.3 seconds.
            - delay_after (float): Default delay after value is 0 seconds.
            - continue_on_error (bool): Default continue_on_error value is True.
            - timeout (int): Default timeout value is 5 seconds.
        """
        attributes = ['delay_before', 'delay_after', 'continue_on_error', 'timeout']
        self.assign_attributes(kwargs, attributes)

        time.sleep(self.delay_before)
            
        for _ in range(0, self.timeout):
            try:
                element = self.driver.find_element(By.XPATH, xpath)
                element.click()
                time.sleep(self.delay_after)
                return True
            except Exception:
                if _ == self.timeout - 1:
                    if not self.continue_on_error:
                        return False
                    raise
                time.sleep(1)
                    
    def sendkeys(self, xpath, str_value, **kwargs):
        """Send keys to a web element.

        Parameters:
        - xpath (str): The XPath of the element.
        - str_value (str): The string value to be sent.
        - **kwargs: 
            - clear (bool): Default clear value is False
            - delay_before (float): Default delay before value is 0.3 seconds.
            - delay_after (float): Default delay after value is 0 seconds.
            - continue_on_error (bool): Default continue_on_error value is True.
            - timeout (int): Default timeout value is 5 seconds.
        """
        attributes = ['delay_before', 'delay_after', 'continue_on_error', 'timeout']
        self.assign_attributes(kwargs, attributes)
        
        clear = kwargs.get("clear", False)

        time.sleep(self.delay_before)

        for _ in range(0, self.timeout):
            try:
                element = self.driver.find_element(By.XPATH, xpath)
                if clear:
                    element.clear()
                element.send_keys(str_value)
                time.sleep(self.delay_after)
                return True
            except Exception:
                if _ == self.timeout - 1:
                    if not self.continue_on_error:
                        return False
                    raise
                time.sleep(1)

    def element_exist(self, xpath, timeout, **kwargs):
        """Check if an element exists within a given timeout.

        Parameters:
        - xpath (str): The XPath of the element.
        - timeout (int): Timeout duration in seconds.
        - **kwargs: Additional keyword arguments.

        Returns:
        - bool: True if element exists within the timeout, False otherwise.
        """
        timeout = self.round_int(timeout)
        for _ in range(0, timeout):
            try:
                self.driver.find_element(By.XPATH, xpath)
                return True
            except Exception:
                if _ == timeout - 1:
                    return False
                time.sleep(1)
            

    def get_text(self, xpath, **kwargs):
        """Retrieve text content from a web element.

        Parameters:
        - xpath (str): The XPath of the element.
        - **kwargs: 
            - delay_before (float): Default delay before value is 0.3 seconds.
            - delay_after (float): Default delay after value is 0 seconds.
            - continue_on_error (bool): Default continue_on_error value is True.
            - timeout (int): Default timeout value is 5 seconds.

        Returns:
        - str: The text content of the element.
        """
        attributes = ['delay_before', 'delay_after', 'continue_on_error', 'timeout']
        self.assign_attributes(kwargs, attributes)
    
        time.sleep(self.delay_before)
            
        for _ in range(0, self.timeout):
            try:
                element = self.driver.find_element(By.XPATH, xpath)
                str_value = element.text
                time.sleep(self.delay_after)
                return str_value
            except Exception:
                if _ == self.timeout - 1:
                    if not self.continue_on_error:
                        return ""
                    raise
                time.sleep(1)

    def get_html_table(self, xpath, **kwargs):
        """Retrieve HTML table data and convert it to a DataFrame.

        Parameters:
        - xpath (str): The XPath of the HTML table.
        - **kwargs: 
            - header_required (bool): Default header required value is True
            - delay_before (float): Default delay before value is 0.3 seconds.
            - delay_after (float): Default delay after value is 0 seconds.
            - continue_on_error (bool): Default continue_on_error value is True.
            - timeout (int): Default timeout value is 5 seconds.

        Returns:
        - pd.DataFrame: DataFrame containing the HTML table data.
        """
        attributes = ['delay_before', 'delay_after', 'continue_on_error', 'timeout']
        self.assign_attributes(kwargs, attributes)

        header_required = kwargs.get("header_required", True)
        
        time.sleep(self.delay_before)

        for _ in range(0, self.timeout):
            header_row = []
            table_rows = []
            try:
                table_element = self.driver.find_element(By.XPATH, xpath)
                rows = table_element.find_elements(By.TAG_NAME, "tr")
                for row in rows:
                    th_data_row=[]
                    try:
                        cols = row.find_elements(By.TAG_NAME, "th")
                        th_row = [col.text for col in cols]
                        if len(th_row)>0:
                            if header_required:
                                header_row = th_row
                                continue
                            else:
                                th_data_row = th_row
                    except Exception:
                        if header_required:
                            print("no header in this table")
                            raise
                    cols = row.find_elements(By.TAG_NAME, "td")
                    data_row = [col.text for col in cols]
                    if len(th_row)>0:
                        data_row=th_data_row + data_row
                    if data_row:
                        table_rows.append(data_row)
                    
                    
                
                time.sleep(self.delay_after)
                return pd.DataFrame(table_rows, columns=header_row if header_row else None)
                
            except Exception:
                if _ == self.timeout - 1:
                    if not self.continue_on_error:
                        return pd.DataFrame()
                    raise
                time.sleep(1)
