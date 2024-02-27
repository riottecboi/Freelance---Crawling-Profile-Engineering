from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class ProfileEngineeringCrawler():
    def __init__(self):
        self._endResults = {}
        # Set up Chrome WebDriver
        self.chrome_options = ChromeOptions()
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")

        # Path to your Chrome WebDriver executable
        self.chrome_driver_path = "xxxxxx" #### Place to your chromedriver on your machine

        # Initialize Chrome WebDriver
        self.driver = Chrome(self.chrome_driver_path, options=self.chrome_options)

    def close_driver(self):
        self.driver.quit()

    def main(self):
        url = "https://americansocietyforengineeringeducation.shinyapps.io/profiles/"

        # Open the URL in Chrome
        self.driver.get(url)
        print(f"Successful access to {url}")

        # Wait for the Tenured/Tenure-Track Falcuty to be clickable
        tabSelection = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "web_button"))
        )

        # Click on the Tenured/Tenure-Track Falcuty
        tabSelection.click()

        # Find the dropdown element by its ID
        dropdown_element = self.driver.find_element_by_id("yrrr3")

        # Create a Select object from the dropdown element
        dropdown = Select(dropdown_element)

        sleep(5)

        # Select the option with the value "2022"
        dropdown.select_by_value("2022")

        sleep(3)

        dummy_element = self.driver.find_element_by_id("exp3")
        dummy_dropdown = Select(dropdown_element)

        dummy_ele = self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/div[4]/div[5]/div/div/div/div[2]/div[4]/div/div/div")
        hidden_ele = self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/div[4]/div[5]/div/div/div/div[2]/div[4]/div/div/div/div[2]")

        hidden_list_institutions = self.driver.find_elements_by_class_name("selectize-dropdown-content")

        institutions_list_id = hidden_list_institutions[2].get_attribute('id')

        dummy_ele.click()

        script = """
            var Div = arguments[0];
            Div.style.display = 'block';  // Set the display property of the outer div to 'block'
            """
        self.driver.execute_script(script, hidden_ele)
        institutions_ele_list = self.driver.find_element_by_id(institutions_list_id)
        child_divs = institutions_ele_list.find_elements_by_xpath("./div")

        institutions_list = [child_div.text for child_div in child_divs if child_div.text != ""]

        for i in range(len(institutions_list)):
            print(f"Getting data from {institutions_list[i]}")
            headers = []
            records = []
            record = {}

            # Wait for table content to load
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "dataTables_scrollBody")))

            tableResultBody = self.driver.find_element_by_class_name("dataTables_scrollBody")
            tableBody = tableResultBody.find_element_by_xpath("./table")

            print("Headers - On progress")
            # Retrieve all the <th> elements within the table
            tableResultHeader = self.driver.find_element_by_class_name("dataTables_scrollHeadInner")
            tableHeader = tableResultHeader.find_element_by_xpath("./table")
            header = tableHeader.find_element_by_tag_name("thead")
            headerRows = header.find_elements_by_tag_name("th")

            for row in headerRows:
                if headerRows.index(row) == 8:
                    self.driver.execute_script("arguments[0].scrollLeft = arguments[0].scrollWidth", tableResultBody)
                    sleep(1)
                headers.append(row.text)

            self.driver.execute_script("arguments[0].scrollLeft = 0", tableResultBody)
            sleep(1)

            print("Records - On progress")
            # Retrieve all the <tr> elements within the table
            body = tableBody.find_element_by_tag_name("tbody")
            bodyRows = body.find_elements_by_tag_name("tr")

            for re in bodyRows:
                tmpCol = []
                reColumns = re.find_elements_by_tag_name("td")
                for col in reColumns:
                    if reColumns.index(col) == 8:
                        self.driver.execute_script("arguments[0].scrollLeft = arguments[0].scrollWidth", tableResultBody)
                        sleep(1)
                    tmpCol.append(col.text)
                record[bodyRows.index(re)] = tmpCol
            records.append(record)
            self._endResults[institutions_list[i]] = {'headers': headers, 'records': records}

            dummy_ele.click()
            script = """
                        var Div = arguments[0];
                        Div.style.display = 'block';  // Set the display property of the outer div to 'block'
                        """
            self.driver.execute_script(script, hidden_ele)
            sleep(3)
            ActionChains(self.driver).send_keys(Keys.ARROW_DOWN).perform()
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            sleep(3)
            print("--------------------------\n")


if __name__ == '__main__':
    crawler = ProfileEngineeringCrawler()
    crawler.main()
    crawler.close_driver()