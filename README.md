# sh_sec_quiz
Programming quiz for sh_sec

IMPORTANT: Before running the script, the variable path_to_chromedriver has to be changed to point to your location of chromedriver.exe

test1_assert_minimum_length.py file contains a solution to Test 1: 
  Assert that the dynamic text (the lorem ipsum text block) on the page contains a word at least 10 characters in length.
  Stretch goal:
    Print the longest word on the page.

Page under test: https://the-internet.herokuapp.com/dynamic_content
Used Selenium driver: chromedriver (path_to_chromedriver variable needs to be changed for your location of the driver).

The answer to the test is presented as a script. For it to be useful in production test environment, it would be inherited from a general test case class and would be used with a test harness, which reads data from YAML or JSON file, and writes the log and results to another file. The assertions, if used at all, would be handled by the harness, but now it’s done in the script together with an imitation of logging, which should be properly done using Python’s logging module.
