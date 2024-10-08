from selenium import webdriver
from selenium.webdriver.common.by import By
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
        selenium_url = "http://localhost:4444/wd/hub"
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Remote(command_executor=selenium_url, options=chrome_options)

        try:
            # Replace with the actual EC2 instance public DNS/IP
            driver.get("http://example-ec2-instance-url")  # Modify with actual EC2 URL

            # Perform validation (e.g., checking a page element)
            element = driver.find_element(By.ID, "expected-element-id")  # Adjust as needed
            print("Element found, instance validation successful!")
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
