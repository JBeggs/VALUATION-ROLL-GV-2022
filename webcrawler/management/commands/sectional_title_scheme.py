from django.core.management.base import BaseCommand


from bs4 import BeautifulSoup as BS

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webcrawler.utils import get_driver, get_que, set_scheme_que, save_valuation


def save_scheme(driver, select, waiting_delay, record_limit):
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
    
    scheme_number = 0
    counter = 0
    options_length = len(select.options)
    while scheme_number < options_length:
        
        que = get_que()
        scheme_number = que.scheme + 1

        select.select_by_index(scheme_number)
        scheme = select.first_selected_option.text
        print(f"{scheme_number} {scheme}")
        
        driver.implicitly_wait(waiting_delay)
        submit = driver.find_element(By.ID, 'btnSearch')
        submit.click()
        
        driver.implicitly_wait(waiting_delay)
        
        driver.switch_to.default_content()
        driver.switch_to.frame('mainFrame')
        driver.switch_to.frame('frameSearch')

        try:
            
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
                        "rate_number"        : cols[0].text.strip(),
                        "legal_descriptionn" : cols[1].text.strip(),
                        "address"            : cols[2].text.strip(),
                        "scheme"             : scheme,
                        "first_owner"        : cols[3].text.strip(),
                        "use_code"           : cols[4].text.strip(),
                        "rating_category"    : cols[5].text.strip(),
                        "market_value"       : cols[6].text.strip(),
                        "registered_extent"  : cols[7].text.split(","),
                        "roll_type"         : "scheme",
                    }
                    
                    save_valuation(valuation_roll)
            
        except:
            pass

        set_scheme_que(scheme_number)

        driver.switch_to.default_content()
        driver.switch_to.frame('mainFrame')
        driver.switch_to.frame('frmSearchCriter')

        counter += 1
        if counter == record_limit:
            break    


class Command(BaseCommand):
    """
    This command connects to a URL
    Then selects for full titles and then
    goes through the deed towns one at a time
    and saves the result.
    
    
    wait : needs a waiting period, int value
    """
    
    help = "We are going to get the full title by scheme"

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

            search_options = len(search_select.options)
            while full_or_sectional < search_options:

                full_or_sectional += 2

                if full_or_sectional == 2:

                    search_select.select_by_index(full_or_sectional)

                    submit = driver.find_element(By.ID, 'btnGo')
                    submit.click()
            
                    driver.implicitly_wait(waiting_delay)
                    driver.switch_to.frame('frmSearchCriter')
                    
                    select_scheme = Select(driver.find_element("id", 'drpScheme'))
                    save_scheme(driver, select_scheme, waiting_delay, record_limit)
                    
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
