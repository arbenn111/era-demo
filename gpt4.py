import openai 
from ToolGPT import ChatGPTWithFunctions
import inspect
import re
import streamlit as st
import streamlit_chat as chat
openai.api_key = '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'
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import streamlit.components.v1 as components
import base64

info_to_learn="""
Our bank offers these loan 
1. Personal loan
2. Home Loan
3. Mortgage Loan
4. Overdraft
5. Credit Card

--Personal Loan have annual interest rate 7%  for each amount the user requires, max periods for 10 years 
--If a period of time greater than 10 years is requested, we must inform you that we cannot provide personal loans longer than this period and suggest other types of loans with longer periods.
--if the client asks about the monthly installment ,you must ensure that he has given the amount and duration of the loan, calculate with PMT formula.
"""
emo_learn="""
- we are dealing with a client who does not understand the financial side, so the answers must be clear and understandable, which fit the client's direct question
-we need to give the customer positive energy and offer it to the bank
- answers should be short and clear" blow i will ask you
-the bot should calculate the monthly interest if it has the parameters on the contrary, I should ask the user for the parameter and then calculate it
-this is a conversation between the client and the chatbot, and the answers should be short without formulas and should be very human in response
-if the client says thank you, you can ask for a feedback or comment about the service
"""
info_1="""
can you extract the loan amount, the loan period and the installment in table only number form from the sentence above
"""

def parse_docstring(function):
    """
    Parse the docstring of a function to extract function name, description and parameters.
    
    Parameters
    ----------
    function : Callable
        The function whose docstring is to be parsed.

    Returns
    -------
    dict
        A dictionary with the function's name, description, and parameters.
    """
    doc = inspect.getdoc(function)

    # Find function description
    function_description = re.search(r'(.*?)Parameters', doc, re.DOTALL).group(1).strip()

    # Find parameter descriptions
    parameters_description = re.findall(r'(\w+)\s*:\s*(\w+)\n(.*?)(?=\n\w+\s*:\s*|\nReturns|$)', doc, re.DOTALL)

    # Get the parameters from the function signature
    signature_params = list(inspect.signature(function).parameters.keys())

    # Construct the parameters dictionary
    properties = {}
    required = []
    for name, type, description in parameters_description:
        name = name.strip()
        type = type.strip()
        description = description.strip()

        required.append(name)
        properties[name] = {
            "type": type,
            "description": description,
        }

    # Check if the number of parameters match
    if len(signature_params) != len(required):
        raise ValueError(f"Number of parameters in function signature ({len(signature_params)}) does not match the number of parameters in docstring ({len(required)})")

    # Check if each parameter in the signature has a docstring
    for param in signature_params:
        if param not in required:
            raise ValueError(f"Parameter '{param}' in function signature is missing in the docstring")

    parameters = {
        "type": "object",
        "properties": properties,
        "required": required,
    }

    # Construct the function dictionary
    function_dict = {
        "name": function.__name__,
        "description": function_description,
        "parameters": parameters,
    }

    return function_dict
def add(principal, annual_interest_rate,loan_term_years):
    """
    Adds Three Numbers

    Parameters
    ----------
    principal : integer
        number to be added
    annual_interest_rate : integer
        number to be added
    loan_term_years : integer
        number to be added

    Returns
    -------
    integer
        monthly_installment
    """
    monthly_interest_rate = annual_interest_rate / 12
    loan_term_months = loan_term_years * 12
    monthly_installment = (principal * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -loan_term_months)
    return monthly_installment
def fun_dict(functions):
    fn_names_dict = {}
    for fn in functions:
        fn_names_dict[fn.__name__] = fn
    function_dicts = [parse_docstring(fun) for fun in functions]
    return function_dicts

st.markdown("""
    <style>
        .title {
            text-align: center;
            top: 0;
            font-size: 3em;
            font-weight: bold;
        }
        #e {
            color: #0262F7;
        }
        #r {
            color: #AD173A;
        }
        #a {
            color: #9F95CA;
        }
    </style>
    <div class="title">
        <span id="e">E</span><span id="r">R</span><span id="a">A</span>
    </div>
    """, unsafe_allow_html=True)
#st.sidebar.title('I Listen')
#st.sidebar.markdown('<p style="text-align: center;"><strong>I Listen</strong></p>', unsafe_allow_html=True)
st.sidebar.markdown('<p style="text-align: center; font-size: 40px; font-weight: bold;">I Listen</p>', unsafe_allow_html=True)


emoji_list = ['😢','😟', '😐', '🙂', '🤩']
columns = st.sidebar.columns(len(emoji_list))
selected_emoji = None

# Placing each emoji in its own column as a button
for i, emoji in enumerate(emoji_list):
    if columns[i].button(emoji):
        selected_emoji = emoji


user_comment = st.sidebar.text_area("Type your comment here...")
if st.sidebar.button('Submit'):
    st.sidebar.markdown(
    '<div style="color: black; background-color: #6ea7ff;font-weight: bold; padding: 10px; border-radius: 5px;">Thanks for your feedback!</div>',
    unsafe_allow_html=True,
)
    
def pffff(prompt):
    chat = ChatOpenAI(model_name="gpt-4-0613", 
                  temperature=0.7, 
                  max_tokens=3500,
                  openai_api_key='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'
                  )
    messages = [
        SystemMessage(content="You are a helpful bank assistant."),
        HumanMessage(content=prompt)
    ]
    response=chat(messages)
    return response.content
