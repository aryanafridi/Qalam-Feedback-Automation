# QALAM FEEDBACK AUTOMATION
Using Chrome Browser, the program automates the process for submitting QA Feedbacks in Feedback section of Qalam. Automations for other feedbacks will also be automated in future.

## Usage
 - ### Using compiled versions
    1. Download the compiled versions according to your Operating System. 
        - [Windows](/compiled/Windows.zip)
        - [Linux](compiled/Linux.zip)
        - MACOS version not available use raw version for MACOS.  
    2. Extract the files and edit `config.ini`. Provide Qalam ID and password. Other configurations can also be customized. See [configuration section](#configuration) for more information.
    3. For Linux users, give `Qalam Feedback Automation` executable permission using this command.  
        ```
        cd Directory-Containing-Qalam-Feedback
        chmod +x 'Qalam Feedback Automation'
        ```
        Replace Directory-Containing-Qalam-Feedback with path where Qalam Feedback Automation is placed.  
    4. Run `Qalam Feedback Automation` for Linux or `Qalam Feedback Automation.exe` for Windows. Use terminal for running program for better output.
- ### Using Raw version
    1. Download Python using [official website](https://python.org).
    2. Download and install requirements using following set of commands
        ```
        git clone https://github.com/aryanafridi/Qalam-Feedback-Automation/
        cd 'Qalam-Feedback-Automation'
        pip install -r requirements.txt
        ```
    3. Edit `config.ini`. Provide Qalam ID and password. Other configurations can also be customized. See [configuration section](#configuration) for more information.
    4. Run using following command.
        ```
        python qalam_feedback_automation.py
        ```
## Configuration
- QALAM USER 
    - This section contains Qalam ID and password. Provide these configuration for ogging in to Qalam.
- FEEDBACKS
    - Provide the comma separated list of Feeback choices ranging from 1 to 5 (1 For Excellent to 5 for Poor) Feedback in RANDOM_FEEDBACK_CHOICES. From these options randomly will be selected.
    - Provide feedback comment in FEEDBACK_COMMENT.
- BROWSER
    - If you want the browser profile to be created temporarily and deleted at the end use `TEMPORARY = YES`.
    - If `TEMPORARY = NO` is used the profile directory provided in `PROFILE` will be used and it will not be deleted.
> ### Example Configuration
    [QALAM USER]
    QALAM_ID = MyUsername
    PASSWORD = mypassword

    [FEEDBACKS]
    RANDOM_FEEDBACK_CHOICES = 1,2,3
    FEEDBACK_COMMENT = :)

    [BROWSER]
    TEMPORARY = NO
    PROFILE = BrowserData

