def format_phone_number(phone_number):
    # Remove any non-digit characters from the phone number
    array = []
    for num in phone_number:
        digits = ''.join(filter(str.isdigit, num))
        digits = digits[-10:]
        print(digits)

        # Check if the phone number has a valid length
        if len(digits) < 10:
            return "Invalid phone number"

        # Format the phone number in the desired format
        formatted_number = "+1 ({}) {}-{}".format(digits[-10:-7], digits[-7:-4], digits[-4:])

        array.append(formatted_number)

    return array

# Example usage
phone_number = ['15 211 513 464', '15 342 513 464', '25 354 123 456']
formatted_number = format_phone_number(phone_number)
print("Formatted phone number:", formatted_number)