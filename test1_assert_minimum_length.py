#***SETUP

import sys

# initialize selenium driver
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# these data should come from the data file and be loaded by test harness
path_to_chromedriver = 'C:\\Users\\Leon\\AppData\\Local\\Programs\\Python' + \
    '\\Python35\\Lib\\site-packages\\selenium\\chromedriver\\chromedriver.exe'
page_to_test = 'https://the-internet.herokuapp.com/dynamic_content'
timeout = 10 # seconds for implicit wait 
row_count_expected = 3 # based on previous knowledge about the page layout
xpath_start = "//div[@class='row']" # used to build a row-specific xpath
xpath_end = "/div[@class='large-10 columns']" # to build a row-specific xpath
length_req = 10 # the minimum word length required for the test to pass
find_longest = True # makes the test search for the longest word(s) or not

# print (path_to_chromedriver)
driver = webdriver.Chrome(path_to_chromedriver)
driver.implicitly_wait(timeout) # seconds

#get the page to test
driver.get(page_to_test)

#***TEST

# find how many rows of text there are on the page
row_count_actual = len(driver.find_elements_by_xpath
                           ("//div[@class='large-10 columns']"))

# Warn if the actual number of text rows is different from expected
if row_count_actual != row_count_expected:
  print ("[warning] Expected and actual row counts are different." + \
         " Actual row count is %d." %row_count_actual)

# Initialize variables needed for asserting the minimum required word length
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
        
        # check that text row is actually displayed (not requested in the quiz)
        if row_text.is_displayed():
          print ("[log] Text in row %d is displayed." %i)
        else:
          print ("[warning] Text in row %d is NOT displayed." %i)

        print("[log] The text in row %d is:\n%s" %(i, row_text.text))

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

    except NoSuchElementException as e:
        print(e)
        driver.quit()

print ("\nRESULTS")
# report results of searching for the longest word(s)
if find_longest:
  #Print the longest word(s) on the page and their length.
  print ("The longest (%d characters) word(s) on the page:" %len_max)
  print (longest_words)

#report results of finding a word of required length
if length_req_satisfied:
  print_text = "Minimum required length of %d char is found first time " + \
               "at the word '%s' in text row %d."
  print(print_text %(length_req, word_req_met, i_req_met))
else:
  # Assert that the dynamic text on the page contains a word of at least
  # required_length in length (the test harness would be the propper place
  # to handle the exception).
  try:
      assert(length_req_satisfied)
  except AssertionError:
      print("Minimum length of %d char is NOT found." %length_req)


#***CLEANUP (test harness would make cleanup happen even when a test bombs out)

#close the selenium driver
driver.quit()