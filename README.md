# MedVoiceFille

A web-based application for automating medical data entry and management through speech recognition and AI-powered text analysis. The system helps medical professionals efficiently process and store patient information.

## Features

- 🎤 **Voice Input**: Record and transcribe medical information using state-of-the-art speech recognition
- 📝 **Text Analysis**: AI-powered extraction of structured medical data from free text
- 📄 **Document Generation**: Automatic generation of standardized medical forms (Form 025/o)
- 💾 **Data Storage**: Save patient data in both JSON and DOCX formats
- 🔄 **Real-time Processing**: Instant processing and visualization of patient information
- 🌐 **Web Interface**: User-friendly interface built with Gradio

## Prerequisites

- Python 3.8 or higher
- Google Cloud API key (for Gemini API)
- 4GB+ RAM recommended
- Internet connection for API services

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/medical-data-automation.git
cd medical-data-automation
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:7860
```

3. Use the interface to:
   - Record voice input for patient information
   - Process text data
   - Generate and download medical documents
   - Save patient records

## Project Structure

```
├── patient_data_docx\
|   └── Іван_Іванов_Іванович.docx            # Save data in docx format with add template
├── patient_data_json\
|   └── patient_Iванов_Іван_2025012952.json  # Save data in json format
├── saved_audio\
|   └── audio.ogg            # Audio to receive text
├── app.py                  # Main application file
├── app_function.py         # Core application functions
├── audio_to_text.py        # Audio processing module
├── document_import.py      # Document generation module
├── text_analyze.py         # Text analysis using Gemini API
├── f025-o.docx            # Document template
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation
```

## Data Processing Flow

1. **Voice Input** → Audio file is saved and processed using Whisper model
2. **Text Analysis** → Processed text is analyzed using Google's Gemini API
3. **Data Extraction** → Structured patient data is extracted from the analysis
4. **Document Generation** → Data is used to fill medical form template
5. **Data Storage** → Information is saved in both JSON and DOCX formats

## Features in Detail

### Voice Recording
- Supports multiple audio formats
- Real-time transcription using Whisper model
- Automatic noise reduction and audio processing

### Text Analysis
- AI-powered medical information extraction
- Recognition of key patient data points
- Structured data output in JSON format

### Document Generation
- Automated filling of Form 025/o
- Support for Ukrainian medical documentation standards
- Professional document formatting

### Data Storage
- Dual format storage (JSON & DOCX)
- Organized file naming system
- Easy data retrieval system

## Security Notes

- Keep your API keys secure
- Don't commit `.env` file to version control
- Ensure patient data privacy compliance
- Regularly update dependencies for security patches

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for the Whisper model
- Google for the Gemini API
- Gradio team for the web interface framework
- Contributors and testers

## Contact

Your Name - youremail@example.com
Project Link: https://github.com/yourusername/medical-data-automation
