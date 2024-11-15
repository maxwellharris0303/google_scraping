import dns.resolver

def check_email_exists(email):
    # Split the email address into username and domain
    username, domain = email.split('@')

    # Perform DNS lookup for MX records of the domain
    try:
        mx_records = dns.resolver.query(domain, 'MX')
    except dns.resolver.NXDOMAIN:
        return False

    # If MX records exist, the email domain is valid
    return len(mx_records) > 0

# Example usage
email = '20190renovations@stanleymartin.com'
exists = check_email_exists(email)
if exists:
    print(f"The email '{email}' exists.")
else:
    print(f"The email '{email}' does not exist.")