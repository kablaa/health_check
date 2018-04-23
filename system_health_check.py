#!/usr/bin/python -p
import subprocess
import boto3
import time
from botocore.exceptions import ClientError

# Replace sender@example.com with your "From" address.
# This address must be verified with Amazon SES.
SENDER = "omega@hackmy.world"

# Replace recipient@example.com with a "To" address. If your account
# is still in the sandbox, this address must be verified.
RECIPIENT = "kablaa@hackmy.world"

# Specify a configuration set. If you do not want to use a configuration
# set, comment the following variable, and the
# ConfigurationSetName=CONFIGURATION_SET argument below.
CONFIGURATION_SET = "server-health"

# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_REGION = "us-west-2"

# The subject line for the email.
SUBJECT = "System Health Check"

# The character encoding for the email.
CHARSET = "UTF-8"




def getZpoolHealth():
    """returns a string containing sensor readings"""
    command = ["zpool","status","-x"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    out, err = process.communicate()
    if err is None:
        return out
    else:
        return "An error occurred while retrieving system info: " + err
    return out



def makeEmailBody(zpoolHealth):
    """compiles all of the information to be sent in a nice format and
    returns the email body"""
# The HTML body of the email.
    final = []
    bodyHTML = """
    <html>
        <head><h1>Warning! Zpool Health is Degraded!</h1></head>
        <body>
          <p>This check was performed on: """ + time.ctime() + """</p>
          <h2>Zpool Health Status</h2>
            <pre>
            """ + zpoolHealth + """
            </pre>
        </body>
    </html>
    """
    final.append(bodyHTML)
    bodyText = (
            "System Health Check \n\n"
            "This check was performed on: " + time.ctime() + " \n\n" +
            "Zpool Health: \n" + zpoolHealth
            )
    final.append(bodyText)
    return final

def sendEmail(body):
# Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
    # Try to send the email.
    try:
#Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': body[0],
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': body[1],
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            ConfigurationSetName=CONFIGURATION_SET,
        )
# Display an error if something goes wrong.
    except ClientError as e:
	print(e.response['Error']['Message'])
    else:
	print("Email sent! Message ID:"),
	print(response['ResponseMetadata']['RequestId'])
	"""sends an email via aws SES"""

def main():
    while True:
        zpoolHealth = getZpoolHealth()
        if zpoolHealth != "all pools are healthy\n":
            body = makeEmailBody(zpoolHealth)
            sendEmail(body)
        time.sleep(60*60*24)

if __name__ == "__main__":
        main()


