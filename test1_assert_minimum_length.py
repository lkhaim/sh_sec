"""
This is a solution to Test 1: 
    Assert that the dynamic text (the lorem ipsum text block) on the page
    contains a word at least 10 characters in length.
    Stretch goal:
        Print the longest word on the page.

Page under test: https://the-internet.herokuapp.com/dynamic_content
Used Selenium driver: chromedriver (path_to_chromedriver variable needs
to be changed for your location of the driver)
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

#***Testing if the word of length 'length_req' is present on the page.
#***Finds the longest word or words if find_longest = True.
#***Reports results if 'length_req' is found and asserts otherwise.
def test(driver, row_count_expected, xpath_start, xpath_end,
         length_req, find_longest):

    # find how many rows of text there are on the page
    row_count_actual = len(driver.find_elements_by_xpath
                               ("//div[@class='large-10 columns']"))

    # Warn if the actual number of text rows is different from expected
    if row_count_actual != row_count_expected:
      logging.warning("Expected and actual row counts are different." + \
             " Actual row count is %d. Check xpath." %row_count_actual)

    # Initialize variables used for asserting the minimum required word length
    # and searching for the longest word(s)
    length_req_satisfied = False # will be set to True when a word with length
                                 # of at least required_length is found
    len_max = 0 # will keep the length of the longest word found
    if find_longest:
      longest_words = [] # will keep a list of longest words

    #Process all text rows on the page
    for i in range (1, row_count_actual+1):
        # build xpath to i's text row
        text_xpath = xpath_start + "[" + str(i) + "]" + xpath_end
        #catch exception if text_xpath doesn't exist
        try:
            row_text = driver.find_element_by_xpath(text_xpath)
        except NoSuchElementException as e:
            print("NoSuchElementException when using xpath.\n%s" %e)
            driver.quit()
            sys.exit(1)

        # check that text row is actually displayed
        if row_text.is_displayed():
          logging.info("Text in row %d is displayed." %i)
        else:
          logging.warning("Text in row %d is NOT displayed." %i)

        logging.info("The text in row %d is:\n%s" %(i, row_text.text))

        # Split text row into words and start processing each word's length
        words = row_text.text.split()
        for word in words:
            word_len = len(word)
            # if word's length is below the required length, but we need
            # to find the longest word(s), search for the longest word
            if word_len < length_req and find_longest:
              if word_len > len_max:
                len_max = word_len
                longest_words = [ word ]
              elif word_len == len_max:
                longest_words.append( word )
            # if word's length is above the required length, keep searching
            # for the longest word(s) if requested. If searching
            # for the longest word(s) is NOT requested, stop processing
            # words in the row
            if word_len >= length_req:
              # remebering where the required word length was found
              # for the first time
              if (not length_req_satisfied):
                length_req_satisfied = True
                i_req_met = i
                word_req_met = word
              if find_longest:
                if word_len > len_max:
                  len_max = word_len
                  longest_words = [ word ]
                elif word_len == len_max:
                  longest_words.append( word )
              else:
                len_max = word_len  
                break
        # if length requirement is met, continue to the next row,
        # if searching for the longest word(s) is requested. Otherwise,
        # stop processing the rows.
        if length_req_satisfied:
          if find_longest:
            continue
          else:
            break

    print ('\nRESULTS\n====================')
    # report results of searching for the longest word(s)
    if find_longest:
      #Print the longest word(s) on the page and their length.
      print ("The longest (%d characters) word(s) on the page:" %len_max)
      print (longest_words)

    #report results of finding a word of required length
    if length_req_satisfied:
      print_text = "Minimum length req of %d char was met first time " + \
                   "at the word '%s' in text row %d."
      print(print_text %(length_req, word_req_met, i_req_met))
    else:
      # Assert that the dynamic text on the page contains a word of at least
      # required_length in length.
      assert length_req_satisfied, "Minimum length of %d char is NOT found." \
          %length_req

    return 1

#***Cleaning up by closing Selenium driver.
def cleanup(driver):
    #close the Selenium driver
    driver.quit()
    
    return 1

if __name__ == '__main__':
    import sys, logging

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

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
    xpath_start = "//div[@class='row']" # used to build a row-specific xpath
    xpath_end = "/div[@class='large-10 columns']" # to finish building xpath
    length_req = 10 # the minimum word length required for the test to pass
    find_longest = True # makes the test search for the longest word(s) or not
    
    # perform the setup
    driver = setup(path_to_chromedriver, timeout, page_to_test)
    
    try:
        # run the test
        test(driver, row_count_expected, xpath_start, xpath_end, length_req, \
            find_longest)
    except AssertionError as e:
        print(e)
    finally:
        # perform cleanup
        cleanup(driver)