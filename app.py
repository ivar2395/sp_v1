import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun

st.set_page_config(page_title="Supreme Packs B2B Lead Gen AI", page_icon="📦")

st.title("📦 Supreme Packs B2B Lead Gen AI")
st.write("Automate your B2B lead generation and outreach email drafting.")

api_key = st.sidebar.text_input("OpenAI API Key", type="password")

industry = st.text_input("Target Industry (e.g., FMCG, Pharmaceuticals)")
location = st.text_input("Target Location (e.g., Coimbatore, Tamil Nadu)")

if st.button("Generate Leads and Outreach Emails"):
    if not api_key:
        st.error("Please provide an OpenAI API Key in the sidebar.")
    elif not industry or not location:
        st.error("Please provide both Target Industry and Target Location.")
    else:
        with st.spinner("Searching for leads and drafting emails..."):

            try:
                # Initialize search tool
                search = DuckDuckGoSearchRun()

                # Step 1: Search for companies
                search_query = f"top {industry} companies in {location}"
                search_results = search.invoke(search_query)

                st.subheader("🔍 Search Results (Raw)")
                st.write(search_results)

                # Step 2: Extract leads and generate emails
                llm = ChatOpenAI(model_name="gpt-4", temperature=0.7, api_key=api_key)

                prompt = PromptTemplate(
                    input_variables=["search_results", "industry", "location"],
                    template="""
                    You are a highly skilled B2B Sales Executive for 'Supreme Packs'.
                    Supreme Packs (supremepacks.in) manufactures high-quality Corrugated Boxes, BOPP Bags, and Pouch Packages.

                    Based on the following search results for {industry} companies in {location}:
                    {search_results}

                    Identify up to 3 potential company leads from the search results.
                    For EACH company, write a personalized B2B outreach email.

                    The email should:
                    1. Have a catchy subject line.
                    2. Briefly mention their company and industry.
                    3. Introduce Supreme Packs and how our Corrugated Boxes, BOPP Bags, or Pouch Packages can solve their packaging needs.
                    4. Include a clear call to action (e.g., scheduling a quick call).

                    Format the output clearly, separating each company's lead info and email.
                    """
                )

                chain = prompt | llm
                output = chain.invoke({
                    "search_results": search_results,
                    "industry": industry,
                    "location": location
                })

                st.subheader("✉️ Generated Outreach Emails")
                st.markdown(output.content)
            except Exception as e:
                st.error(f"An error occurred: {e}")
