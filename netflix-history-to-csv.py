#!/usr/bin/python3

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import codecs

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions \
    import StaleElementReferenceException, WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time
import argparse
from datetime import datetime
from datetime import datetime, timedelta


# List that is filled with strings of viewing activity
activity_list = []

# Initialising PhantomJS driver
chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# In your terminal window do a 'whereis chromedriver' to find the location of chromedriver and make sure the path below is correct.
# driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=chrome_options) # uncomment for ubuntu
driver = webdriver.Chrome(service=Service("/usr/lib/chromium-browser/chromedriver"), options=chrome_options) # uncomment this for pi

USER = ""
DAYS_WORTH_OF_HISTORY = None

def get_active_profile():
    """
    Selects Netflix profile
    """
    # Obtain profiles and names
    profiles = driver.find_elements_by_class_name('profile-icon')
    users = driver.find_elements_by_class_name('profile-name')

    # If profiles in empty, it means there is only one default profile on the account
    if profiles is not None:
        print('Selecting Profile')
        # Iterate through names to check for a match with user's profile name
        for i in range(len(profiles)):
            try:
                if users[i].text == USER:
                    # Click profile image associated with name
                    profiles[i].click()
                    navigate_site()
                elif i == len(profiles):
                    print('Error: Your profile name (\'%s\') was not found.\n' % USER
                            + '       Please check if you entered the correct profile name in \'userconfig.ini\'')
            except StaleElementReferenceException:
                pass
            except WebDriverException:
                pass

def navigate_site():
    """
    Navigates to 'Viewing Activity' page
    """
    # Wait for browse page to load
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'profile-icon')))
    print('Navigating Site')

    time.sleep(1)
    hover_clicked = hover_click()

    # Navigate to page containing viewing activity
    if hover_clicked:
        try:
            # //*[contains(@class, 'single-profile') and contains(.//*, 'Zain')]//a[@data-uia='action-viewing-activity']

            # //*[contains(@class, 'single-profile') and contains(.//*, 'Zain')]//button
            driver.find_element_by_xpath("//*[contains(@class, 'single-profile') and contains(.//*, 'Zain')]//button").click()
            time.sleep(2)
            driver.find_element_by_xpath("//*[contains(@class, 'single-profile') and contains(.//*, 'Zain')]//a[@data-uia='action-viewing-activity']").click()
            scroll_to_bottom()
        except Exception as e:
            print(e)
    else:
        print('Closing Program')

def hover_click():
    """
    Hovers on user avatar and clicks 'Your Account'
    Returns: Boolean
    """
    error_count = 0
    prof_icon_classes = [
        'account-dropdown-button'
        'profile-icon',
        'profile-name',
        'profile-arrow',
        'avatar',
        'profile-link',
        'account-dropdown-button',
        'account-menu-item',
        'current-profile'
    ]
    while True:
        try:
            # On some systems the profile icon is displayed differently.
            # For this reason the first attempt doesn't work,
            # the program searches for a different item that will do the same thing when clicked as the profile-icon
            if error_count <= 7:
                hov_profile = driver.find_element_by_class_name(prof_icon_classes[error_count])
            else:
                print('Error: Program was unable to find profile picture.\n'
                        + '       Please report this issue to m13basra@gmail.com')
                return False

            # Attempt to move to profile icon
            hov = ActionChains(driver).move_to_element(hov_profile)
            hov.perform()

            # Click on 'Your Account' which appears from drop-down menu provoked in previous step
            driver.find_element_by_link_text('Account').click()
            return True
        except:
            error_count += 1

