# Chiara - Language Learning Assistant

Chiara is an intelligent language learning platform that uses AI to provide personalized learning experiences. The application adapts to each user's learning pace by dynamically adjusting word difficulty based on their performance.

## Features

-   **Dialogue Mode**: Engages users in interactive conversations simulating real-life conversations
-   **AI-Powered Translation Evaluation**: Utilizes the newest LLMs to evaluate user translations and give them ratings
-   **Dynamic Difficulty Adjustment**: Automatically adjusts word difficulty based on user performance
-   **Flashcard Learning Mode**: Interactive flashcard system for vocabulary practice

## Setup

1. Clone the repository

2. Run the setup script:

```bash
./utils/setup.sh
```

3. Set up environment variables:

-   Create a `.env` file in the root directory
-   Copy `.env.example` to `.env`
-   Configure the following variables:
    -   `GEMINI_API_KEY`: Your Google Gemini API key
    -   `DEEPSEEK_API_KEY`: Your DeepSeek API key
    -   `MONGODB_URI`: Your MongoDB connection string

4. Run the application:

```bash
python3 run.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
