from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Path to ChromeDriver in the chromedriver-win64 folder
DRIVER_PATH = "./chromedriver-win64/chromedriver.exe"

# Base URLs
LOGIN_URL = "https://admin.indy.systems/#/login"
BASE_URL = "https://admin.indy.systems/#/operations/customers/users"

def initialize_driver():
    """
    Initialize the Selenium WebDriver.
    """
    service = Service(DRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    return driver

def login_and_navigate(driver, email, password):
    """
    Log into the website and directly navigate to the users page.
    """
    try:
        # Open the login page
        print("Opening login page...")
        driver.get(LOGIN_URL)

        # Wait for the login form to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-test-id='email-input']"))
        )
        print("Login page loaded. Locating email and password fields...")

        # Find email and password fields
        email_input = driver.find_element(By.CSS_SELECTOR, "input[data-test-id='email-input']")
        password_input = driver.find_element(By.CSS_SELECTOR, "input[data-test-id='password-input']")

        # Enter credentials
        print("Entering credentials...")
        email_input.send_keys(email)
        password_input.send_keys(password)

        # Find and click the login button
        login_button = driver.find_element(By.CSS_SELECTOR, "button[data-test-id='login-submit-button']")
        print("Clicking login button...")
        login_button.click()

        # Explicitly navigate to the users page
        print("Navigating to the users page...")
        driver.get(BASE_URL)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.q-table tbody tr"))
        )
        print("Users page loaded successfully!")

    except Exception as e:
        print(f"An error occurred during login or navigation: {e}")
        driver.quit()
        exit()

def scrape_users_with_selenium(driver):
    """
    Scrape user data using Selenium after navigating to the users page.
    """
    print("Waiting for the user data page to load...")
    try:
        # Wait for the user table to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.q-table tbody tr"))
        )
        print("User data page loaded. Starting to scrape users...")
    except Exception as e:
        print(f"Failed to load user data page: {e}")
        driver.quit()
        exit()

    users = []
    page = 1

    while True:
        print(f"Scraping page {page}...")

        # Locate the table rows
        rows = driver.find_elements(By.CSS_SELECTOR, "table.q-table tbody tr")

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells:
                user = {
                    "ID": cells[0].text.strip(),
                    "First Name": cells[2].text.strip(),
                    "Last Name": cells[3].text.strip(),
                    "Email": cells[4].text.strip(),
                    "Phone": cells[5].text.strip() if len(cells) > 5 else "",
                    "User Class": cells[6].text.strip(),
                    "Membership Type": cells[7].text.strip(),
                    "Membership Tier": cells[8].text.strip(),
                    "Membership State": "✔" if "check" in cells[9].get_attribute("innerHTML") else "✘",
                    "Movies Watched": cells[12].text.strip(),
                    "Created At": cells[13].text.strip()
                }
                users.append(user)

        # Check for the next page button
        try:
            print("Looking for the next page button...")
            next_button = driver.find_element(By.CSS_SELECTOR, "button.q-btn.q-btn-item.q-btn--flat.q-btn--round.q-btn--dense:not([disabled])")

            # Remember the first row of the current page
            first_row_text = rows[0].text if rows else None

            print("Clicking next page button...")
            next_button.click()

            # Wait for the table rows to change
            WebDriverWait(driver, 10).until(
                lambda d: d.find_elements(By.CSS_SELECTOR, "table.q-table tbody tr")[0].text != first_row_text
            )
            print(f"Successfully loaded new data for page {page + 1}!")

            page += 1
        except Exception as e:
            print(f"No more pages or an error occurred: {e}")
            break

    print("Finished scraping users.")
    return users


def save_to_csv(users, filename="users.csv"):
    """
    Save the scraped data to a CSV file.
    """
    if not users:
        print("No users to save.")
        return

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=users[0].keys())
        writer.writeheader()
        writer.writerows(users)
    print(f"Saved {len(users)} users to {filename}.")

if __name__ == "__main__":
    # Replace these with your login credentials
    EMAIL = "youremail@yourdomain.com"
    PASSWORD = "your_password"

    # Initialize WebDriver
    driver = initialize_driver()

    # Log in and navigate to the users page
    login_and_navigate(driver, EMAIL, PASSWORD)

    # Scrape user data
    users = scrape_users_with_selenium(driver)

    # Save data to CSV
    save_to_csv(users)

    # Quit the browser
    driver.quit()
