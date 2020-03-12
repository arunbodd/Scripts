#Import all libraries required for the Script

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()

#One can change the tissue type by manually entering the tissue name below, eg. Adult-Brain, Bone-Marrow, Retina etc.
driver.get('http://bis.zju.edu.cn/MCA/gallery.html?tissue=Adult-Brain')

#Open an output file
dataFile = open("AdultBrian_MouseCellAtlas.txt", "w")

try:
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sorting_1"))
    )
finally:
    
    #Set xpath to marker table length, i.e, setting number of entries
    xpath = '//*[@id=\"marker_table_length\"]/label/select/option[4]'
    driver.execute_script("document.evaluate(arguments[0], document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.value = arguments[1];", xpath, "10000")

    #Search for Marker table length in the body of the webpage and set the value to highest
    select = Select(driver.find_element_by_name('marker_table_length'))
    select.select_by_value('10000') # select by value 

    #Wait for 10 seconds before loading all values
    WebDriverWait( driver, 10 ) # seconds

    #Use HTML parser to parse through the page
    soup = BeautifulSoup(driver.page_source, 'html.parser')


    ##Script starts writing an output of whatever it finds in the body of the html page
    #Write the header ouput to a file
    dataFile.write("### columns from Head ###")
    dataFile.write("\n")
    data = soup.find('thead').findAll('th')
    header = ""
    for tag in data :
        header = header + "     " + tag.text

    dataFile.write(header)

    dataFile.write("\n")
    dataFile.write("\n")

    #Append the body output to the file
    dataFile.write("### data from body ###")
    dataFile.write("\n")

    ## for the first time
    tbody = soup.find('tbody').findAll('tr')
    
    ##loop over the tbody and write each row as text
    for tr in tbody :
        row = ""
        td = tr.findAll('td')
        dataFile.write("\n")
        for each in td :
            row = row + "     " + each.text 
        
        #Write the output
        dataFile.write(row)
    
    #exit the driver and datafile
    driver.close()
    dataFile.close()
