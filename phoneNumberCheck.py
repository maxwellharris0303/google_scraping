import phonenumbers

def check_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number)
        return phonenumbers.is_valid_number(parsed_number)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False

# Example usage
phone_number = "+1 (250) 422-8184"
exists = check_phone_number(phone_number)
print(f"Phone number {phone_number} exists: {exists}")