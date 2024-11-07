import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


with open("test_data.json", "r") as file:
    test_data = json.load(file)

opts= webdriver.ChromeOptions()
opts.add_experimental_option("detach",True)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=opts)


def setup_browser():
    driver.get("https://testpages.herokuapp.com/styled/tag/dynamic-table.html")
    driver.maximize_window()
    driver.implicitly_wait(4)

def enter_data_and_refresh():
    table_data_button = driver.find_element(By.XPATH,"//div[@class='centered']//summary")
    table_data_button.click()
    time.sleep(1)
    print("Clicked on Table Data button and new input text box displayed:")

    input_box = driver.find_element(By.XPATH,"//textarea[@id='jsondata']")
    input_box.clear()
    input_box.send_keys(json.dumps(test_data))
    print("Successfully entered Test data into text area")

    refresh_button = driver.find_element(By.XPATH,"//button[text()='Refresh Table']")
    refresh_button.click()
    print("Clicked On Refresh Table Button")

def validate_table_data():
    table_rows = driver.find_elements(By.XPATH, "//table[@id='dynamictable']//tr")[1:]
    for i, row in enumerate(table_rows):
        cells = row.find_elements(By.TAG_NAME, "td")
        name, age, gender = cells[0].text, int(cells[1].text), cells[2].text

        # Assertion to compare UI data with JSON data
        assert name == test_data[i]["name"], f"Expected name: {test_data[i]['name']}, found: {name}"
        assert age == test_data[i]["age"], f"Expected age: {test_data[i]['age']}, found: {age}"
        assert gender == test_data[i]["gender"], f"Expected gender: {test_data[i]['gender']}, found: {gender}"
        print(f"Row {i + 1} data validated: {name}, {age}, {gender}")

def main():

    setup_browser()
    enter_data_and_refresh()
    validate_table_data()
    print("All data successfully validated.")
    driver.quit()

if __name__ == "__main__":
    main()