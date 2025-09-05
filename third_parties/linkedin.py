import os
from h11 import Response
import requests
from dotenv import load_dotenv


load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """
    scrape information from linkedin profiles,
    Manualy scrape the information from the LinkedIn profile
    """

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/maaz-codes/458d28f9310e75860043ae0870767579/raw/2840edb5f365b3748a5285083143a25758853c70/maaz-khan-scrapin.json"
        response = requests.get(
            url=linkedin_profile_url, 
            timeout=30
        )
        data = response.json().get("person")
    else:
        api_endpoint =  "https://api.scrapin.io/v1/enrichment/profile"
        # params = {
        #     "apikey": os.environ['SCRAPIN_API_KEY'],
        #     "linkedInUrl": linkedin_profile_url,
        # }
        response = requests.post(
            url=api_endpoint,
            headers={"x-api-key": os.environ['SCRAPIN_API_KEY']},
            json={"linkedInUrl": linkedin_profile_url},
            timeout=30,
        )
        data = response.json().get("person")
        data = {
            k: v
            for k, v in data.items()
            if v not in ([], "", '', None)
            and k not in ['certifications']
        }

    return data


def main():
    profile_url = "https://www.linkedin.com/in/maaz-khan-685982369/"
    profile = scrape_linkedin_profile(profile_url, mock=True)
    print(profile)


if __name__ == "__main__":
    main()
