import os

import chainlit as cl
from chainlit.input_widget import *
from langchain.schema.runnable import Runnable, RunnableConfig

# Mercury.Hermes frontend lib imports
from mercury.core.modules.hermes.chains import assistant_chat, document_chat
from mercury.core.modules.hermes.postprocessing import PostMessageHandler

# Document storage path global variable
DOCUMENT_STORAGE_PATH = "./app/data/"


# ------------------------ ChainLit Callbacks Start ------------------------ #
@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="AI Assistant",  # can have images
            markdown_description="Chat with Hermes.",
            icon="/public/hermes.png",
        ),
        cl.ChatProfile(
            name="Documents",  # can have images
            markdown_description="Ask Hermes questions about the uploaded documents.",
            icon="/public/docs.svg",
        ),
    ]


@cl.on_chat_start
async def on_chat_start() -> None:
    """
    This function is called when a chat starts.

    Returns:
        None
    """

    # Set the avatar for the chat
    await cl.Avatar(
        name="Hermes",
        path="./public/hermes.png",
    ).send()

    # Get the chat profile
    chat_profile = cl.user_session.get("chat_profile")

    # Modify behaviour based on chat profile
    if chat_profile == "Documents":
        await document_chat()
    elif chat_profile == "AI Assistant":
        await assistant_chat()


@cl.on_message
async def on_message(message: cl.Message) -> None:
    """
    Callback function that is called when a message is received.

    Args:
        message (cl.Message): The message object containing the received message.

    Returns:
        None
    """
    runnable = cl.user_session.get("runnable")  # type: Runnable
    msg = cl.Message(content="")

    async with cl.Step(type="run", name="Assistant"):
        async for chunk in runnable.astream(
            message.content,
            config=RunnableConfig(
                callbacks=[
                    cl.LangchainCallbackHandler(stream_final_answer=True),
                    PostMessageHandler(msg),
                ]
            ),
        ):
            await msg.stream_token(chunk)

    await msg.send()


@cl.on_chat_end
async def on_chat_end() -> None:
    """
    This function is called when a chat ends.

    It clears the runnable session from the user session.

    Returns:
        None
    """

    # Delete contents of directory
    for file_name in os.listdir(DOCUMENT_STORAGE_PATH):
        file_path = os.path.join(DOCUMENT_STORAGE_PATH, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)


@cl.on_logout
async def on_logout() -> None:
    """
    This function is called when a user logs out.

    It clears the runnable session from the user session.

    Returns:
        None
    """

    # Delete contents of directory
    for file_name in os.listdir(DOCUMENT_STORAGE_PATH):
        file_path = os.path.join(DOCUMENT_STORAGE_PATH, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)


@cl.on_chat_resume
async def on_chat_resume() -> None:
    """
    This function is called when a chat is resumed.

    Returns:
        None
    """
    pass


# ------------------------ ChainLit Callbacks End ------------------------ #
