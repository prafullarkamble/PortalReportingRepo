from datetime import date, timedelta, datetime
import inspect
import os
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import shutil
import time
import unicodedata
import zipfile
from email import encoders
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


ChromeDriver = 'C:\\PortalTesting\\Drivers\\chromedriver.exe'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--incognito")

# chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(executable_path=ChromeDriver, chrome_options=chrome_options)
driver.maximize_window()

# ------------------- login ------------------- #
driver.implicitly_wait(130)


class PortalTesting:

    start = time.time()

    def login(self):
        # driver.get("http:\\google.com")
        driver.get("https://portal.touchcommerce.com/portal/portal.jsp")

        # wait = WebDriverWait(driver, 10)
        # driver.implicitly_wait(30)
        username = driver.find_element_by_css_selector("#uid")
        username.send_keys("portal@testing")
        password = driver.find_element_by_css_selector("#pid")
        password.send_keys("Summer01")

        login_button = driver.find_element_by_class_name("secondarybtnlabel")
        login_button.click()
        # time.sleep(30)
        driver.get_screenshot_as_file("C:\\Nuance\\New folder\\login.png")

    def create_new_folder(self):

        self.screenshots_folder = ''
        self.new_folder_name = ''
        try:
            self.tday = datetime.today().strftime('%Y%m%d-%H%M')
            # print(tday)
            # Get currently executing file name
            full_file_name = os.path.basename(__file__)
            file_name = os.path.splitext(full_file_name)[0]
            # print(file_name)
            # Create a new folder with filename and timestamp

            self.new_folder_name = file_name + "-" + self.tday
            print('Folder ' + self.new_folder_name + ' created.')
            os.mkdir(self.new_folder_name)

            self.screenshots_folder = os.path.join(os.path.dirname(__file__), self.new_folder_name).replace('\\', '/')
            # print(self.screenshots_folder)
            os.chdir(self.screenshots_folder)
            print("We are in ", os.getcwd())

        # will get an error if folder already exists
        except WindowsError as e:
            print("Please run the file after a minute. ", e)



    # Get the currently running function name
    def get_current_function(self):
        # self.now_running = ''
        frame = inspect.currentframe()
        self.now_running = inspect.currentframe(frame).function
        print(type(self.now_running))
        print(self.now_running)

    def get_portal_name(self):

        active_cluster = ['elv3portal12', 'elv3portal11']
        not_active_cluster = ['elv3portal01', 'elv3portal02']

        dc_elm = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[4]/div/div[3]/div/div[2]/span[2]').text

        print(dc_elm)
        print(type(dc_elm))

        new = unicodedata.normalize('NFKD', dc_elm).encode('ascii', 'ignore').split()

        print("Current portal is ", new[-1])
        try:

            if new[-1] in active_cluster:
                print('DC name is same')
                self.admin()
                self.transcript()
            else:
                print('DC name is different.')
                self.close_browser()
        except Exception as e:
            print("There is something wrong. Error :====>", e)

        # else:
        #     time.sleep(4)
        #     print('Names are different.')
        #     driver.close()

    def close_browser(self):
        driver.close()

    # ------------------- Select BU ------------------- #

    def get_business_unit(self):
        # Click on a dropdown
        # elm = driver.find_element_by_id('isc_B')
        # time.sleep(2)
        # elm.send_keys(Keys.HOME)
        # time.sleep(2)
        # elm.click()
        # time.sleep(2)
        # driver.find_element_by_xpath("//*[contains(text(), 'BestBrands')]").click()

        # Alternative for above code,
        elm = driver.find_element_by_class_name('selectItemText').click()
        rpt_e5 = driver.find_element_by_xpath('//*[@id="isc_Ftable"]/tbody/tr[1]/td/div/span')
        hover5 = ActionChains(driver).move_to_element(rpt_e5).click().perform()
        print("BU set.")

    # ------------------- Administration ------------------- #

    def admin(self):
        element = driver.find_element_by_id('admin_menu')
        hover = ActionChains(driver).move_to_element(element)
        hover.click().perform()
        # time.sleep(5)

        e1 = driver.find_element_by_id('sitesAndUsers')
        hover1 = ActionChains(driver).move_to_element(e1)
        hover1.perform()

        e2 = driver.find_element_by_id('getNewUserManagement')
        hover2 = ActionChains(driver).move_to_element(e2)
        hover2.click().perform()
        time.sleep(2)

        # select checkbox
        e3 = driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div[2]/table/tbody/tr[1]/td[1]/input')
        e3.click()
        time.sleep(2)

        # edit button
        e4 = driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div[4]/div[1]/button[2]/span').click()
        time.sleep(2)

        # General information
        e5 = driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div/table/tbody/tr/td[1]/left-navigation/nav/ul/li[1]/button/span').click()
        time.sleep(5)

        screenshot_name = self.tday + "_Administration.png"
        driver.get_screenshot_as_file(screenshot_name)

        # Agent configuration
        e6 = driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div/table/tbody/tr/td[1]/left-navigation/nav/ul/li[2]/button/span').click()
        time.sleep(5)

        # Agent skills
        e7 = driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div/table/tbody/tr/td[1]/left-navigation/nav/ul/li[3]/button').click()
        time.sleep(5)

        # Security settings
        e8 = driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div/table/tbody/tr/td[1]/left-navigation/nav/ul/li[4]/button').click()
        time.sleep(2)

        # Cancel button
        e9 = driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div/table/tbody/tr/td[2]/div/div[2]/div/div[2]/a').click()
        print("Administration check complete.")

        time.sleep(5)

    def BU_test(self):
        element = driver.find_element_by_id('admin_menu')
        hover = ActionChains(driver).move_to_element(element)
        hover.click().perform()
        # time.sleep(5)

        e10 = driver.find_element_by_id('programManagement')
        hover1 = ActionChains(driver).move_to_element(e10)
        hover1.perform()

        e11 = driver.find_element_by_id('getBusinessRules')
        hover1 = ActionChains(driver).move_to_element(e11)
        hover1.click().perform()

        time.sleep(5)
        e12 = driver.find_element_by_id('gwt-debug-businessRule-sourceHeader')
        hover1 = ActionChains(driver).move_to_element(e12)
        hover1.click().perform()

        screenshot_name = self.tday + "_BU_Rules.png"
        driver.get_screenshot_as_file(screenshot_name)
        print("BU rules check complete.")


    # ------------------- Transcript ------------------- #


    def transcript(self):

        tr_e1 = driver.find_element_by_id('Transcript_ID')
        hover1 = ActionChains(driver).move_to_element(tr_e1)
        hover1.click().perform()

        tr_e2 = driver.find_element_by_id('sub_transcript_id')
        hover2 = ActionChains(driver).move_to_element(tr_e2).click().perform()

        time.sleep(5)
        tr_e3 = driver.find_element_by_id('gwt-debug-transcriptSearch-searchButton')
        hover3 = ActionChains(driver).move_to_element(tr_e3).click().perform()

        # Enter date
        start_date = date.today() - timedelta(5)
        start_date.strftime('%m-%d-%Y')
        driver.find_element_by_id('gwt-DateBox').send_keys('')
        print("Transcript check complete.")
        time.sleep(8)
        # print("self.screenshots_folder inside transcripts: ", self.screenshots_folder)
        screenshot_name = self.tday + "_Transcripts.png"
        driver.get_screenshot_as_file(screenshot_name)

    # ------------------- Reporting ------------------- #

    def reporting(self):

        try:
            # t1 = driver.find_element_by_id('Transcript_ID')
            # hover = ActionChains(driver).move_to_element(t1)
            # hover.click().perform()

            # Reports tab
            rpt_e1 = driver.find_element_by_id('report_menu_id')
            hover1 = ActionChains(driver).move_to_element(rpt_e1)
            hover1.click().perform()

            driver.find_element_by_id('gwt-uid-12').click()

            # Choose report
            driver.find_element_by_id('gwt-debug-buttonsPanel').click()

            rpt_e11 = driver.find_element_by_class_name('gwt-MenuItem')
            hover11 = ActionChains(driver).move_to_element(rpt_e11)
            hover11.perform()

            # rpt_e1 = driver.find_element_by_id('report_menu_id')
            # hover1 = ActionChains(driver).move_to_element(rpt_e1)
            # hover1.perform()

            rpt_e2 = driver.find_element_by_id('Standard Reports')
            hover2 = ActionChains(driver).move_to_element(rpt_e2).perform()

            time.sleep(0.5)
            rpt_e3 = driver.find_element_by_id('Program Reports')
            hover3 = ActionChains(driver).move_to_element(rpt_e3).perform()

            time.sleep(0.5)
            rpt_e4 = driver.find_element_by_id('Client Performance Report Totals')
            hover4 = ActionChains(driver).move_to_element(rpt_e4).perform()

            time.sleep(0.5)
            # rpt_e5 = driver.find_element_by_link_text('By Page')
            # hover5 = ActionChains(driver).move_to_element(rpt_e5).perform()
            rpt_e5 = driver.find_element_by_xpath("//*[contains(text(), 'By Date')]")
            hover5 = ActionChains(driver).move_to_element(rpt_e5).click().perform()

            time.sleep(5)
            # rpt_e6 = driver.find_element_by_xpath('//*[@id="reportingcalendar"]/ul/li/div[2]/div')

            # # Click on run report button
            # rpt_e6 = driver.find_element_by_xpath("//*[contains(text(), 'Run Report')]")
            # click = ActionChains(driver).move_to_element(rpt_e6).click().perform()
            #
            # set_prt_date = driver.find_element_by_xpath('//*[@id="reportingcalendar"]/ul/li/div[1]/span')
            # yesterday = date.today() - timedelta(5)
            # date2 = yesterday.strftime('%m-%d-%Y')
            # today = date.today()
            # date1 = today.strftime('%m-%d-%Y')
            # rpt_date = '{} - {}'.format(date1, date2)
            # print(rpt_date)


            # Click on a down arrow to get calender
            rpt_btn = driver.find_element_by_xpath('//*[@id="gwt-debug-arrowDOWN"]')
            click = ActionChains(driver).move_to_element(rpt_btn).click().perform()

            # Select 1st date
            rpt_date = driver.find_element_by_xpath('//*[@id="threeMonthRange"]/div[6]/div[1]')
            click = ActionChains(driver).move_to_element(rpt_date).click().perform()
            time.sleep(2)

            # Select 2nd date
            rpt_date_2 = driver.find_element_by_xpath('//*[@id="threeMonthRange"]/div[6]/div[6]')
            click = ActionChains(driver).move_to_element(rpt_date_2).click().perform()
            time.sleep(2)

            # Click on a Apply button
            apply_btn = driver.find_element_by_xpath('//*[@id="reportingcalendar"]/ul/li/div[3]/div[1]/div/div[1]')
            click = ActionChains(driver).move_to_element(apply_btn).click().perform()
            time.sleep(2)

            # Click on a Run Report button
            # time.sleep(2)
            rpt_e6 = driver.find_element_by_xpath("//*[contains(text(), 'Run Report')]")
            click = ActionChains(driver).move_to_element(rpt_e6).click().perform()

            time.sleep(5)

            # Check for report graph
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, 'PortalChartContainer'))).click()
            screenshot_name = self.tday + "_Reports.png"
            driver.get_screenshot_as_file(screenshot_name)
            print("Reporting check complete.")
        except:
            pass


        # ------------------- Set report date ------------------- #

        # yesterday = date.today() - timedelta(5)
        # date2 = yesterday.strftime('%m-%d-%Y')
        # today = date.today()
        # date1 = today.strftime('%m-%d-%Y')
        # rpt_date = '{} - {}'.format(date1, date2)
        # print(rpt_date)
        #
        # time.sleep(5)
        # rpt_e6 = driver.find_element_by_xpath("//*[contains(text(), 'Run Report')]")
        # click = ActionChains(driver).move_to_element(rpt_e6).click().perform()



    # def zip_folder(self):
    #     folder_name = self.new_folder_name
    #     print("abs path: ", os.path.abspath(folder_name))
    #     print('screenshot: ', self.screenshots_folder)
    #     print(folder_name)
    #     try:
    #         for file in os.listdir(folder_path):
    #             if file.endswith('.png'):
    #                 print(file)
    #                 # all_zip_files.append(file)
    #                 # shutil.make_archive('Zip_Folder_Test', 'zip', folder_path)
    #             else:
    #                 pass
    #
    #     except Exception as e:
    #         print("error: ", e)
    #     # finally:
    #     #     shutil.make_archive('Zip_Folder_Test', 'zip', folder_path)
    #
    #     shutil.make_archive('DC1-Chrome', 'zip', self.screenshots_folder)
    #     print('Screenshots have been zipped.')

    def zip_screenshots(self):
        all_zip_files = []
        try:
            for file in os.listdir(self.screenshots_folder):
                if file.endswith('.png'):
                    print("Captured screenshots:\n", file)
                    all_zip_files.append(file)
                    # shutil.make_archive('NEW_TEST', 'zip', folder_path)
                else:
                    pass

            self.zip_file_name = self.new_folder_name + ".zip"
            with zipfile.ZipFile(self.zip_file_name, 'w') as myzip:
                print('Zipping...')
                for f in all_zip_files:
                    myzip.write(f)
        except Exception as e:
            print("Error: ====> ", e)

        time.sleep(5)
    def send_email(self):

        try:
            sender = 'prafulla.kamble@nuance.com'
            receiver = 'prafulla.kamble@nuance.com'
            msg = MIMEMultipart()

            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = self.new_folder_name + 'Portal Automation testing results'

            body = 'Hi, \n\n Attached are the portal automation test results. Below are the scenarios covered, \n\n 1) Business Rules ' \
                ' \n 2)Reports \n 3) Transcripts \n 4) User Administration \n\n' \
            'Please validate the the test results.'

            msg.attach(MIMEText(body, 'plain'))

            # filename = 'C:\\PortalTesting\\DC4\\DC4_Firefox-20180508-1725\\DC4_Firefox-20180508-1725.zip'
            filename = self.zip_file_name
            attachment = open(filename, 'rb')

            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            # part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= " + filename)

            msg.attach(part)

            server = smtplib.SMTP('mail.nuance.com', 587)
            server.starttls()
            server.login(sender, "Pa00word")
            text = msg.as_string()
            server.sendmail(sender, receiver, text)
            server.quit()
            print('.......')
            print("Email sent.")
            print("-------------------------------------------------------------------------------------")
        except Exception as e:
            print('Email can not be sent. Error ====>', e)


pt = PortalTesting()

start_time = time.time()

pt.login()
pt.create_new_folder()
# pt.get_current_function()
# pt.get_portal_name()
pt.get_business_unit()
# pt.BU_test()
# pt.transcript()
pt.reporting()
pt.admin()
pt.zip_screenshots()
pt.send_email()
pt.close_browser()
end_time = time.time()

print("Time2 taken to complete the tests: ", end_time - start_time)
