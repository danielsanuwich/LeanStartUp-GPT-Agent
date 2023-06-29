import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain 
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper 
from langchain.llms import OpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent, Tool
from langchain.agents import load_tools
from langchain.agents import AgentType

serpapi_key = '41dfa06048fd6cb0ae8832930675efbd6a71babe12920ed982c5219a309f8fcf'
open_api_key = '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'

st.title("LeanStartupAgent")

#define company and project

job_to_be_done = st.text_input('Describe the core job to be done')
customer_description = st.text_input('Describe your customer segment')

clicked = st.button('Click me')

if clicked:
    st.write('Button clicked! Performing an operation...')
    # Place the code that should only execute after click here
    llm = OpenAI(openai_api_key=open_api_key, temperature=0.8)
    hardest_template = PromptTemplate(
      input_variables = ['customer_description','job_to_be_done'], 
      template='You are {customer_description}. What is the hardest part about {job_to_be_done}?')
    hardest_chain = LLMChain(llm=llm, prompt=hardest_template, verbose=True, output_key='hardest_part')
    hardest = hardest_chain.run(customer_description=customer_description, job_to_be_done=job_to_be_done)
    st.markdown('**Agent core painpoint =**')
    st.write(hardest)
    value_proposition_template = PromptTemplate(
      input_variables = ['hardest_part'], 
      template='Create a unique value proposition for a startup that solves the problem of {hardest_part}')
    value_proposition_chain = LLMChain(llm=llm, prompt=value_proposition_template, verbose=True, output_key='value_proposition')
    valueproposition = value_proposition_chain.run(hardest_part=hardest)
    st.markdown('**Agent Value proposition =**')
    st.write(valueproposition)
    canvas_template = PromptTemplate(
      input_variables = ['value_proposition'], 
      template='Provide the value proposition canvas for {value_proposition}. You should describe the following elements: customer jobs, custome pains, customer gains, products and services, pain relievers, gain creators')
    canvas_chain = LLMChain(llm=llm, prompt=canvas_template, verbose=True, output_key='canvas')
    canvas = canvas_chain.run(value_proposition=valueproposition)
    st.markdown('**Agent description of value proposition canvas =**')
    st.write(canvas)
    competitors_template = PromptTemplate(
      input_variables = ['value_proposition'], 
      template='Find three existing startup companies that have a description that is very similar to the following description: {value_proposition}. For each startup, provide company name, location and website.')
    competitors_chain = LLMChain(llm=llm, prompt=competitors_template, verbose=True, output_key='competitors')
    competitors = competitors_chain.run(value_proposition=valueproposition)
    st.markdown('**Agent identification of competitors =**')
    st.write(competitors)
    competitorsselect = competitors[2:]
    competitors_split1 = competitorsselect.split('\n')
    competitors_list = list()
    for competitor in competitors_split1:
      competitor_split = competitor.split(',')
      competitors_list.append(competitor_split[0][2:])
    competitors_list
    search = SerpAPIWrapper(serpapi_api_key = serpapi_key)
    search_tool = [Tool(
        name="Intermediate Answer",
        func=search.run,
        description="useful for when you need to ask with search")]
    self_ask_with_search = initialize_agent(search_tool, llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True)
    for i in range(len(competitors_list)):
      company = competitors_list[i]
      searchstring = "Provide company information for " + company + ". Include company description and founders"
      result = self_ask_with_search.run(searchstring)
      st.markdown('**Additional information competitor =**')
      st.write(result)
    hypotheses_template = PromptTemplate(
      input_variables = ['value_proposition', 'canvas'], 
      template='Generate a list of hypotheses for testing the following value proposition: {value_proposition}. You should rely on information from the value proposition canvas: {canvas}. Include at least 3 hypotheses. Each hypothesis should focus on the feasibility or viability of the business model. Here are some potential topics for hypotheses testing: willingness to pay, preferred distribution model, ultimate customer segmet, etc.')
    hypotheses_chain = LLMChain(llm=llm, prompt=hypotheses_template, verbose=True, output_key='hypotheses')
    hypotheses = hypotheses_chain.run(value_proposition=valueproposition, canvas=canvas)
    st.markdown('**Agent hypotheses =**')
    st.write(hypotheses)
else:
    st.write('Please click the button to perform an operation')














