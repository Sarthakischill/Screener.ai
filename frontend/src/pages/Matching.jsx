import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/Card';
import Button from '../components/Button';
import { 
  getJobDescriptions, 
  getJobWithCandidates, 
  matchAllCandidates, 
  shortlistCandidates,
  scheduleInterviews 
} from '../services/api';
import { 
  ChevronDownIcon, 
  ChevronUpIcon, 
  CheckCircleIcon,
  EnvelopeIcon,
  UserCircleIcon,
  BriefcaseIcon
} from '@heroicons/react/24/outline';

export default function Matching() {
  const navigate = useNavigate();
  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [matchLoading, setMatchLoading] = useState(false);
  const [shortlistLoading, setShortlistLoading] = useState(false);
  const [interviewLoading, setInterviewLoading] = useState(false);
  const [error, setError] = useState(null);
  const [expandedInterviews, setExpandedInterviews] = useState({});

  // Fetch jobs on component mount
  useEffect(() => {
    async function fetchJobs() {
      try {
        setLoading(true);
        const data = await getJobDescriptions();
        setJobs(data);
        if (data.length > 0) {
          // Auto-select the first job
          handleJobSelect(data[0].id);
        } else {
          setLoading(false);
        }
      } catch (err) {
        console.error('Error fetching jobs:', err);
        setError('Failed to load job descriptions');
        setLoading(false);
      }
    }

    fetchJobs();
  }, []);

  // Handle job selection
  const handleJobSelect = async (jobId) => {
    try {
      setLoading(true);
      setSelectedJob(jobId);
      
      // Fetch the job with its candidates
      const jobData = await getJobWithCandidates(jobId);
      
      // Update the candidates state
      setCandidates(jobData.candidates || []);
    } catch (err) {
      console.error('Error fetching job with candidates:', err);
      setError('Failed to load candidates for this job');
    } finally {
      setLoading(false);
    }
  };

  // Match all candidates to selected job
  const handleMatchAll = async () => {
    if (!selectedJob) return;
    
    try {
      setMatchLoading(true);
      await matchAllCandidates(selectedJob);
      
      // Reload candidates for this job
      const jobData = await getJobWithCandidates(selectedJob);
      setCandidates(jobData.candidates || []);
      
      // Success toast or notification could be added here
    } catch (err) {
      console.error('Error matching candidates:', err);
      setError('Failed to match candidates to this job');
    } finally {
      setMatchLoading(false);
    }
  };

  // Shortlist candidates for selected job
  const handleShortlist = async () => {
    if (!selectedJob) return;
    
    try {
      setShortlistLoading(true);
      await shortlistCandidates(selectedJob);
      
      // Reload candidates for this job
      const jobData = await getJobWithCandidates(selectedJob);
      setCandidates(jobData.candidates || []);
      
      // Success toast or notification could be added here
    } catch (err) {
      console.error('Error shortlisting candidates:', err);
      setError('Failed to shortlist candidates');
    } finally {
      setShortlistLoading(false);
    }
  };

  // Schedule interviews for shortlisted candidates
  const handleScheduleInterviews = async () => {
    if (!selectedJob) return;
    
    try {
      setInterviewLoading(true);
      const selectedJobData = jobs.find(job => job.id === selectedJob);
      const companyName = selectedJobData ? selectedJobData.company : 'Acme Corp';
      
      await scheduleInterviews(selectedJob, companyName);
      
      // Reload candidates for this job
      const jobData = await getJobWithCandidates(selectedJob);
      setCandidates(jobData.candidates || []);
      
      // Success toast or notification could be added here
    } catch (err) {
      console.error('Error scheduling interviews:', err);
      setError('Failed to schedule interviews');
    } finally {
      setInterviewLoading(false);
    }
  };

  // Toggle interview email expansion
  const toggleInterviewExpand = (candidateId) => {
    setExpandedInterviews(prev => ({
      ...prev,
      [candidateId]: !prev[candidateId]
    }));
  };

  if (loading && jobs.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 p-4 rounded-md">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">Error</h3>
            <div className="mt-2 text-sm text-red-700">
              <p>{error}</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (jobs.length === 0) {
    return (
      <div className="text-center py-12">
        <BriefcaseIcon className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-medium text-gray-900">No job descriptions</h3>
        <p className="mt-1 text-sm text-gray-500">You need to add job descriptions before matching candidates.</p>
        <div className="mt-6">
          <Button onClick={() => navigate('/jobs/new')}>
            Add Job Description
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="pb-5 border-b border-gray-200 mb-5">
        <h1 className="text-3xl font-bold text-gray-900">Candidate Matching</h1>
        <p className="mt-2 text-sm text-gray-700">
          Match, shortlist, and schedule interviews with candidates.
        </p>
      </div>

      {/* Job selection */}
      <div className="mb-6">
        <label htmlFor="job-select" className="block text-sm font-medium text-gray-700 mb-2">
          Select Job Description
        </label>
        <select
          id="job-select"
          value={selectedJob || ''}
          onChange={(e) => handleJobSelect(Number(e.target.value))}
          className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
        >
          <option value="" disabled>
            Select a job...
          </option>
          {jobs.map((job) => (
            <option key={job.id} value={job.id}>
              {job.title} - {job.company}
            </option>
          ))}
        </select>
      </div>

      {/* Action buttons */}
      <div className="flex flex-wrap gap-4 mb-6">
        <Button 
          onClick={handleMatchAll}
          disabled={!selectedJob || matchLoading}
          className={matchLoading ? 'opacity-50 cursor-wait' : ''}
        >
          {matchLoading ? 'Matching...' : 'Match All Candidates'}
        </Button>
        <Button 
          onClick={handleShortlist}
          disabled={!selectedJob || shortlistLoading || candidates.length === 0}
          variant="secondary"
          className={shortlistLoading ? 'opacity-50 cursor-wait' : ''}
        >
          {shortlistLoading ? 'Shortlisting...' : 'Shortlist Candidates'}
        </Button>
        <Button 
          onClick={handleScheduleInterviews}
          disabled={!selectedJob || interviewLoading || candidates.filter(c => c.is_shortlisted).length === 0}
          variant="outline"
          className={interviewLoading ? 'opacity-50 cursor-wait' : ''}
        >
          {interviewLoading ? 'Scheduling...' : 'Schedule Interviews'}
        </Button>
      </div>

      {/* Candidates list */}
      {selectedJob && candidates.length > 0 ? (
        <div className="mt-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Matched Candidates</h2>
          
          <div className="bg-white shadow overflow-hidden sm:rounded-md">
            <ul className="divide-y divide-gray-200">
              {candidates.map((candidate) => (
                <li key={candidate.id} className={`relative ${candidate.is_shortlisted ? 'bg-green-50' : ''}`}>
                  <div className="px-4 py-4 sm:px-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <div className="flex-shrink-0">
                          <UserCircleIcon className="h-10 w-10 text-gray-400" />
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-primary-600">{candidate.name}</div>
                          <div className="flex items-center mt-1">
                            <EnvelopeIcon className="h-4 w-4 text-gray-400 mr-1" />
                            <div className="text-sm text-gray-500">{candidate.email}</div>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center">
                        <div className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          candidate.match_score >= 80 ? 'bg-green-100 text-green-800' :
                          candidate.match_score >= 60 ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        }`}>
                          {Math.round(candidate.match_score)}% Match
                        </div>
                        {candidate.is_shortlisted && (
                          <div className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                            <CheckCircleIcon className="h-3 w-3 mr-1" /> Shortlisted
                          </div>
                        )}
                      </div>
                    </div>
                    
                    <div className="mt-2">
                      <div className="text-sm text-gray-700 grid grid-cols-1 md:grid-cols-3 gap-2">
                        <div>
                          <span className="font-medium">Skills:</span> {candidate.skills || 'None listed'}
                        </div>
                        <div>
                          <span className="font-medium">Experience:</span> {candidate.experience || 'None listed'}
                        </div>
                        <div>
                          <span className="font-medium">Education:</span> {candidate.education || 'None listed'}
                        </div>
                      </div>
                    </div>
                    
                    {/* Interview details */}
                    {candidate.interview_scheduled && (
                      <div className="mt-2">
                        <button
                          onClick={() => toggleInterviewExpand(candidate.id)}
                          className="text-sm font-medium text-primary-600 hover:text-primary-800 flex items-center"
                        >
                          {expandedInterviews[candidate.id] ? (
                            <>
                              <ChevronUpIcon className="h-5 w-5 mr-1" />
                              Hide Interview Details
                            </>
                          ) : (
                            <>
                              <ChevronDownIcon className="h-5 w-5 mr-1" />
                              Show Interview Details
                            </>
                          )}
                        </button>
                        
                        {expandedInterviews[candidate.id] && (
                          <div className="mt-3 p-3 bg-gray-50 rounded-md">
                            <h4 className="text-sm font-medium text-gray-900">Interview Invitation Email</h4>
                            <div className="mt-1 text-sm text-gray-700 whitespace-pre-line">
                              {candidate.interview_email || 'Interview details will be generated when scheduling is complete.'}
                            </div>
                            <div className="mt-2">
                              <span className="text-sm font-medium text-gray-900">Interview Format:</span>
                              <span className="ml-2 text-sm text-gray-700">{candidate.interview_format || 'Not specified'}</span>
                            </div>
                            <div className="mt-1">
                              <span className="text-sm font-medium text-gray-900">Suggested Date:</span>
                              <span className="ml-2 text-sm text-gray-700">
                                {candidate.interview_date ? new Date(candidate.interview_date).toLocaleDateString() : 'Not scheduled'}
                              </span>
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      ) : selectedJob ? (
        <div className="text-center py-12 bg-white shadow rounded-lg">
          <UserCircleIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No candidates matched</h3>
          <p className="mt-1 text-sm text-gray-500">Get started by matching candidates to this job.</p>
          <div className="mt-6">
            <Button onClick={handleMatchAll}>
              Match All Candidates
            </Button>
          </div>
        </div>
      ) : null}
    </div>
  );
} 