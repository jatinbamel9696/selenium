from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
        time.sleep(2)

        # Click on Sign In to the Console
        sign_in = driver.find_element(By.LINK_TEXT, 'Sign In to the Console')
        sign_in.click()
        time.sleep(3)

        # Enter AWS access key
        access_key_input = driver.find_element(By.NAME, 'username')
        access_key_input.send_keys(os.environ['AWS_ACCESS_KEY_ID'])

        # Click Next
        driver.find_element(By.ID, 'signin_submit').click()
        time.sleep(3)

        # Enter AWS secret key
        secret_key_input = driver.find_element(By.NAME, 'password')
        secret_key_input.send_keys(os.environ['AWS_SECRET_ACCESS_KEY'])

        # Click Sign In
        driver.find_element(By.ID, 'signin_submit').click()
        time.sleep(5)

        # Navigate to the EC2 Dashboard
        driver.get('https://console.aws.amazon.com/ec2/v2/home')
        time.sleep(5)

        # Search for the instance by ID
        search_box = driver.find_element(By.XPATH, '//*[@id="search-ec2"]')
        search_box.send_keys(instance_id + Keys.RETURN)
        time.sleep(5)

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
