from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup import linkedin_lookup
from output_parser import summary_output_parser


load_dotenv()


def main():
    print("Hello from Capstone-01!")

    summary_template = """
        given the linkedin information {information} about a peron I want you to create:
        1. A short summary
        2. two intresting facts about them

        \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=['information'],
        template=summary_template,
        partial_variables={"format_instructions": summary_output_parser.get_format_instructions()},
    )

    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)

    chain = summary_prompt_template | llm | summary_output_parser
    linkedin_profile = linkedin_lookup(name="Mohammad Maaz Khan")
    scraped_profile = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile, mock=False)
    result = chain.invoke(
        input={"information": scraped_profile},
    )
    summary = result.summary
    facts = result.facts
    print(f"SUMMARY:\n{summary}\n\nFACTS:\n{facts}")

 
if __name__ == "__main__":
    main()
