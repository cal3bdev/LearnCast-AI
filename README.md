# Learncast AI

## Project Overview

Inspiered by Google's NotebookLM, Learncast is a podcast generation application that leverages AI to create engaging and informative podcasts based on user-provided content. Users can input various types of sources, such as URLs, PDF files, or DOC files, and specify the style, analogy, and topic of emphasis for the podcast. The application generates a podcast script and converts it into audio format, ready for playback with intro and outro music. See sample generations in App/generated

## Features

- **AI-Powered Podcast Generation**: Utilizes OpenAI's API to generate conversational scripts.
- **Multiple Source Types**: Supports URLs, PDF files, and DOC files as input sources.
- **Customizable Output**: Users can specify the style, analogy, and emphasis for the podcast.
- **Background Music and Voice Settings**: Incorporates background music and customizable voice settings for different speakers.
- **Real-time Status Updates**: Users can check the status of their podcast generation in real-time.

## Technologies Used

- **FastAPI**: For building the backend API.
- **OpenAI API**: For generating podcast scripts.
- **Pydub**: For audio processing.
- **BeautifulSoup**: For web scraping content from URLs.
- **Streamlit**: For the user interface.
- **Python**: The primary programming language.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/cal3bdev/LearnCast-AI.git
   
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```plaintext
   OPENAI_API_KEY=your_openai_api_key
   ```

5. **Run the FastAPI server**:
   ```bash
   python main.py
   ```

6. **Run the Streamlit UI**:
   In a new terminal, run:
   ```bash
   streamlit run ui.py
   ```

## Usage

1. Open your web browser and navigate to `http://localhost:8501` to access the Streamlit interface.
2. Fill in the required fields:
   - **Source Type**: Select the type of source (URL, PDF, or DOC).
   - **Source**: Enter the URL or file path.
   - **Analogy**: Provide an analogy to guide the podcast generation.
   - **Emphasis**: Specify the emphasis for the podcast.
   - **Style**: Choose the style of the podcast (entertaining, informative, academic, funny).
3. Click the "Generate" button to start the podcast generation process.
4. Wait for the podcast to be generated. The status will be updated in real-time.
5. Once completed, the podcast will be available for playback in the audio player.

## API Endpoints

### Generate Podcast

- **Endpoint**: `POST /generate_podcast`
- **Request Body**:
  ```json
  {
      "source_type": "url", // or "pdf", "doc"
      "source": "http://example.com",
      "analogy": "an analogy",
      "emphasis": "important points",
      "style": "entertaining"
  }
  ```
- **Response**:
  ```json
  {
      "podcast_id": "unique_podcast_id"
  }
  ```

### Get Podcast Status

- **Endpoint**: `GET /podcast_status/{podcast_id}`
- **Response**:
  ```json
  {
      "id": "unique_podcast_id",
      "status": "pending | completed | failed",
      "podcast_url": "http://example.com/podcast.mp3" // only if completed
  }
  ```

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.



## Contact

For any inquiries, please contact [lwangacalebb@gmail.com].
