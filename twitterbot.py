from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
'''Uncomment the below line when running in linux'''
from pyvirtualdisplay import Display
import time
import os
import logging
# import re
from cleantext import clean

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class Twitterbot:

    def __init__(self, email, password):
        """Constructor

        Arguments:
            email {string} -- registered twitter email 
            password {string} -- password for the twitter account
        """

        self.email = email
        self.password = password
        # initializing chrome options
        chrome_options = Options()

        # adding the path to the chrome driver and
        # integrating chrome_options with the bot
        self.bot = webdriver.Chrome(
            executable_path=os.path.join(os.getcwd(), 'chromedriver'),
            options=chrome_options
        )

    def paste_content(self, el, content):
        self.bot.execute_script(
            f'''
        const text = `{content}`;
        const dataTransfer = new DataTransfer();
        dataTransfer.setData('text', text);
        const event = new ClipboardEvent('paste', {{
          clipboardData: dataTransfer,
          bubbles: true
        }});
        arguments[0].dispatchEvent(event)
        ''',
            el)

    def login(self):
        """
            Method for signing in the user
            with the provided email and password.
        """

        bot = self.bot
        # fetches the login page
        bot.get('https://twitter.com/i/flow/login')
        # adjust the sleep time according to your internet speed
        time.sleep(10)

        try:
            email = bot.find_element_by_xpath(
                '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input'
            )
        except:
            time.sleep(5)
            email = bot.find_element_by_xpath(
                '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input'
            )

        print("email: ", email)

        while email is None:
            time.sleep(1)
            email = bot.find_element_by_xpath(
                '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input'
            )
            print("email: ", email)

        # sends the email to the email input
        email.send_keys(self.email)

        # get "next" button
        # executes RETURN key action
        email.send_keys(Keys.RETURN)

        time.sleep(1)
        password = bot.find_element_by_xpath(
            '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'
        )
        print("password: ", password)
        while password is None:
            time.sleep(1)
            password = bot.find_element_by_xpath(
                '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'
            )
            print("password: ", password)

        # sends the password to the password input
        password.send_keys(self.password)
        # executes RETURN key action
        password.send_keys(Keys.RETURN)

        time.sleep(1)

    def post_single_tweet(self, text):
        JS_ADD_TEXT_TO_INPUT = """
        var elm = arguments[0], txt = arguments[1];
        elm.value += txt;
        elm.dispatchEvent(new Event('change'));
        """
        logger.info("post single tweet:")
        logger.info("text: %s", text)
        bot = self.bot
        textArea = bot.find_element_by_xpath(
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div'
        )
        # print("text: ", text)
        logger.info("clicking text area")
        textArea.click()
        time.sleep(1)
        # sends the text to the text area
        textarea = bot.find_element_by_xpath(
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div[2]/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div'
        )
        text = text + " "
        self.paste_content(textarea, text)
        logger.info("textarea: ", textarea)
        logger.info("putting text")
        # bot.execute_script(JS_ADD_TEXT_TO_INPUT, textarea, text)

        time.sleep(1)

        # clicks the tweet button
        postButton = bot.find_element_by_xpath(
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[3]'
        )
        # print("post button: ", postButton)
        postButton.click()

        time.sleep(1)

    def post_thread(self, thread):
        logger.info("post thread:")

        # click on post button

        bot = self.bot
        text = thread[0]
        text_number = 0
        thread = thread[1:]
        # put the first tweet
        bot = self.bot

        postButton = bot.find_element_by_xpath(
            '//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a')
        postButton.click()
        time.sleep(1)

        textArea = bot.switch_to.active_element
        text = text + "+"
        self.paste_content(textArea, text)
        # text = text + "+"

        # bot.execute_script(JS_ADD_TEXT_TO_INPUT, textArea, text)

        time.sleep(1)
        # sends the text to the text area
        # clicks the thread button
        try:
            threadButton = bot.find_element_by_css_selector(
                '[aria-label="Add post"]')
        except:
            threadButton = bot.find_element_by_css_selector(
                '[aria-label="Adicionar post"]')
        # print("thread button", threadButton)

        # print("thread button", threadButton)
        threadButton.click()
        time.sleep(1)
        for text in thread:
            logger.info("text-%s: %s", text_number, text)
            text_number += 1
            # get the text area
            bot.switch_to.active_element.click()
            time.sleep(1)
            # sends the text to the text area
            if text != thread[-1]:
                text = text + "+"
                textArea = bot.switch_to.active_element
                self.paste_content(textArea, text)
                # bot.execute_script(JS_ADD_TEXT_TO_INPUT, textArea, text)
                # clicks the thread button
                time.sleep(1)
                try:
                    threadButton = bot.find_element_by_css_selector(
                        '[aria-label="Add post"]')
                except:
                    threadButton = bot.find_element_by_css_selector(
                        '[aria-label="Adicionar post"]')
                # print("thread button", threadButton)

                threadButton.click()
                time.sleep(1)
            else:
                textArea = bot.switch_to.active_element
                text = text + " "
                self.paste_content(textArea, text)
                # bot.execute_script(JS_ADD_TEXT_TO_INPUT, textArea, text)
                time.sleep(1)

        # clicks the tweet button
        postButton = bot.find_element_by_css_selector(
            '[data-testid="tweetButton"]')

        print("post button: ", postButton)
        postButton.click()
        time.sleep(1)

    def post_tweet(self, text):
        """
        This function automatically posts the
        tweet to the twitter account

        Arguments:
            text {string} -- text to be tweeted
        """
        logger.info("text: %s", text)

        bot = self.bot

        # fetches the twitter homepage
        # bot.get('https://twitter.com/')
        # time.sleep(1)
        # remove emoji
        # text = clean(text, no_emoji=True)

        # clicks the text area
        thread = [text[start:start+260] for start in range(0, len(text), 260)]
        logger.info("thread: %s", thread)
        time.sleep(1)
        if len(thread) > 1:
            self.post_thread(thread)
        else:
            self.post_single_tweet(text)

    def like_retweet(self, hashtag):
        """
        This function automatically retrieves
        the tweets and then likes and retweets them

        Arguments:
            hashtag {string} -- twitter hashtag
        """

        bot = self.bot

        # fetches the latest tweets with the provided hashtag
        bot.get(
            'https://twitter.com/search?q=%23' +
            hashtag+'&src=typed_query&f=live'
        )

        time.sleep(1)

        # using set so that only unique links
        # are present and to avoid unnecessary repetition
        links = set()

        # obtaining the links of the tweets
        for _ in range(100):
            # executing javascript code
            # to scroll the webpage
            bot.execute_script(
                'window.scrollTo(0, document.body.scrollHeight)'
            )

            time.sleep(4)

            # using list comprehension
            # for adding all the tweets link to the set
            # this particular piece of code might
            # look very complicated but the only reason
            # I opted for list comprehension because is
            # lot faster than traditional loops
            [
                links.add(elem.get_attribute('href'))
                for elem in bot.find_elements_by_xpath("//a[@dir ='auto']")
            ]

        # traversing through the generated links
        for link in links:
            # opens individual links
            bot.get(link)
            time.sleep(4)

            try:
                # retweet button selector
                bot.find_element_by_css_selector(
                    '.css-18t94o4[data-testid ="retweet"]'
                ).click()
                # initializes action chain
                actions = ActionChains(bot)
                # sends RETURN key to retweet without comment
                actions.send_keys(Keys.RETURN).perform()

                # like button selector
                bot.find_element_by_css_selector(
                    '.css-18t94o4[data-testid ="like"]'
                ).click()
                # adding higher sleep time to avoid
                # getting detected as bot by twitter
                time.sleep(10)
            except:
                time.sleep(1)

        # fetches the main homepage
        bot.get('https://twitter.com/')
