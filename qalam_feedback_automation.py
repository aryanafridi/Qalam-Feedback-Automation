from browser.handler import *
import random
import traceback
import os
import configparser

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class QalamFeedbackAutomation(BrowserHandler):
    def __init__(self) -> None:
        """Automating the Qalam Feedbac submission."""
        self.configurations = configparser.ConfigParser()
        self.configurations.read("config.ini")
        print("Configurations Loaded.")
        profile = self.configurations.get("BROWSER", "PROFILE") 
        if self.configurations.getboolean("BROWSER", "TEMPORARY"):
            profile = None
        super().__init__(temp_profile=profile)
        print("Starting Chrome!")
        self.start_chrome(headless=False)
        self.driver.get("https://qalam.nust.edu.pk/student/qa/feedback")
        
        
    
    def login(self) -> None:
        """Login to Qalam."""
        print("Logging in to Qalam!")
        qalam_id_input = self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input#login")))
        qalam_id_input.send_keys(self.configurations.get("QALAM USER", "QALAM_ID"))
        password_input = self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input#password")))
        password_input.send_keys(self.configurations.get("QALAM USER", "PASSWORD"))
        submit = self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[type=submit]")))
        submit.click()
        self.wait.until(ec.url_contains("student/qa/feedback"))
        print("Logged in successfully.")
    
    def is_logged_in(self) -> bool:
        """Check if Qalam ID is already logged in."""
        if self.driver.current_url.__contains__("web/login"):
            return False
        print("Already logged in.")
        return True
    
    def get_feedback_links(self) -> list:
        """Getting feedback links"""
        print("Getting feedback links!")
        links = []
        feedback_card_list = self.wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, "#hierarchical-show > div > ul")))
        for feedback_card in feedback_card_list:
            if feedback_card.get_property("innerText").__contains__("Completed"):
                continue
            links.append(feedback_card.find_element(By.TAG_NAME, "a").get_attribute('href'))

        print(f"Got {len(links)} feedback for submission.")
        return links

    def feedbacks_handler(self) -> None:
        """Submitting Feedbacks"""
        random_feedbacks = [int(x) for x in self.configurations.get("FEEDBACKS", "RANDOM_FEEDBACK_CHOICES").split(",")]
        for feedback_link in self.get_feedback_links():
            print(f"Feedback started => {feedback_link}")
            self.driver.get(feedback_link)
            questions = self.wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type=range]")))
            for question in questions:
                random_choice = random_feedbacks[random.randint(0, len(random_feedbacks) - 1)]
                question.clear()
                [question.send_keys(Keys.LEFT) for _ in range(random_choice)]
            comment = self.driver.find_element(By.CSS_SELECTOR, "textarea#description")
            comment.send_keys(self.configurations.get("FEEDBACKS", "FEEDBACK_COMMENT"))
            submit_button = self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "button[type=submit]")))
            submit_button.click()
            self.wait.until(ec.url_contains("student/qa/feedback"))
            print(f"Feedback completed => {feedback_link}")

            
    def run(self) -> bool:
        try:
            if not self.is_logged_in():
                self.login()
            self.feedbacks_handler()
            return True
        except:
            print("Error Occured!")
            traceback.print_exc()
            return False
        finally:
            print("Closing Browser")
            self.kill_browser(delete_profile=self.configurations.getboolean("BROWSER", "TEMPORARY"))


if __name__ == "__main__":
    completed = False
    while not completed:
        completed = QalamFeedbackAutomation().run()
    print("Quitting...")
