import xml.etree.ElementTree as ET
import os
import boto3

# Amazon SNS configuration
SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN')  # Get the ARN of the topic from an environment variable
sns_client = boto3.client('sns')

# Path to the output.xml file
output_file = os.getenv('OUTPUT_FILE', 'output/output.xml')

try:
    # Parse the XML file
    tree = ET.parse(output_file)
    root = tree.getroot()

    # Counters for passed and failed tests
    passed = 0
    failed = 0
    total_tests = 0

    # Search for test results
    for test in root.findall('.//test'):
        status = test.find('status').get('status')
        total_tests += 1
        if status == 'PASS':
            passed += 1
        elif status == 'FAIL':
            failed += 1

    # Calculate percentages
    passed_percentage = (passed / total_tests) * 100 if total_tests > 0 else 0
    failed_percentage = (failed / total_tests) * 100 if total_tests > 0 else 0

    # Create the message
    message = (
        f"Test results:\n"
        f"- Total tests: {total_tests}\n"
        f"- Passed tests: {passed} ({passed_percentage:.2f}%)\n"
        f"- Failed tests: {failed} ({failed_percentage:.2f}%)\n"
    )

    # Send the message via SNS
    if SNS_TOPIC_ARN:
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="Robot Framework Test Results",
            Message=message
        )
        print("Message successfully sent to SNS.")
    else:
        print("SNS topic ARN not configured. Set SNS_TOPIC_ARN in the environment variables.")

except FileNotFoundError:
    print(f"File {output_file} not found. Make sure the file exists and the path is correct.")
except Exception as e:
    print(f"Error processing the file or sending the message: {e}")
