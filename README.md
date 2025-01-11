# INDY Systems Data Export Tool

This repository contains a Python script to log in to INDY Systems' admin portal, scrape user data, and export it to a CSV file. The script uses Selenium for browser automation and is designed to handle pagination while scraping.

---

## Features

- **Automated Login**: Logs into the INDY Systems admin portal using credentials.
- **Data Scraping**: Extracts user data from the "Users" section of the portal, handling multiple pages of results.
- **CSV Export**: Saves the scraped data in a structured CSV format for easy analysis.

---

## Prerequisites

1. **Python 3.8+**: Ensure Python is installed on your system.
2. **Google Chrome**: Install the latest version of Google Chrome.
3. **ChromeDriver**: Download the appropriate ChromeDriver for your Chrome version. You can find it [here](https://googlechromelabs.github.io/chrome-for-testing/#stable).
   - Place the downloaded `chromedriver.exe` in the `chromedriver-win64` folder or update the path in the script.

---

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/benmcnelly/indy-export.git
    cd indy-export
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

    Create a `requirements.txt` file in the repository with the following content:
    ```plaintext
    selenium
    ```

---

## Configuration

Update the following constants in the script:

1. **Driver Path**: Ensure the `DRIVER_PATH` variable points to the correct location of your ChromeDriver binary.
    ```python
    DRIVER_PATH = "./chromedriver-win64/chromedriver.exe"
    ```

2. **Credentials**: Replace `EMAIL` and `PASSWORD` with your INDY Systems admin portal credentials:
    ```python
    EMAIL = "youremail@yourdomain.com"
    PASSWORD = "your_password@"
    ```
   **Important**: Avoid hardcoding sensitive credentials. Consider using environment variables or a `.env` file.

---

## Usage

1. Run the script:
    ```bash
    python scrape.py
    ```

2. The script will:
   - Log in to the INDY Systems admin portal.
   - Navigate to the "Users" section.
   - Scrape user data, handling pagination.
   - Export the data to a CSV file named `users.csv` in the same directory.

---

## Important Note

Due to possible changes on the INDY Systems website:
- You may need to **manually navigate to the "Users" tab** after logging in. 
- If the script encounters issues with pagination, you might need to manually click the "Next" button on the users page.
- **Mileage may vary**, but the script worked for us in its current state.

---

## Output Example

The exported CSV will contain sanitized user data with the following structure:

| ID       | First Name | Last Name | Email               | Phone       | User Class | Membership Type | Membership Tier | Membership State | Movies Watched | Created At           |
|----------|------------|-----------|---------------------|-------------|------------|-----------------|-----------------|------------------|----------------|----------------------|
| 1189108  | Ben      | McNelly    | me@benmcnelly.com |             | Adult      | Cinima CLub |                 | ✔                | 0              | Jan 11, 2019, 4:55 PM |

---

## Sanitization

To protect user data:
- Ensure sensitive credentials and output files are not exposed publicly.
- Modify or redact personal information before sharing output files.
- For demo purposes, replace sensitive fields (e.g., `Email`) in the CSV output.

---

## Troubleshooting

1. **WebDriver Errors**: Ensure your ChromeDriver version matches your Chrome version.
2. **Timeout Errors**: Increase the `WebDriverWait` timeout values in the script if your internet connection is slow.
3. **Login Issues**: Verify your credentials and ensure the INDY Systems admin portal is accessible.
4. **Manual Navigation**: If the script fails to navigate to the "Users" page or handle pagination, perform these actions manually and rerun the script.

---

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any improvements or bug fixes.
