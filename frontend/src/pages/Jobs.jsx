import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getJobDescriptions } from '../services/api';
import Card from '../components/Card';
import Button from '../components/Button';
import { PlusIcon, ArrowTopRightOnSquareIcon } from '@heroicons/react/24/outline';

export default function Jobs() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchJobs() {
      try {
        setLoading(true);
        const data = await getJobDescriptions();
        setJobs(data);
      } catch (err) {
        console.error('Error fetching jobs:', err);
        setError('Failed to load job descriptions');
      } finally {
        setLoading(false);
      }
    }

    fetchJobs();
  }, []);

  if (loading) {
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

  return (
    <div>
      <div className="pb-5 border-b border-gray-200 sm:flex sm:items-center sm:justify-between mb-5">
        <h1 className="text-3xl font-bold text-gray-900">Job Descriptions</h1>
        <div className="mt-3 sm:mt-0 sm:ml-4">
          <Button as={Link} to="/jobs/new" className="inline-flex items-center">
            <PlusIcon className="-ml-1 mr-2 h-5 w-5" aria-hidden="true" />
            Add New Job
          </Button>
        </div>
      </div>

      {jobs.length === 0 ? (
        <div className="text-center py-12">
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 13h6m-3-3v6m-9 1V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z"
            />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">No job descriptions</h3>
          <p className="mt-1 text-sm text-gray-500">Get started by creating a new job description.</p>
          <div className="mt-6">
            <Button as={Link} to="/jobs/new">
              <PlusIcon className="-ml-1 mr-2 h-5 w-5" aria-hidden="true" />
              Add Job Description
            </Button>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {jobs.map((job) => (
            <Link key={job.id} to={`/jobs/${job.id}`}>
              <Card 
                className="h-full cursor-pointer hover:shadow-md transition-shadow duration-200"
                title={
                  <div className="flex justify-between items-center">
                    <h3 className="text-lg font-medium text-gray-900 truncate">{job.title}</h3>
                    <ArrowTopRightOnSquareIcon className="h-5 w-5 text-gray-400" />
                  </div>
                }
              >
                <div className="space-y-3">
                  <p className="text-sm text-gray-500">{job.company}</p>
                  
                  <div className="space-y-2">
                    {job.summary && (
                      <p className="text-sm text-gray-800 line-clamp-3">{job.summary}</p>
                    )}
                    
                    {job.required_skills && (
                      <div>
                        <h4 className="text-xs font-medium text-gray-500 uppercase">Skills</h4>
                        <p className="text-sm text-gray-700 line-clamp-2">{job.required_skills}</p>
                      </div>
                    )}
                  </div>
                </div>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
} 