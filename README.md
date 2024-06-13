# custom_assistant2.0
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Custom_Assistant2.0 is an improved and enhanced version of the original custom assistant. With a newly implemented Graphical User Interface (GUI), this version utilizes the power of OpenAI and ElevenLabs to create a highly adaptable and customizable AI assistant that caters to your personal needs. 

## Getting Started

These instructions will help you get a copy of the project up and running on your local machine.

### Prerequisites

- Python >= 3.x
- OpenAI and ElevenLabs API keys. Visit [OpenAI](https://openai.com) and [ElevenLabs](https://beta.elevenlabs.io) to obtain these keys.

### Installation and Setup

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/micahkepe/custom_assistant2.0.git
   ```
2. Navigate to the project directory:
   ```
   cd custom_assistant2.0
   ```
   
3. Install the project's dependencies with:
  ```
  pip install -r requirements.txt
  ```

4. Add your OpenAI and ElevenLabs API keys to the `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   ```

5. Run `custom_assistant.py` to start the assistant:
   ```
   python custom_assistant.py
   ```
You'll be prompted when to ask your questions if speaking. The program can be ended by saying the instruction "That is all."

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
