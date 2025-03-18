# Resume Analyzer AI

A web application that analyzes resumes against job descriptions using Google's Gemini AI to provide detailed feedback and match scores.

![git](https://github.com/user-attachments/assets/278068d7-ebf2-49e2-8dba-42975739c21c)

## Features

- **Resume Analysis**: Get comprehensive feedback on your resume's strengths and weaknesses
- **Match Scoring**: Calculate how well your resume matches specific job descriptions
- **Detailed Recommendations**: Receive actionable suggestions to improve your resume
- **Modern UI**: Clean, responsive interface with a professional dark theme
- **Easy to Use**: Simple upload-and-analyze workflow

## How It Works

1. Upload your resume as a PDF
2. Paste the job description you're applying for
3. Choose between full analysis or match scoring
4. Get instant AI-powered feedback

## Technologies Used

- Streamlit for the web interface
- OpenAI gpt-4-turbo for analysis
- PDF2Image for PDF processing
- Custom CSS for enhanced UI

## Installation & Setup

### Prerequisites
- Python 3.10
- OPENAI API Key

### Local Development
1. Clone the repository:
   ```
   git clone https://github.com/iamshubhp/Resume-Review.git
   cd Resume-Review
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_gemini_api_key_here
   ```

4. Run the application:
   ```
   streamlit run app.py
   ```

## Deployment

This app can be deployed on Railway, Streamlit Cloud, or other Python-supporting platforms.

For Railway deployment:
1. Create a Procfile with: `web: streamlit run app.py`
2. Set up your OPENAI_API_KEY in Railway's environment variables
3. Deploy from your GitHub repository

## Future Enhancements

- Multi-page resume support
- Custom analysis for different industries
- Resume templates and suggestions
- Comparison against multiple job descriptions
- Export results as PDF

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Streamlit and OPENAI
- I got inspired to build this web app by the challenges of modern job applications

## Contributions are Excepted thankyou!
