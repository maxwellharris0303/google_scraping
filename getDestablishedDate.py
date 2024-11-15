import whois

def get_establishment_date(url):
    try:
        domain = whois.whois(url)
        print(domain)
        creation_date = domain.updated_date
        if isinstance(creation_date, list):
            return creation_date[0].strftime("%Y-%m-%d")
        else:
            return creation_date.strftime("%Y-%m-%d")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
website_url = "https://www.qualityfirsthome.com/"
establishment_date = get_establishment_date(website_url)
if establishment_date:
    print(f"The establishment date of {website_url} is {establishment_date}.")