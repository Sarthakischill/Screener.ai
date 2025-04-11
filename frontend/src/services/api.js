import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ===== Job Descriptions API =====
export const getJobDescriptions = async () => {
  const response = await api.get('/job-descriptions/');
  return response.data;
};

export const getJobDescription = async (id) => {
  const response = await api.get(`/job-descriptions/${id}`);
  return response.data;
};

export const createJobDescription = async (jobData) => {
  const response = await api.post('/job-descriptions/', jobData);
  return response.data;
};

// ===== Candidates API =====
export const getCandidates = async () => {
  const response = await api.get('/candidates/');
  return response.data;
};

export const getCandidate = async (id) => {
  const response = await api.get(`/candidates/${id}`);
  return response.data;
};

export const createCandidate = async (candidateData) => {
  const response = await api.post('/candidates/', candidateData);
  return response.data;
};

export const uploadResume = async (name, email, file) => {
  const formData = new FormData();
  formData.append('name', name);
  formData.append('email', email);
  formData.append('resume', file);
  
  const response = await api.post('/candidates/upload-resume', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

// ===== Matching API =====
export const matchCandidateToJob = async (jobId, candidateId) => {
  const response = await api.post(`/matching/match-candidate/${jobId}/${candidateId}`);
  return response.data;
};

export const matchAllCandidates = async (jobId) => {
  const response = await api.post(`/matching/match-all/${jobId}`);
  return response.data;
};

export const getJobWithCandidates = async (jobId) => {
  const response = await api.get(`/matching/job/${jobId}/candidates`);
  return response.data;
};

export const shortlistCandidates = async (jobId) => {
  const response = await api.post(`/matching/shortlist/job/${jobId}`);
  return response.data;
};

export const scheduleInterviews = async (jobId, companyName) => {
  const response = await api.post(`/matching/schedule-interviews/job/${jobId}`, { company_name: companyName });
  return response.data;
};

// ===== Stats API =====
export const getShortlistedCount = async () => {
  const response = await api.get('/matching/stats/shortlisted');
  return response.data.count;
};

export const getInterviewsCount = async () => {
  const response = await api.get('/matching/stats/interviews');
  return response.data.count;
}; 