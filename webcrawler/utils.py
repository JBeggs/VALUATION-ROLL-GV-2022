from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.remote_connection import RemoteConnection
from webcrawler.models import RollQue, ValuationRoll

# URL of the website to scrape
# URL = "https://valuation2022.durban.gov.za/"
URL = "https://valuation2017.durban.gov.za/"

def get_driver():
    """
    Gets and return the selenium driver needed
    
    return driver
    """
    
    #driver = webdriver.Chrome()
    
    options = Options()
    driver = webdriver.Remote(options=options, command_executor=RemoteConnection("http://chrome:4444/wd/hub"))
    
    driver.get(URL)
    driver.maximize_window()
    driver.switch_to.frame('mainFrame')
    return driver


def get_que():
    """
    Process and get the que for the scraping
    
    return que object
    """
    que = RollQue.objects.all().first()
    if not que:
        que = RollQue.objects.create(
            deeds_town = 0,
            suburb = 0,
            scheme = 0
        )

        que.save()
    
    return que


def set_scheme_que(number):
    """
    Setup scheme que
    params: number it the number being saved
    returns: Nothing
    """
    que = RollQue.objects.all().first()
    que.scheme = number
    que.save()
    

def set_suburb_que(number):
    """
    Setup suburb que
    params: number it the number being saved
    returns: Nothing
    """
    que = RollQue.objects.all().first()
    que.suburb = number
    que.save()
    

def set_deed_que(number):
    """
    Setup deed town que
    params: number it the number being saved
    returns: Nothing
    """
    que = RollQue.objects.all().first()
    que.deeds_town = number
    que.save()


def save_valuation(valuation_roll):
    """
    Save the data to the database
    
    params: valuation_roll is a dictiionery object with the relevant fields
    returns: Nothing
    """
    check = ValuationRoll.objects.filter(rate_number=valuation_roll['rate_number'])
    if not check:
        data = ValuationRoll(**valuation_roll)
        data.save()
    else:
        check.update(**valuation_roll)
