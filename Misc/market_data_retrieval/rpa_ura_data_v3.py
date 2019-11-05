# Note: Need TagUI Python to be installed
import tagui as t
import re
from pathlib import Path
import shutil
import logging
import datetime

Path.ls = lambda x: list(x.iterdir())

PROCEED = True
START_DATE = 'OCT 2016'
END_DATE = 'SEP 2019'
SELECTION_LIMIT = 5

url = 'https://www.ura.gov.sg/realEstateIIWeb/transaction/search.action'
project_total = 0
project_count = 0
batch_count = 0
basepath = Path('.')
rawpath = basepath/'raw'
rawpath.mkdir(exist_ok=True)
logpath = basepath/'log'
logpath.mkdir(exist_ok=True)

log_name = datetime.datetime.now().strftime('resume_%H_%M_%d_%m_%Y.log')
logging.basicConfig(filename=logpath/log_name, 
                    level=logging.INFO)

# start chrome
t.init()

while PROCEED == True:
    
    batch_count += 1
    t.url(url)
    print(f'\n-----start batch {batch_count}-----\n')

    # start date
    t.select('//select[@id="searchForm_selectedFromPeriodProjectName"]', START_DATE)

    # end date
    t.select('//select[@id="searchForm_selectedToPeriodProjectName"]',END_DATE)

    # type of sale
    t.click('//label[@for="checkbox1"]')
    t.click('//label[@for="checkbox2"]')
    t.click('//label[@for="checkbox3"]')

    project_total = t.count('//div[@id="projectContainerBox"]/a')

    # select projects
    for _ in range(SELECTION_LIMIT):
        if project_count > project_total-1:
            PROCEED = False
            break
        
        selected = t.read(f'//*[@id="addToProject_{project_count}"]')
        print(f'select {selected}')
        t.click(f'//*[@id="addToProject_{project_count}"]')
        
        logging.info(f'batch: {batch_count}, project: {selected}, id: {project_count}')
        
        project_count += 1
    
    
    # search
    t.click('//input[@class="btn btn-primary btn-lg"]')
    t.wait(2) # wait for page load complete
    
    t.click('//input[@value="Download into CSV"]')
    t.wait(2) # wait for download complete
    print('File downloaded')
    
    #print(f'directory list before:\n {basepath.ls()}\n')
    
    csvfiles = basepath.glob('*.csv')
    for csvfile in csvfiles:
        print(f'processing file: {csvfile}')
        from_file = basepath/csvfile
        to_file = rawpath/f'batch_{batch_count}.csv'
        shutil.move(from_file, to_file)
        print('file renamed and moved to raw folder')
    
    #print(f'directory list after:\n {basepath.ls()}\n')
    
    print(f'Project progress: {project_count} of {project_total}')
    print(f'batch {batch_count} of {project_total//SELECTION_LIMIT} done')

