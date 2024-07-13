from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup as BS

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webcrawler.utils import get_driver, get_que, set_deed_que, save_valuation


def save_deeds(driver, select, waiting_delay, record_limit):
    """
    Save search result to database

    Parameters:
        driver (selenium): Selenium driver
        select (selenium): Select box currently using
        waiting_delay (int): time in sec to wait between certain functionality
        The bigger it is the longer it takes

    Returns:
        NOTHING   
    """
    
    deed_number = 0
    counter = 0
    options_length = len(select.options)
    while deed_number < options_length:
        deed_number += 1
        que = get_que()
        deed_number = que.deeds_town + 1
        select.select_by_index(deed_number)
        deeds_town = select.first_selected_option.text
        print(f"{deed_number} {deeds_town}")
        
        driver.implicitly_wait(waiting_delay)
        submit = driver.find_element(By.ID, 'btnSearch')
        submit.click()

        driver.implicitly_wait(waiting_delay)
        
        driver.switch_to.default_content()
        driver.switch_to.frame('mainFrame')
        driver.switch_to.frame('frameSearch')

        table = WebDriverWait(
            driver, waiting_delay
        ).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, ".searchResultTable"
            ))
        )

        soup = BS(
            table.get_attribute('innerHTML'), 
            'html.parser'
        )

        for row in soup.find_all('tr'):
            cols = row.find_all('td')

            if len(cols) == 8:
                valuation_roll = {
                    "rate_number"       : cols[0].text,
                    "legal_description" : cols[1].text,
                    "address"           : cols[2].text,
                    "deeds_town"        : deeds_town,
                    "first_owner"       : cols[3].text,
                    "use_code"          : cols[4].text,
                    "rating_category"   : cols[5].text,
                    "market_value"      : cols[6].text,
                    "registered_extent" : cols[7].text.split(","),
                    "roll_type"         : "deeds",
                }
                
                save_valuation(valuation_roll)

                    
        set_deed_que(deed_number)

        driver.switch_to.default_content()
        driver.switch_to.frame('mainFrame')
        driver.switch_to.frame('frmSearchCriter')

        counter += 1
        if counter == record_limit:
            break

    return ""


class Command(BaseCommand):
    """
    This command connects to A URL
    Then selects for full titles and then
    goes through the deed towns one at a time
    and saves the result.
    
    
    wait : needs a waiting period, int value
    """
    
    help = "We are going to get the full title by deeds town"

    def add_arguments(self, parser):
        # lets you set the delay you are willing to wait
        parser.add_argument("wait", nargs="+", type=int)
        
        #limit the amount of records run
        parser.add_argument("limit", nargs="+", type=int)

    def handle(self, *args, **options):

        for delay in options['wait']:
            waiting_delay = delay
            
        for limit in options['limit']:
            record_limit = limit

        try:
            
            driver = get_driver()

            search_select = Select(driver.find_element(By.ID, 'drpSearchType'))
            
            # 1 is full title
            # 2 is sectional title
            full_or_sectional = 0
            options_length = len(search_select.options)
            while full_or_sectional < options_length:

                full_or_sectional += 1

                if full_or_sectional == 1:
                    # Select by index and submit to the search 
                    search_select.select_by_index(full_or_sectional)
                    submit = driver.find_element(By.ID, 'btnGo')
                    submit.click()

                    driver.implicitly_wait(waiting_delay)
                    # select the search criteria frame
                    driver.switch_to.frame('frmSearchCriter')
                    
                    select_deeds_town = Select(driver.find_element("id", 'drpDeedsTown'))

                    save_deeds(driver, select_deeds_town, waiting_delay, record_limit)
                    
                    driver.switch_to.default_content()
                    driver.switch_to.frame('mainFrame')
       
        except Exception as error:
            self.stdout.write(
                self.style.ERROR(error)
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("Everything seems ok")
            )
        finally:
            driver.quit()
            self.stdout.write(
                self.style.SUCCESS("Closing up")
            )
