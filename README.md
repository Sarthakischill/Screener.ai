# TalentMatch AI

A multi-agent AI system for intelligent candidate screening and job matching. This project was developed for the Accenture Hackathon, helping recruiters streamline the hiring process through AI-powered analysis and matching.

## Features

- **Job Description Analysis**: Automatically reads and summarizes job descriptions, extracting key skills, qualifications, and responsibilities.
- **Candidate Matching**: Analyzes candidate resumes and matches them with job requirements for optimal fit.
- **Shortlisting**: Intelligently shortlists candidates who meet or exceed defined match thresholds.
- **Interview Scheduling**: Generates personalized interview requests with suggested dates for shortlisted candidates.

## Architecture

- **Backend**: Python with FastAPI
- **Frontend**: React with Tailwind CSS (Bricolage Grotesque for headings, Montserrat for body text)
- **Database**: SQLite for data persistence
- **AI**: Google's Gemini API for intelligent text processing and analysis

## Multi-Agent System

The system uses a specialized multi-agent architecture with dedicated agents:

1. **Job Description Summarizer Agent**: Extracts and analyzes key information from job descriptions.
2. **Recruiting Agent**: Processes candidate resumes and calculates match scores based on job requirements.
3. **Shortlisting Agent**: Identifies the best candidates based on comprehensive match analysis.
4. **Interview Scheduler Agent**: Creates personalized interview invitations with suggested meeting times.

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 14+
- Google Gemini API key

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/talentmatch-ai.git
   cd talentmatch-ai
   ```

2. Create a `.env` file in the root directory with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

3. Install backend dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Install frontend dependencies:
   ```
   cd frontend
   npm install
   cd ..
   ```

5. Import sample data:
   ```
   python import_data.py
   ```

6. Start the application:
   ```
   bash start.sh
   ```
   
   This will start both the backend and frontend services.

7. Open your browser to `http://localhost:3000`

## Usage

1. Dashboard - View key statistics and navigate to other sections
2. Jobs - Browse and manage job descriptions
3. Candidates - View all candidates in the system
4. Matching - The core of the application:
   - Select a job and click "Match All Candidates"
   - Review candidate matches and their scores
   - Click "Shortlist Candidates" to automatically select the best matches
   - Click "Schedule Interviews" to generate personalized interview invitations

## API Rate Limits

The application uses Google's Gemini API which has rate limits. If you encounter errors during heavy usage, this may be due to API rate limiting. Consider:

- Spacing out operations
- Using the system with smaller batches of candidates/jobs
- Upgrading to a higher tier API plan for production use

## Future Enhancements

- Integration with calendar systems for automatic interview scheduling
- Email integration for sending interview invitations
- Advanced matching algorithms using vector embeddings
- Customizable matching criteria and weights 