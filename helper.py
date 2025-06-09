import os
from dotenv import load_dotenv
import logging
from datetime import datetime
from typing_extensions import TypedDict
from typing import Annotated
from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

class Helper:
    def __init__(self):
        print("Initializing requirements")
        self.tools = self.initialize_tools()
        self.llm = self.initialize_llm()
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.graph = self.initialize_graph()

    @staticmethod
    def initialize_tools() -> list:
        print("Inside initialize_tools")
        datetime_tool = Tool(
            name='datetime',
            description='A tool to get the current date and time in realtime.',
            func=lambda x: datetime.now()
        )
        duck_duck_tool = DuckDuckGoSearchRun()
        return [datetime_tool, duck_duck_tool]

    @staticmethod
    def initialize_llm():
        print("Inside initialize_llm")
        # llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', google_api_key=os.environ['GEMINI_API_KEY'])
        llm = ChatGroq(model='deepseek-r1-distill-llama-70b', temperature=0.7, api_key=os.environ['GROQ_API_KEY'])
        return llm

    def tool_calling_llm_as_node(self, state: State):
        print("Inside tool_calling_llm_as_node")
        return {'messages': [self.llm_with_tools.invoke(state['messages'])]}

    def initialize_graph(self):
        print("Inside initialize_graph")
        builder = StateGraph(State)

        builder.add_node('tool_calling_llm_as_node', self.tool_calling_llm_as_node)
        builder.add_node('tools', ToolNode(self.tools))

        builder.add_edge(START, 'tool_calling_llm_as_node')
        builder.add_conditional_edges('tool_calling_llm_as_node', tools_condition)
        builder.add_edge('tools', 'tool_calling_llm_as_node')

        graph = builder.compile()
        return graph

    def generate(self, query):
        print("Generating Answer")
        messages = self.graph.invoke({'messages': query})
        return messages['messages']

helper = Helper()