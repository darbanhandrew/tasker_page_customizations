# import frappe
# import requests
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# # def send_email_via_mailgun(recipient, subject, body, tags=None, deliverytime=None, dkim=None,
# #                            testmode=None, tracking=None, tracking_clicks=None, tracking_opens=None, custom_headers=None,
# #                            custom_variables=None):
# #     api_key = 'ee5417ba40ff7c6e5871251552e3863e-7ca144d2-2a123627'
# #     domain = 'taskerpage.com'
# #     sender = 'postmaster@taskerpage.com'
# #     # Create a MIME message
# #     msg = MIMEMultipart()
    
# #     # Change the sender address here
# #     msg['From'] = sender
    
# #     msg['To'] = recipient
# #     msg['Subject'] = subject

# #     # Attach the body of the email
# #     msg.attach(MIMEText(body, 'plain'))

# #     # Additional headers
# #     if custom_headers:
# #         for key, value in custom_headers.items():
# #             msg[key] = value

# #     # Create the Mailgun API URL
# #     url = f"https://api.eu.mailgun.net/v3/{domain}/messages.mime"

# #     # Create the data for the POST request
# #     data = {
# #         'to': recipient,
# #         'message': msg.as_string()
# #     }

# #     # Optional parameters
# #     if tags:
# #         data['o:tag'] = tags
# #     if deliverytime:
# #         data['o:deliverytime'] = deliverytime
# #     if dkim:
# #         data['o:dkim'] = dkim
# #     if testmode:
# #         data['o:testmode'] = testmode
# #     if tracking:
# #         data['o:tracking'] = tracking
# #     if tracking_clicks:
# #         data['o:tracking-clicks'] = tracking_clicks
# #     if tracking_opens:
# #         data['o:tracking-opens'] = tracking_opens
# #     if custom_variables:
# #         for key, value in custom_variables.items():
# #             data[f'v:{key}'] = value

# #     # Send the request using requests library
# #     response = requests.post(url, auth=("api", api_key), data=data)

# #     # Check the response
# #     if response.status_code == 200:
# #         return True
# #     else:
# #         return False

# # # Example usage:


# # def send(self, sender, recipient, msg):
# #     print("Hello")
# #     subject = msg.get("subject", "")
# #     body = msg.get("message", "")
    
# #     # Customize additional options as needed
# #     tags = None
# #     deliverytime = None
# #     dkim = None
# #     testmode = None
# #     tracking = None
# #     tracking_clicks = None
# #     tracking_opens = None
# #     custom_headers = None
# #     custom_variables = None
    
# #     # Send the email using Mailgun API
# #     hello
# #     result = send_email_via_mailgun(sender, recipient, subject, body, tags, deliverytime, dkim, testmode,
# #                                     tracking, tracking_clicks, tracking_opens, custom_headers, custom_variables)
    
# #     self.update_status("Sending")


# # def get_sender_details():
# #     return "Taskerpage No-Reply", "postmaster@taskerpage.com"

# #  Define your custom function
# @frappe.whitelist(allow_guest=True)
# def send_email_via_mailgun():
#     api_key = 'ee5417ba40ff7c6e5871251552e3863e-7ca144d2-2a123627'
#     domain = 'taskerpage.com'
#     sender = 'Excited User <postmaster@taskerpage.com>'
#     recipient = 'darbanhandrew@gmail.com'
#     subject = 'Hello'
#     text = 'Testing some Mailgun awesomeness!'

#     # Create the Mailgun API URL
#     url = f"https://api.eu.mailgun.net/v3/{domain}/messages"

#     # Create the data for the POST request
#     data = {
#         'from': sender,
#         'to': recipient,
#         'subject': subject,
#         'text': text,
#     }

#     # Send the request using requests library
#     response = requests.post(url, auth=("api", api_key), data=data)

#     # Check the response
#     if response.status_code == 200:
#         return True
#     else:
#         return False

import random
import string
import requests
import frappe

def generate_verification_code(length=6):
    """Generate a random verification code."""
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(length))
    return code

def send_email_via_mailgun(recipient, subject, body):
    api_key = 'ee5417ba40ff7c6e5871251552e3863e-7ca144d2-2a123627'
    domain = 'taskerpage.com'
    sender = 'Taskerpage No-Reply <postmaster@taskerpage.com>'
    """Send an email using the Mailgun API."""
    url = f"https://api.eu.mailgun.net/v3/{domain}/messages"
    data = {
        'from': sender,
        'to': recipient,
        'subject': subject,
        'text': body,
    }
    response = requests.post(url, auth=("api", api_key), data=data)
    return response.status_code

@frappe.whitelist(allow_guest=True)
def send_verification_code_to_email(user_profile):
    try:
        # Generate a verification code
        verification_code = generate_verification_code()

        # Save the verification code in the user's profile
        customer_profile = frappe.get_doc("Customer Profile",user_profile)
        
        customer_profile.set("email_verification_code", verification_code)
        customer_profile.save()
        user = frappe.get_doc("User", customer_profile.user)
        user_email = user.email
        # Compose and send the email with the verification code using Mailgun
        subject = "Verification Code"
        message = f"Your verification code is: {verification_code}"

        response_code = send_email_via_mailgun(user_email, subject, message)

        if response_code == 200:
            return {"status": "success", "message": "Verification code sent successfully."}
        else:
            return {"status": "error", "message": "Failed to send verification code email."}

    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist()
def check_verification_code(profile_id, entered_code):
    try:
        # Retrieve the user's profile
        user = frappe.get_doc("User", profile_id)

        # Get the stored verification code
        stored_code = user.get("verification_code")

        # Check if the entered code matches the stored code
        if entered_code == stored_code:
            # Clear the verification code after successful verification
            user.set("verification_code", "")
            user.save()
            return {"status": "success", "message": "Verification code matched."}
        else:
            return {"status": "error", "message": "Verification code does not match."}
    except Exception as e:
        return {"status": "error", "message": str(e)}