def scroll_to_bottom():
    more_than_needed = False

    button = driver.find_elements_by_xpath('//button[text()="Show More"][contains(@class, "disabled")]')
    while not button:
        driver.find_element_by_xpath('//button[text()="Show More"]').click()
        time.sleep(2)
        button = driver.find_elements_by_xpath('//button[text()="Show More"][contains(@class, "disabled")]')
        
        if DAYS_WORTH_OF_HISTORY:
            print("Checking you days worith of history..")
            row_list = driver.find_elements_by_class_name('retableRow')
            for row, i in zip(row_list, range(1, len(row_list))):
                date_cell = row.find_elements_by_tag_name('div')[0]
                datetime_object = datetime.strptime(date_cell.text, '%d/%m/%Y')
                time_between = datetime.now() - datetime_object
                if time_between.days>DAYS_WORTH_OF_HISTORY:
                    more_than_needed = True
                    break

        if more_than_needed:
            break
    
    get_page_activity()


def get_page_activity():
    """
    Gets viewing activity and outputs into 'netflix_activity.txt'
    """
    print('Retrieving viewing activity')

    # List that contains all row elements on viewing activity page
    row_list = driver.find_elements_by_class_name('retableRow')
    # For every item viewed, appends to activity_list
    print('Progress:')
    print('\t[' + (' ' * 20) + ']' + ' 0%', end='\r')
    for row, i in zip(row_list, range(1, len(row_list))):
        date_cell = row.find_elements_by_tag_name('div')[0]
        title_cell = row.find_elements_by_tag_name('div')[1]
        datetime_object = datetime.strptime(date_cell.text, '%d/%m/%Y')
        date_string = datetime_object.strftime('%d/%m/%y')
        show_title = title_cell.text.replace(",", "")
        print(date_string + ", " + show_title)
        activity_list.append(date_string + ', ' + show_title + '\n')
        # Display progress bar to user
        percent_comp = i / len(row_list)
        fill_bar = round(19 * percent_comp)
        print('\t[' + ('#' * fill_bar) + (' ' * (20-fill_bar)) + '] ' + str(round(percent_comp*100)) + '%',
                end='\r')

    print('\t[' + ('#' * 20) + ']' + ' 100%')
    # Close driver
    driver.close()

    output_activity(activity_list)

def output_activity(activity_list):
    """
    Outputs viewing activity into 'SERVICE_activity.txt'
    """

    service = 'netflix_video'

    print('Writing activity to \'%s_history.csv\'' % service.lower())
    # Open output file
    file = codecs.open('%s_history.csv' % service.lower(), 'w+', encoding='utf8')
    # Write to file
    for item in activity_list:
        file.write(item)

    # Close output file
    file.close()
    print('Process finished')


def main(username, password):
    """
    Logs into Netflix
    """
    print('Logging into Netflix')

    # Keep track of whether login was successful
    logged_in = True

    driver.get("https://www.netflix.com/gb/login")
    mutli_page_login = False

    time.sleep(5)
    # Clearing email textbox and typing in user's email
    driver.find_element_by_name('userLoginId').clear()
    driver.find_element_by_name('userLoginId').send_keys(username)

    # Clearing password textbox
    try:
        driver.find_element_by_name('password').clear()
    except NoSuchElementException:
        # It is a double page login. So we first need to click on "Next" and then send the password
        driver.find_element_by_class_name('login-button').click()
        mutli_page_login = True

    if mutli_page_login:
        driver.find_element_by_name('password').clear()

    time.sleep(5)
    # Typing in user's password
    driver.find_element_by_name('password').send_keys(password)

    # Clicking on submit button
    driver.find_element_by_class_name('login-button').click()

    try:
        # Wait for profiles page to load
        wait = WebDriverWait(driver, 60)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'profile-icon')))
    except TimeoutException:
        # If a TimeoutException occurs, it means user credentials were incorrect
        logged_in = False

    if logged_in:
        get_active_profile()
    else:
        print('Error: Incorrect Credentials.\n' 
                + '       Please check if you entered the correct email and password in \'userconfig.ini\'')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', required=True, help='Netflix email address')
    parser.add_argument('--password', required=True, help='Netflix password')
    parser.add_argument('--user', required=True, help='Profile user name')
    parser.add_argument('--history', required=False, type=int, help='How many days worth of history do you want?')
    
    args = parser.parse_args()

    USER = args.user

    if args.history:
        DAYS_WORTH_OF_HISTORY = args.history

    main(args.username, args.password)