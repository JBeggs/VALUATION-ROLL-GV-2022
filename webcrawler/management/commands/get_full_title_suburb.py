from django.core.management.base import BaseCommand

from bs4 import BeautifulSoup as BS

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webcrawler.utils import get_driver, get_que, set_suburb_que, save_valuation



def save_suburbs(driver, select, waiting_delay, record_limit):
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
    suburb_number = 0
    counter = 0
    options_length = len(select.options)
    while suburb_number < options_length:

        que = get_que()
        suburb_number = que.suburb + 1
        
        select.select_by_index(suburb_number)
        suburb = select.first_selected_option.text
        print(f"{suburb_number} {suburb}")

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

        soup = BS(table.get_attribute('innerHTML'), 'html.parser')

        for row in soup.find_all('tr'):
            cols = row.find_all('td')

            if len(cols) == 8:
                valuation_roll = {
                    "rate_number"       : cols[0].text.strip(),
                    "legal_description" : cols[1].text.strip(),
                    "address"           : cols[2].text.strip(),
                    "suburb"            : suburb,
                    "first_owner"       : cols[3].text.strip(),
                    "use_code"          : cols[4].text.strip(),
                    "rating_category"   : cols[5].text.strip(),
                    "market_value"      : cols[6].text.strip(),
                    "registered_extent" : cols[7].text.split(","),
                    "roll_type"         : "suburb",
                }
                
                save_valuation(valuation_roll)

        set_suburb_que(suburb_number)
        
        driver.switch_to.default_content()
        driver.switch_to.frame('mainFrame')
        driver.switch_to.frame('frmSearchCriter')
        counter += 1
        if counter == record_limit:
            break

    return ''


class Command(BaseCommand):
    """
    This command connects to the URL above
    Then selects for full titles and then
    goes through the suburbs one at a time
    and saves the result.
    
    
    wait : needs a waiting period, int value
    """
    
    help = "We are going to get the full title by suburbs"

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
            
            # end when full_or_fucntional is bigger than the options
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
                    # find the suburb dropdown
                    select_suburb = Select(driver.find_element("id", 'drpSuburb'))
                    
                    #run the search and save results for suburb
                    save_suburbs(driver, select_suburb, waiting_delay, record_limit)
                    
                    #switch to main frame and repeat
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
