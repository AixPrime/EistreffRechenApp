from time import sleep
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class Quiz:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Hides the browser window

        # Initialize the WebDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.get("http://quiz.eis-treff.de/")
        print(self.driver.title)

        self.login()
        level, count = self.choose_level()
        self.do_level(level, count)

    def login(self):
        # User inputs for credentials
        username = input("Benutzername: ")
        password = input("Passwort: ")

        # Locating and entering the login credentials
        username_entry = self.driver.find_element(By.NAME, "username")
        username_entry.send_keys(username)
        password_entry = self.driver.find_element(By.NAME, "password")
        password_entry.send_keys(password)

        # Clicking the login button
        login_button = self.driver.find_element(By.CLASS_NAME, "btn")
        login_button.click()

    def choose_level(self):
        while True:
            try:
                level = int(input("Level 1, 2 oder 3 auswaehlen (1/2/3): "))
                if 1 <= level <= 3:
                    break
                else:
                    print("1,2 oder 3 eingeben!")
            except ValueError:
                print("1,2 oder 3 eingeben!")

        while True:
            try:
                count = int(
                    input("Wie oft soll das Level gemacht werden? (1-10): ")
                )
                if 1 <= count <= 100:
                    break
                else:
                    print("Zahl zwischen 1 und 10 eingeben!")
            except ValueError:
                print("Zahl zwischen 1 und 10 eingeben!")

        return level, count

    def do_level(self, level, count):
        for _ in range(count):
            # Random sleep duration between 5 and 15 seconds
            sleep_duration = random.randint(5, 15)
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, f"Level {level}"))
            )
            self.driver.find_element(By.LINK_TEXT, f"Level {level}").click()

            # Handling the quiz logic
            self.handle_quiz()

            sleep(sleep_duration)

    def handle_quiz(self):
        # Execute JavaScript to get values
        sum_order_final = self.driver.execute_script(
            "return sumOrderFinal"
        ).replace(".", "")
        sum_change_final = self.driver.execute_script("return sumChangeFinal")

        # Early exit if change is too small
        if sum_change_final < 0.1:
            return

        # Enter the price value
        for char in sum_order_final:
            btn_xpath = (
                "//*[@id='keys']/p[4]/button[2]"
                if char == "0"
                else f"//*[@id='keys']//button[text()='{char}']"
            )
            self.driver.find_element(By.XPATH, btn_xpath).click()

        # Confirm price
        self.driver.find_element(
            By.XPATH, "//*[@id='keys']/p[4]/button[4]"
        ).click()

        # Enter change value
        btn_10c = self.driver.find_element(
            By.XPATH, "//*[@id='change']/div[5]/button"
        )
        for _ in range(int(sum_change_final / 0.1)):
            btn_10c.click()

        # Confirm change value
        self.driver.find_element(By.ID, "change_submit").click()


if __name__ == "__main__":
    Quiz()
