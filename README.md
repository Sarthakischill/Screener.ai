# Job Screening AI

A multi-agent AI system for enhancing job screening with AI and data intelligence. This project was developed for the Accenture Hackathon.

## Features

- **Job Description Analysis**: Automatically reads and summarizes job descriptions, extracting key skills, qualifications, and responsibilities.
- **Candidate Matching**: Extracts data from CVs and matches candidates with job requirements.
- **Shortlisting**: Automatically shortlists candidates who meet or exceed a defined match threshold.
- **Interview Scheduling**: Generates personalized interview requests for shortlisted candidates.

## Architecture

- **Backend**: Python with FastAPI
- **Frontend**: React with Tailwind CSS
- **Database**: SQLite for data persistence
- **AI**: Ollama-based LLMs for text generation and analysis

## Multi-Agent System

The system uses a multi-agent architecture with specialized agents:

1. **Job Description Summarizer Agent**: Extracts key information from job descriptions.
2. **Recruiting Agent**: Processes candidate resumes and calculates match scores.
3. **Shortlisting Agent**: Identifies the best candidates based on match scores.
4. **Interview Scheduler Agent**: Generates personalized interview invitations.

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 14+
- Ollama (for local LLM access)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/job-screening-ai.git
   cd job-screening-ai
   ```

2. Install backend dependencies:
   ```
   cd backend
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```
   cd ../frontend
   npm install
   ```

4. Start Ollama:
   ```
   ollama run llama3
   ```

5. Import sample data:
   ```
   cd ..
   python import_data.py
   ```

6. Start the backend:
   ```
   python run.py
   ```

7. Start the frontend (in a separate terminal):
   ```
   cd frontend
   npm start
   ```

8. Open your browser to `http://localhost:3000`

## Usage

1. View job descriptions and candidates on the dashboard
2. Navigate to the Matching page
3. Select a job and click "Match All Candidates"
4. Review candidate matches and scores
5. Click "Shortlist Candidates" to automatically select the best matches
6. Click "Schedule Interviews" to generate interview invitations for shortlisted candidates

## Future Enhancements

- Integration with calendar systems for interview scheduling
- Email integration for sending interview invitations
- Advanced matching algorithms using vector embeddings
- Customizable matching criteria and weights 