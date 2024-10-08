from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import boto3

# Function to validate EC2 instance
def validate_ec2_instance(instance_id):
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances(InstanceIds=[instance_id])
    instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']
    
    if instance_state == 'running':
        print(f"Instance {instance_id} is running")

        # Set up Selenium to connect to the container
        selenium_url = "http://localhost:4444/wd/hub"  # Connect to the Selenium server running in the service
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")  # Disable sandbox for Chrome
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

        # Connect to the Selenium server
        driver = webdriver.Remote(command_executor=selenium_url, options=chrome_options)

        try:
            # Replace with the actual EC2 instance public DNS/IP
            driver.get("http://3.80.247.247")  # Modify with actual EC2 URL

            # Check if the expected text is present on the page
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))  # Assuming "h1" tag or check for the welcome text
            )
            page_source = driver.page_source
            
            # Validate the presence of the nginx welcome message
            if "Welcome to nginx!" in page_source:
                print("Nginx welcome message found, instance validation successful!")
            else:
                print("Nginx welcome message not found, instance validation failed.")
        except Exception as e:
            print(f"Error during instance validation: {e}")
            return False
        finally:
            driver.quit()

        return True
    else:
        print(f"Instance {instance_id} is not running. Current state: {instance_state}")
        return False


if __name__ == "__main__":
    # Hardcoded EC2 instance ID
    instance_id = "i-037b62ef3a84bff22"  # Hardcoded instance ID

    if validate_ec2_instance(instance_id):
        print("EC2 instance validation passed.")
    else:
        print("EC2 instance validation failed.")
