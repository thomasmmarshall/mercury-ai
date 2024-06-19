from typing import Any, List

import chainlit as cl
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import Document


class PostMessageHandler(BaseCallbackHandler):
    """
    A callback handler for processing messages and extracting unique source-page pairs.

    Args:
        msg (cl.Message): The message object to be processed.

    Attributes:
        msg (cl.Message): The message object to be processed.
        sources (set): A set to store unique source-page pairs.

    """

    def __init__(self, msg: cl.Message):
        BaseCallbackHandler.__init__(self)
        self.msg = msg
        self.sources = set()  # To store unique pairs

    def on_retriever_end(
        self,
        documents: List[Document],
        *,
        run_id: str,
        parent_run_id: str,
        **kwargs: Any,
    ) -> None:
        """
        Callback method called when the retriever process ends.

        Args:
            documents (list): List of retrieved documents.
            run_id: The ID of the current run.
            parent_run_id: The ID of the parent run.
            **kwargs: Additional keyword arguments.

        """
        for d in documents:
            source_page_pair = (
                d.metadata["source"],  # path
                d.metadata["source"].split("\\")[-1],  # source name
                d.metadata["page"],  # page number
            )
            self.sources.add(source_page_pair)  # Add unique pairs to the set

    def on_llm_end(
        self, response: Any, *, run_id: str, parent_run_id: str, **kwargs: Any
    ) -> None:
        """
        Callback method called when the LLM (Language Model) process ends.

        Args:
            response: The response from the LLM process.
            run_id: The ID of the current run.
            parent_run_id: The ID of the parent run.
            **kwargs: Additional keyword arguments.

        """
        if len(self.sources):
            sources_text = "\n".join(
                [f"{source}, page {page}" for path, source, page in self.sources]
            )
            self.msg.content += "\n\n**Sources:**\n" + sources_text

            # PDF Displays
            for path, source, page in self.sources:
                self.msg.elements.append(
                    cl.Pdf(
                        name=f"{source}, page {page}",
                        display="side",
                        path=path,
                        page=int(page),
                    )
                )
