from langflow.base.io.chat import ChatComponent
from langflow.field_typing import Text
from langflow.schema.message import Message
from langflow.template import Input, Output


class ChatInput(ChatComponent):
    display_name = "Chat Input"
    description = "Get chat inputs from the Playground."
    icon = "ChatInput"

    inputs = [
        Input(
            name="input_value",
            type=str,
            display_name="Text",
            multiline=True,
            input_types=[],
            info="Message to be passed as input.",
        ),
        Input(
            name="sender",
            type=str,
            display_name="Sender Type",
            options=["Machine", "User"],
            value="User",
            info="Type of sender.",
            advanced=True,
        ),
        Input(name="sender_name", type=str, display_name="Sender Name", info="Name of the sender.", value="User"),
        Input(
            name="session_id", type=str, display_name="Session ID", info="Session ID for the message.", advanced=True
        ),
    ]
    outputs = [
        Output(display_name="Message", name="message", method="text_response"),
        Output(display_name="Record", name="record", method="message_response"),
    ]

    def text_response(self) -> Text:
        result = self.input_value
        if self.session_id and isinstance(result, (Message, str)):
            self.store_message(result, self.session_id, self.sender, self.sender_name)
        return result

    def message_response(self) -> Message:
        message = Message(
            text=self.input_value,
            sender=self.sender,
            sender_name=self.sender_name,
            session_id=self.session_id,
        )
        if self.session_id and isinstance(message, (Message, str)):
            self.store_message(message)
        self.status = message
        return message