#user_input="hello era"
#history=''
def chat_with_history(history, user_input,info_to_learn,emo_learn):
    # Combine history with user input
    prompt = f"base info: {info_to_learn}\n {history} User: {user_input}\nBot:"
    
    # Get bot response
    try:
        bot_response = pffff(prompt)
    except:
        bot_response = pffff(prompt)
    #bot_response = pffff(prompt)
    # Update history
    updated_history = f"{history}User: {user_input}\nBot: {bot_response}\n Importent: {emo_learn}"
    
    return updated_history, bot_response

background_url= open(r"C:\Users\User\Downloads\ERA.jpg", 'rb').read()  # fc aka file_content
background_encode = base64.b64encode(background_url).decode('utf-8')
era_png="data:image/jpeg;base64,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"
user_img= "https://www.socialsamosa.com/static/images/svg%20icons/user-avatar.svg"
era_url= open(r"C:\Users\User\Downloads\ERA_me sfond te paster.png", 'rb').read()  # fc aka file_content
era_encode = base64.b64encode(era_url).decode('utf-8')
page_bg_img = f"""
            <style>
            [data-testid="stAppViewContainer"]{{
            width: 100%;
            height: 100%;
            background-size: cover;
            background-position: center center;
            background-repeat: repeat;
           /* background-color: #FEE600;*/
            background-image: url(data:image/png;base64,{background_encode});
            }}
            </style>
        """
st.markdown(
   f"""
    <style>
        [data-testid="stSidebar"]{{
            background-color: transparent !important;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(page_bg_img,unsafe_allow_html=True)
# avatars = {
#     "user": "👤",  # Here you can replace with URL of user avatar or HTML/CSS styling
#     "assistant": "🤖"  # Here you can replace with URL of assistant avatar or HTML/CSS styling
# }
st.markdown(
    """
    <style>
        .stChatFloatingInputContainer {
            background-color: transparent !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
def display_messages():
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "Hello I'm Era, how can I help you?","avatar": era_png}]
    for message in st.session_state.messages:
        role = message.get("role")  # Extract role from message
        content = message.get("content")  # Extract content from message
        if role == "user":
            with st.chat_message(role):
                st.write(content)
        elif role == "assistant":
            with st.chat_message(role,avatar=message["avatar"]):
                st.write(content)
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant",avatar=message["avatar"]):
            with st.spinner("Thinking..."):
                if "history" not in st.session_state:
                    st.session_state["history"] = ""
                st.session_state["history"], bot_response = chat_with_history(st.session_state["history"], prompt, info_to_learn, emo_learn)
                st.write(bot_response) 
        message = {"role": "assistant", "content": bot_response,"avatar": era_png}
        st.session_state.messages.append(message)
    #st.subheader("Chat")
    #for message in st.session_state.messages:
    #    with st.chat_message(message["role"]):
    #        st.write(message["content"])

# def display_messages():
#     if "messages" not in st.session_state:
#         st.session_state["messages"] = []
#     st.subheader("Chat")
#     for i, (msg, is_user) in enumerate(st.session_state["messages"]):
#         chat.message(msg, is_user=is_user, key=str(i))
#     st.session_state["thinking_spinner"] = st.empty()

# def process_input():
#     user_text = st.session_state["user_input"].strip()
#     if user_text:
#         with st.spinner("Thinking..."):
#             if "history" not in st.session_state:
#                 st.session_state["history"] = ""
#             st.session_state["history"], bot_response = chat_with_history(st.session_state["history"], user_text, info_to_learn, emo_learn)
#         st.session_state["messages"].append((user_text, True))
#         st.session_state["messages"].append((bot_response, False))
#         # Clear the input box after processing the input
#         st.session_state["user_input"] = ""



# Initialize session state variables if not already present
# if "user_input" not in st.session_state:
#     st.session_state["user_input"] = ""

display_messages()
#display_messages()
#st.text_input("Message", key="user_input", on_change=process_input)



st.divider()

# if "messages" not in st.session_state:
#     st.session_state["messages"] = []
# if "history" not in st.session_state:
#     st.session_state["history"] = []

# display_messages()

# st.text_input("Message", key="user_input", on_change=process_input, args=(st.session_state["history"] ,))

# st.divider()
    
    #user_input=st.text_input("Message")
    #st.write(st.session_state.history)
    #st.session_state.history, bot_response = chat_with_history(st.session_state.history, user_input,info_to_learn,emo_learn)
    #with st.chat_message("user"):
    #    st.write(user_input)
    #with st.chat_message("assistant"):
    #    st.write(bot_response)
    


# if __name__ == "__main__":
#     main()



# def process_input(history):
#     if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
#         user_text = st.session_state["user_input"].strip()
#         with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
#             history, query_text = chat_with_history(history, user_text,info_to_learn,emo_learn)
#         st.session_state["messages"].append((user_text, True))
#         st.session_state["messages"].append((query_text, False))



# history=''
# while True:
#    user_input = input("You: ")
#    if user_input.lower() in ["quit", "exit"]:
#        break
#    history, bot_response = chat_with_history(history, user_input,info_to_learn,emo_learn)
#    print("Era:", bot_response)
