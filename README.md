# LongS checkouter

Version = 1.0.0

## What is it?

Since it's difficult nowadays to book from Esselunga's website, I try to automate their availability by automate the checkout process.
Note: this only works if there are items in the basket. I do not the shopping for you (at least, not for now). 

## Let it work

#### Single run
After all the installation process, run the script ```job.sh``` (I know the name is horrible, suggestions are accepted!).
#### Via a cron job
You can automate the script by adding a rule to crontab  

    crontab -e

and then `0 * * * * /path/to/the/checkouter/job.sh`. This is just an example. You can run it whenever you want (or at least until the police comes).

## How do I get it?

#### Clone the repo

    git clone 

#### Run the setup script

Run ```setup.sh```. This will:

   * create and activate the virtualenv
   * install the dependencies
   * create the ``.env`` file where you store all the sensitive information and configuration
   
#### The .env file

Here is a description of which environment variable you need:

    PYTHONPATH=/path/to/this/repo/checkouter:$PYTHONPATH => you need to add the path where you download this repo
    PATH=/path/to/the/virtualenv/venv/bin:$PATH => same as above. The virtualenv is created in the project's path
    SERVICE_EMAIL=email.used.as.a.notification_service@gmail.com => this is optional. I'll explain it later
    SERVICE_PASSWORD=password_of_the_service_email_account => this is optional. Same as above
    EMAIL=esselunga_registration_email@some_email.com => Your registration email
    PASSWORD=esselunga_account_password => your registration password
    WEB_DRIVER=/path/to/the/webdriver/executable => the path where you download the browser executable (see below) 
    
The `SERVICE_EMAIL` is a gmail account from where the notification are sent. You must allow the "less secure apps" in order to work (https://support.google.com/accounts/answer/6010255?hl=en)
   
#### Get the selenium web driver you want

This application runs with selenium webdriver. You need to download and install a web driver. Here is a list:

* Chrome => https://chromedriver.chromium.org/
* Firefox => https://developer.mozilla.org/en-US/docs/Web/WebDriver
* Safari => https://developer.apple.com/documentation/webkit/testing_with_webdriver_in_safari
* Internet explorer => R U serious?