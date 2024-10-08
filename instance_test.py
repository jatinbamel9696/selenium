import boto3
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def get_instance_status(instance_id):
    ec2 = boto3.client('ec2')
    response = ec2.describe_instance_status(InstanceIds=[instance_id])
    instance_status = response['InstanceStatuses'][0]['InstanceState']['Name']
    return instance_status

def validate_ec2_instance(instance_id):
    # Step 1: Check EC2 instance status using boto3
    status = get_instance_status(instance_id)
    if status == 'running':
        print(f"Instance {instance_id} is running")
    else:
        print(f"Instance {instance_id} status: {status}")
        return False

    # Step 2: Use Selenium to validate the instance
    # Example: Launch a browser to verify instance via a web interface (if applicable)
    driver = webdriver.Chrome()
    driver.get("http://3.80.247.247")  # Replace with actual EC2 instance URL if necessary

    try:
        # Example of checking a web element on the instance page
        element = driver.find_element(By.ID, "expected-element-id")
        print("Element found, instance validation successful!")
    except Exception as e:
        print(f"Error during instance validation: {e}")
        return False
    finally:
        driver.quit()
    
    return True

if __name__ == "__main__":
    instance_id = "i-037b62ef3a84bff22"  # Replace with your EC2 instance ID
    if validate_ec2_instance(instance_id):
        print("EC2 instance validation passed.")
    else:
        print("EC2 instance validation failed.")
