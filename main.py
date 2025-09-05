from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from third_parties.linkedin import scrape_linkedin_profile


load_dotenv()


def main():
    print("Hello from Capstone-01!")

    summary_template = """
        given the linkedin information {information} about a peron I want you to create:
        1. A short summary
        2. two intresting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=['information'],
        template=summary_template,
    )

    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)

    chain = summary_prompt_template | llm
    linkedin_profile = "https://www.linkedin.com/in/maaz-khan-685982369/"
    scraped_profile = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile, mock=True)
    result = chain.invoke(
        input={"information": scraped_profile},
    )
    print(result.content)


if __name__ == "__main__":
    main()
