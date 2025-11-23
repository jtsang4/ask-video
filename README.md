# Ask Video

A tool to chat with YouTube and Bilibili videos using AI.

## Features

- **Video Download**: Automatically fetches video from YouTube and Bilibili videos.
- **AI Chat**: Uses OpenAI (or compatible) models to answer questions based on the video content.
- **Streaming Output**: Responses are streamed in real-time for a better user experience.
- **Cross-Platform**: Works on macOS, Linux, and Windows.

## Usage

You can run this tool directly using `uvx` without installing it manually.

### Prerequisites

You need to have [uv](https://github.com/astral-sh/uv) installed.

### Running the Tool

1.  **Set your OpenAI API Key**:
    You need to provide your OpenAI API key. You can do this by setting an environment variable.

    ```bash
    export OPENAI_API_KEY=your_api_key_here
    ```

    If you are using a custom OpenAI-compatible provider (like DeepSeek, Moonshot, etc.), you can also set the base URL and model:

    ```bash
    export OPENAI_BASE_URL=https://api.example.com/v1
    export OPENAI_MODEL_ID=gpt-5-mini-2025-08-07
    ```

2.  **Run with `uvx`**:

    ```bash
    uvx ask-video <VIDEO_URL>
    ```

    Example:

    ```bash
    uvx ask-video https://www.youtube.com/watch?v=qjPH9njnaVU
    ```

## Development

To develop or contribute to this project:

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/jtsang4/ask-video.git
    cd ask-video
    ```

2.  **Install dependencies**:

    ```bash
    uv sync
    ```

3.  **Run locally**:
    ```bash
    uv run ask-video <URL>
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
