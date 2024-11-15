import requests

def get_company_info(url, api_key):
    # Construct the API endpoint URL
    endpoint = f"https://company.clearbit.com/v1/domains/find?name={url}"
    
    # Set the API key as a header
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    
    # Send a GET request to the API
    response = requests.get(endpoint, headers=headers)
    print(response)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Extract the company name and founding date
        company_name = data.get('name')
        founding_date = data.get('foundedYear')
        
        return company_name, founding_date
    
    return None, None

# Example usage
website_url = 'example.com'
api_key = 'sk_f43756c100d9fba51513b1f1fe95f7ac'

company_name, founding_date = get_company_info(website_url, api_key)

print('Company Name:', company_name)
print('Founding Date:', founding_date)