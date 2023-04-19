import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
import time

#For the URL, go into Clio, Billing, then select all the filters that apply, and copy the URL from the address bar. If you want to rename all the invoices in the drafts, keep the URL below
url = "https://app.clio.com/nc/#/bills?state=%7B%22value%22:%22draft%22%7D&type=%7B%22value%22:%22%22%7D"
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

# Find email input field and enter email
email_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "email")))
email = input("Type your username: ")


email_input.send_keys(email)

# Click the next button
next_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "next"))
)
next_button.click()


# Find password input field and enter password
password_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "password"))
)
password = input("Type your password: ")
password_input.send_keys(password)

#Login button

login = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "signin"))
)
login.click()

# Find column header by ID and click on header
column_header = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div/cc-page-header/div/div/div/th-tab[1]/div/cc-page-content/div/bills-table/th-data-table/div[1]/div[1]/div/table/thead/tr/th[4]/a"))
)
column_header.click()

# Wait for the page to load
time.sleep(3)

stop_value = "7696"
row = 1

while True:
    try:
        value_xpath = f"/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div/cc-page-header/div/div/div/th-tab[1]/div/cc-page-content/div/bills-table/th-data-table/div[1]/div[2]/table/tbody/tr[{row}]/td[4]"
        fourth_column = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, value_xpath)))
        fourth_column_value = fourth_column.text

        if fourth_column_value == stop_value:
            break

        print("I'm on Invoice #: "+ fourth_column_value)

        edit_xpath = f"/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div/cc-page-header/div/div/div/th-tab[1]/div/cc-page-content/div/bills-table/th-data-table/div[1]/div[2]/table/tbody/tr[{row}]/td[2]/bill-actions/th-combo-button-basic/span/button[1]"
        edit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, edit_xpath)))
        edit_button.click()

        #Getting the description
        description_xpath = "/html/body/div[1]/div/div[1]/div/div/div/div/bills-edit-modal/div/th-modal-body/ng-transclude/form/edit-modal-data-grid/div/p/th-data-table/div[1]/div[2]/table/tbody/tr[1]/td[7]/span"
        description_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, description_xpath)))
        description = description_element.text

        # Extract the 4-digit invoice number using a regular expression
        invoice_number_match = re.search(r'\d{4}', description)
        if invoice_number_match:
            invoice_number = invoice_number_match.group(0)

            #Remove any other lines in the invoice
            line = 2
            while True:
                try:
                    additional_line_xpath = f"/html/body/div[1]/div/div[1]/div/div/div/div/bills-edit-modal/div/th-modal-body/ng-transclude/form/edit-modal-data-grid/div/p/th-data-table/div[1]/div[2]/table/tbody/tr[{line}]/td[7]"
                    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, additional_line_xpath)))

                    remove_button_xpath = f"/html/body/div[1]/div/div[1]/div/div/div/div/bills-edit-modal/div/th-modal-body/ng-transclude/form/edit-modal-data-grid/div/p/th-data-table/div[1]/div[2]/table/tbody/tr[{line}]/td[2]"
                    remove_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, remove_button_xpath)))
                    remove_button.click()
                    time.sleep(1)
                except Exception as e:
                    print("No more additional lines in invoice, saving new invoice...")
                    break

            # Paste the invoice number into the specified input field
            input_xpath = "/html/body/div[1]/div/div[1]/div/div/div/div/bills-edit-modal/div/th-modal-body/ng-transclude/form/edit-modal-invoice-details/div/div[1]/div[1]/span/th-row/span/th-row/th-column[1]/div/label/span[2]/input"
            input_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, input_xpath)))
            input_element.clear()
            input_element.send_keys(invoice_number)

            # Click the save invoice button
            save_invoice_xpath = "//*[@id='apollo-app']/div/div[1]/div/div/div/div/bills-edit-modal/div/th-modal-footer/th-button-group/th-button[1]/button/ng-transclude/span"
            save_invoice_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, save_invoice_xpath)))
            save_invoice_button.click()

        # Go back to the previous page after editing (you may need to adjust this based on the website structure)
        driver.back()
        time.sleep(3)

        row += 1
    except Exception as e:
        print("No more rows found or an error occurred.")
        break

driver.quit()
