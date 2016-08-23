"""
This is a solution to Test 2: 
    Assert that the "Punisher" image (silhouette with a skull on his chest)
    does not appear on the page.
    Stretch goal:
        Give names to each avatar that can appear on the page and print out
        each avatars name.

Page under test: https://the-internet.herokuapp.com/dynamic_content
Used Selenium driver: chromedriver (path_to_chromedriver variable needs
to be changed for your location of the driver)

Images of avatars (often called 'avatars' for brevity sake in the comments)
are identified using their URL and size.
"""

#***Setting up Selenium driver and opens the page to test
def setup(path_to_chromedriver, timeout, page_to_test):

    # create an instance of chromedriver
    driver = webdriver.Chrome(path_to_chromedriver)
    # set implicit wait to 'timeout' seconds
    driver.implicitly_wait(timeout)
    # open the page to test
    driver.get(page_to_test)

    return driver

#***TEST
def test(driver, row_count_expected, xpath_avatars, punisher, \
         known_avatars, assign_names):

    page_avatars = [] # container for name/url/size of the page's avatars
    punisher_not_here = True # keeps info about Punisher's presence on the page
    
    # Find all avatars on the page
    avatars = driver.find_elements_by_xpath(xpath_avatars)
    row_count_actual = len(avatars) # assumes that there is one avatar per row

    # Warn if the actual number of rows with avatars is different from expected
    if row_count_actual != row_count_expected:
      logging.warning("Expected and actual row counts are different." + \
             " Actual row count is %d. Check xpath." %row_count_actual)

    #Process all rows with avatars on the page
    for n,av in enumerate(avatars, start = 1):

        url = av.get_attribute('src')
        logging.info("Avatar(row %d) URL is: %s" %(n,url))

        # Download the file from 'url' and save it locally under 'f_name'
        f_name = 'row' + str(n) + 'av.jpg'
        logging.info("Avatar(row %d) image downloaded as %s file" %(n,f_name))
        with urllib.request.urlopen(url) as resp, open(f_name, 'wb') as out_f:
            shutil.copyfileobj(resp, out_f)
        size = os.path.getsize(f_name)
        logging.info("Avatar(row %d) file size is %d bytes" %(n,size))
     
        # If requested to assign names to avatars,
        # do the assignment for those avatars, whose image's size and url
        # cannot be matched with the known ones.
        if assign_names:
            # match avatar's url/size with those of known avatars
            url_m = False
            size_m = False
            for known_av in known_avatars:
                if known_av['url'] == url:
                    url_m = True
                if known_av['size'] == size:
                    size_m = True
                if url_m or size_m:
                    break
                
            # If there is a match, check for Punisher.
            # Else give the avatar a name and add it to known avatars.
            # Add the avatar to the page's avatars
            if url_m and size_m:
                #check for Punisher
                if size == punisher['size']:
                    punisher_not_here = False
                    punisher_row = n
                page_avatars.append(known_av)
            else:
                # Make avatar's name 'Avatar-[num]' by splicing its url
                name = url[-12:-4]
                new_av = {
                    'name': name,
                    'url' : url,
                    'size' : size
                }
                known_avatars.append(new_av)
                page_avatars.append(new_av)
                if url_m or size_m:
                    logging.warning('Only size or URL matches a known ' + \
                                    'avatar in row %d' %n)

                logging.info(known_avatars)
        # If assigning names to avatars is not requested,
        # just check for Punisher
        else:
            if size == punisher['size'] and url == punisher['url']:
                punisher_not_here = False
                punisher_row = n
                break

    # Reporting results
    print ('\nRESULTS\n====================')
    if assign_names:
        # print out names of each avatar found on the page
        print("%d avatars found on the page:" %len(page_avatars))
        for av in page_avatars:
            print(av['name'])
        # Dump known_avatars as JSON file into working directory
        f = open("known_avatars.json", "w")
        json.dump(known_avatars, f)
        f.close()
    # Assert that Punisher image is not on the page
    assert punisher_not_here, "Punisher was last found in row %d." \
        %punisher_row

    if punisher_not_here:
        print("Punisher was NOT found on the page.")

    return 1

#***Cleaning up by closing Selenium driver.
def cleanup(driver):
    #close the Selenium driver
    driver.quit()
    
    return 1

if __name__ == '__main__':
    import json, logging, os, shutil, sys, urllib

    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.INFO)

    # initialize selenium driver
    from selenium import webdriver
    from selenium.common.exceptions import NoSuchElementException

    # test parameters
    path_to_chromedriver = 'C:\\Users\\Leon\\AppData\\Local\\Programs' + \
        '\\Python\\Python35\\Lib\\site-packages\\selenium\\chromedriver' + \
        '\\chromedriver.exe'
    timeout = 10 # seconds for implicit wait 
    page_to_test = 'https://the-internet.herokuapp.com/dynamic_content'
    row_count_expected = 3 # based on previous knowledge about the page layout
    xpath_avatars = "//div[@class='large-2 columns']/img" # avatars' xpath
    name_p = 'Punisher' # name of the avatar, which shouldn't be on the page
    url_p = 'https://the-internet.herokuapp.com/img/avatars/Original-' + \
           'Facebook-Geek-Profile-Avatar-3.jpg' # URL of Punisher's image
    size_p = 12817      # size of Punisher's image
    punisher = {        # dictionary containing Punisher's attributes
        'name': name_p,
        'url' : url_p,
        'size' : size_p
    }
    # known_avatars is a list of dictionaries with attributes of known avatars
    if os.path.exists("known_avatars.json"):
       known_avatars = json.load(open("known_avatars.json"))
    else:
        known_avatars  = [punisher]
    assign_names = True # when True, avatars named and
                         # those on the page are printed

    # perform the setup
    driver = setup(path_to_chromedriver, timeout, page_to_test)
    
    try:
        # run the test
        test(driver, row_count_expected, xpath_avatars, punisher, \
            known_avatars, assign_names)
    except AssertionError as e:
        print(e)
    finally:
        # perform cleanup
        cleanup(driver)