from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Hardcoded instance ID
instance_id = 'i-037b62ef3a84bff22'  # Replace with your instance ID

# Function to validate EC2 instance
def validate_ec2_instance(instance_id):
    # Set up WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode for CI/CD
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=options
    )

    try:
        # Open AWS login page
        driver.get('https://aws.amazon.com/')
        
        # Wait for the Sign In link to be present and click it
        sign_in = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Sign In to the Console'))
        )
        sign_in.click()

        # Wait for username input field to be present
        access_key_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        access_key_input.send_keys(os.environ['AWS_ACCESS_KEY_ID'])

        # Click Next
        driver.find_element(By.ID, 'signin_submit').click()

        # Wait for the password input field to be present
        secret_key_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'password'))
        )
        secret_key_input.send_keys(os.environ['AWS_SECRET_ACCESS_KEY'])

        # Click Sign In
        driver.find_element(By.ID, 'signin_submit').click()

        # Wait for the EC2 dashboard to load
        WebDriverWait(driver, 10).until(
            EC.url_contains('ec2/home')
        )

        # Navigate to the EC2 Dashboard
        driver.get('https://console.aws.amazon.com/ec2/v2/home')

        # Wait for the search box to be present and search for the instance
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="search-ec2"]'))
        )
        search_box.send_keys(instance_id + Keys.RETURN)

        # Wait for the instance details to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{instance_id}')]"))
        )

        # Check instance status
        try:
            instance_status = driver.find_element(By.XPATH, f"//td[contains(text(), '{instance_id}')]/following-sibling::td[1]").text  # Status
            print(f"Instance {instance_id} is {instance_status}.")

            # Retrieve other instance details
            ram = driver.find_element(By.XPATH, f"//td[contains(text(), '{instance_id}')]/following-sibling::td[4]").text  # RAM
            public_ip = driver.find_element(By.XPATH, f"//td[contains(text(), '{instance_id}')]/following-sibling::td[5]").text  # Public IP
            private_ip = driver.find_element(By.XPATH, f"//td[contains(text(), '{instance_id}')]/following-sibling::td[6]").text  # Private IP
            hostname = driver.find_element(By.XPATH, f"//td[contains(text(), '{instance_id}')]/following-sibling::td[3]").text  # Hostname

            print(f"RAM: {ram}")
            print(f"Hostname: {hostname}")
            print(f"Public IP: {public_ip}")
            print(f"Private IP: {private_ip}")

        except Exception as e:
            print(f"Error retrieving instance details: {str(e)}")

    finally:
        # Close the browser
        driver.quit()

# Call the validation function
if __name__ == "__main__":
    validate_ec2_instance(instance_id)





# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# import os
# import boto3

# # Function to validate EC2 instance
# def validate_ec2_instance(instance_id):
#     ec2 = boto3.client('ec2')
#     response = ec2.describe_instances(InstanceIds=[instance_id])
#     instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']
    
#     if instance_state == 'running':
#         print(f"Instance {instance_id} is running")

#         # Set up Selenium to connect to the container
#         selenium_url = "http://localhost:4444/wd/hub"  # Connect to the Selenium server running in the service
#         chrome_options = Options()
#         chrome_options.add_argument("--headless")  # Run in headless mode
#         chrome_options.add_argument("--no-sandbox")  # Disable sandbox for Chrome
#         chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

#         # Connect to the Selenium server
#         driver = webdriver.Remote(command_executor=selenium_url, options=chrome_options)

#         try:
#             # Replace with the actual EC2 instance public DNS/IP
#             driver.get("http://3.80.247.247")  # Modify with actual EC2 URL

#             # Perform validation (e.g., checking a page element)
#             element = driver.find_element(By.ID, "expected-element-id")  # Adjust as needed
#             print("Element found, instance validation successful!")
#         except Exception as e:
#             print(f"Error during instance validation: {e}")
#             return False
#         finally:
#             driver.quit()

#         return True
#     else:
#         print(f"Instance {instance_id} is not running. Current state: {instance_state}")
#         return False


# if __name__ == "__main__":
#     # Hardcoded EC2 instance ID
#     instance_id = "i-037b62ef3a84bff22"  # Hardcoded instance ID

#     if validate_ec2_instance(instance_id):
#         print("EC2 instance validation passed.")
#     else:
#         print("EC2 instance validation failed.")
