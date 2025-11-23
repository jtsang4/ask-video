import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from rich.console import Console


console = Console(force_terminal=True)


def start_chat(subtitle_content: str):
    """
    Starts a chat session based on the provided subtitle content.
    """

    # Initialize ChatOpenAI
    # Expects OPENAI_API_KEY to be set in environment
    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        model=os.getenv("OPENAI_MODEL_ID", "gpt-4o"),
        temperature=0.7,
    )

    # Create prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. You have been provided with the subtitles of a video. "
                "Answer the user's questions based on the video content. "
                "If the answer is not in the video, say so.\n\n"
                "Video Subtitles:\n{subtitles}",
            ),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )

    chain = prompt | llm | StrOutputParser()

    # History management
    store = {}

    def get_session_history(session_id: str):
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]

    with_message_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="history",
    )

    console.print(
        "[bold green]Chat session started! Type 'exit' or 'quit' to end.[/bold green]"
    )

    session_id = "user_session"

    while True:
        try:
            user_input = console.input("[bold blue]You:[/bold blue] ")
            if user_input.lower() in ["exit", "quit"]:
                break

            if not user_input.strip():
                continue

            console.print("[bold yellow]AI is thinking...[/bold yellow]")

            response_generator = with_message_history.stream(
                {"subtitles": subtitle_content, "question": user_input},
                config={"configurable": {"session_id": session_id}},
            )

            console.print("[bold green]AI:[/bold green]", end=" ")

            full_response = ""
            for chunk in response_generator:
                console.print(chunk, end="")
                full_response += chunk

            print()  # Add a newline after the full response
            print()  # Add another newline for spacing

        except KeyboardInterrupt:
            console.print("\n[bold red]Exiting...[/bold red]")
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
