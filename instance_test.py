import boto3
import sys

# Hardcoded instance ID
instance_id = 'i-037b62ef3a84bff22'

def validate_ec2_instance(instance_id):
    ec2 = boto3.client('ec2')

    try:
        # Describe the EC2 instance
        response = ec2.describe_instances(InstanceIds=[instance_id])
        instance = response['Reservations'][0]['Instances'][0]

        # Check if the instance is running
        state = instance['State']['Name']
        if state != 'running':
            print(f"Instance {instance_id} is {state}.")
            return False

        # Get instance details
        ram = instance['MemoryInfo']['SizeInMiB'] if 'MemoryInfo' in instance else "Memory info not available"
        public_ip = instance.get('PublicIpAddress', 'No Public IP assigned')
        private_ip = instance['PrivateIpAddress']
        hostname = instance['PrivateDnsName']

        print(f"Instance {instance_id} is running.")
        print(f"RAM: {ram} MiB")
        print(f"Hostname: {hostname}")
        print(f"Public IP: {public_ip}")
        print(f"Private IP: {private_ip}")

        return True

    except Exception as e:
        print(f"Error during instance validation: {str(e)}")
        return False

# Call the validation function
if __name__ == "__main__":
    if validate_ec2_instance(instance_id):
        print("EC2 instance validation succeeded.")
    else:
        print("EC2 instance validation failed.")



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
