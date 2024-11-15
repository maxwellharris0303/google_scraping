import smtplib
import dns.resolver

def check_email_exists(email):
    # Split the email address into username and domain
    username, domain = email.split('@')

    # Check the MX records for the email domain
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
    except dns.resolver.NXDOMAIN:
        print(f"The email domain '{domain}' does not exist.")
        return
    except dns.resolver.NoAnswer:
        print(f"No MX records found for the email domain '{domain}'.")
        return

    # Get the MX host with the highest priority
    mx_host = str(mx_records[0].exchange)

    # Create an instance of SMTP server
    smtp_server = smtplib.SMTP(mx_host)

    # Set up a 'hello' message to the server
    hello_msg = smtp_server.docmd('EHLO example.com')

    # Check if the email address exists
    try:
        # Verify the email address
        resp_code, resp_msg = smtp_server.verify(email)
        if resp_code == 250:
            print(f"The email address '{email}' exists.")
        else:
            print(f"The email address '{email}' does not exist.")
    except smtplib.SMTPException as e:
        print(f"An error occurred while verifying the email address: {str(e)}")

    # Close the connection to the server
    smtp_server.quit()

# Usage example
email_to_check = 'oscarrogers303@gmail.com'
check_email_exists(email_to_check)