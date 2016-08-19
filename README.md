# sh_sec_quiz
Programming quiz for sh_sec

test1_assert_minimum_length.py file contains a solution to Test 1:<br>
  Assert that the dynamic text (the lorem ipsum text block) on the page contains a word at least 10 characters in length.<br>
  Stretch goal:<br>
    Print the longest word on the page.

Page under test: https://the-internet.herokuapp.com/dynamic_content<br>
Used Selenium driver: chromedriver

IMPORTANT: Before running the script, the variable path_to_chromedriver has to be changed to point to your location of chromedriver.exe

To turn the printing of the longest word on the page on and off, edit the find_longest variable, which is currntly set to 'True'

DISCLAIMER: The answer to the test is presented as a script. For it to be useful in production test environment, it would be inherited from a general test case class and would be used with a test harness, which reads data from YAML or JSON file, and writes the log and results to another file. The assertions, if used at all, would be handled by the harness, but now it’s done in the script together with an imitation of logging, which should be properly done using Python’s logging module.

EXAMPLES OF TEST OUTPUT:

Output examples for 4 combinations of length_req and find_longest:

====================
length_req = 10,
find_longest = True

[log] Text in row 1 is displayed.<br>
[log] The text in row 1 is:<br>
Eos rerum cupiditate eum et nostrum est sed nam ut voluptatem sed delectus modi aspernatur quaerat ipsum animi libero alias velit velit quo sequi ducimus non hic numquam sit quod optio ut iure.<br>
[log] Text in row 2 is displayed.<br>
[log] The text in row 2 is:<br>
Quo dolores qui voluptatem voluptatem sequi omnis laborum unde maiores sit et autem doloremque optio qui repellat fuga mollitia omnis et id rerum porro blanditiis eum est voluptas eum officia tenetur veritatis voluptas vel et.<br>
[log] Text in row 3 is displayed.<br>
[log] The text in row 3 is:<br>
Maiores esse sed voluptas deserunt vero amet dolores occaecati aut eum incidunt repellat voluptatem ex labore est sit voluptas sunt facilis rerum ut et quisquam qui et quos aperiam vel aut.

RESULTS<br>
The longest (10 characters) word(s) on the page:<br>
['cupiditate', 'voluptatem', 'aspernatur', 'voluptatem', 'voluptatem', 'doloremque', 'blanditiis', 'voluptatem']<br>
Minimum required length of 10 char is found first time at the word 'cupiditate' in text row 1.

====================
length_req = 100,
find_longest = True

[log] Text in row 1 is displayed.<br>
[log] The text in row 1 is:<br>
Et consequatur tempora velit qui et beatae ratione numquam odio sed quisquam et sed consequuntur quos omnis totam est magni laudantium ducimus et exercitationem natus vel dolores nulla cum similique libero veniam provident nihil officia.<br>
[log] Text in row 2 is displayed.<br>
[log] The text in row 2 is:<br>
Aliquid numquam debitis explicabo id possimus beatae voluptates consequatur sunt blanditiis a quia animi aperiam ut magnam sed non eum accusantium culpa et velit eum perspiciatis rerum ducimus quasi deserunt enim sint porro suscipit.<br>
[log] Text in row 3 is displayed.<br>
[log] The text in row 3 is:<br>
Ut itaque iusto est eligendi autem nihil culpa officia atque id quam velit quia occaecati ea excepturi ipsum minus rerum porro harum ipsam nesciunt maxime voluptatibus accusantium asperiores inventore placeat.

RESULTS<br>
The longest (14 characters) word(s) on the page:<br>
['exercitationem']<br>
Minimum length of 100 char is NOT found.

====================
length_req = 100,
find_longest = False

[log] Text in row 1 is displayed.<br>
[log] The text in row 1 is:<br>
Numquam doloremque vero dolores voluptas quibusdam id quis voluptatum sed repellendus expedita ducimus culpa quis fugiat omnis voluptatem pariatur omnis dolorum et perferendis quia cupiditate laboriosam magni commodi perspiciatis voluptas magnam ad eligendi dicta non.<br>
[log] Text in row 2 is displayed.<br>
[log] The text in row 2 is:<br>
Ea fugiat unde iste occaecati quisquam qui nam illo eveniet nobis adipisci officia inventore a sed quia vel et deserunt doloremque molestiae voluptas repudiandae in reiciendis itaque aut voluptatem sit.<br>
[log] Text in row 3 is displayed.<br>
[log] The text in row 3 is:<br>
Vitae porro ab in consequuntur qui ipsum ut ad quasi veniam nesciunt velit inventore facere qui corporis alias laborum deleniti magnam dicta et autem veritatis officia expedita molestias ut animi vel qui est quas quia.

RESULTS<br>
Minimum length of 100 char is NOT found.

====================
length_req = 10,
find_longest = False

[log] Text in row 1 is displayed.<br>
[log] The text in row 1 is:<br>
Quis iste blanditiis dolore ipsum suscipit officia mollitia facere sunt est sed quia ea a error itaque quia exercitationem nostrum quaerat iure eos in voluptatem minus accusantium veniam et et et illo necessitatibus sit cum.

RESULTS<br>
Minimum required length of 10 char is found first time at the word 'blanditiis' in text row 1.
