import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Card from '../components/Card';
import Button from '../components/Button';
import { 
  getJobDescriptions, 
  getCandidates, 
  getShortlistedCount, 
  getInterviewsCount 
} from '../services/api';
import { 
  BriefcaseIcon, 
  UserGroupIcon, 
  DocumentCheckIcon, 
  ArrowTrendingUpIcon 
} from '@heroicons/react/24/outline';

export default function Dashboard() {
  const [stats, setStats] = useState({
    jobs: 0,
    candidates: 0,
    shortlisted: 0,
    interviews: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        // Fetch jobs and candidates count
        const jobs = await getJobDescriptions();
        const candidates = await getCandidates();
        
        // Fetch actual shortlisted and interview counts
        const shortlistedCount = await getShortlistedCount();
        const interviewsCount = await getInterviewsCount();
        
        setStats({
          jobs: jobs.length,
          candidates: candidates.length,
          shortlisted: shortlistedCount,
          interviews: interviewsCount,
        });
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
        setError('Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  const statCards = [
    { name: 'Job Descriptions', value: stats.jobs, icon: BriefcaseIcon, color: 'bg-blue-500', path: '/jobs' },
    { name: 'Candidates', value: stats.candidates, icon: UserGroupIcon, color: 'bg-green-500', path: '/candidates' },
    { name: 'Shortlisted', value: stats.shortlisted, icon: DocumentCheckIcon, color: 'bg-purple-500', path: '/matching' },
    { name: 'Interviews Scheduled', value: stats.interviews, icon: ArrowTrendingUpIcon, color: 'bg-amber-500', path: '/matching' },
  ];

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
      <div className="pb-5 border-b border-gray-200 mb-5">
        <h1 className="text-3xl font-bold text-gray-900 font-display">Dashboard</h1>
        <p className="mt-2 text-sm text-gray-700 font-body">
          Overview of your recruitment activities and statistics.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat) => (
          <Link key={stat.name} to={stat.path}>
            <Card className="cursor-pointer hover:shadow-md transition-shadow duration-200">
              <div className="flex items-center">
                <div className={`p-3 rounded-md ${stat.color}`}>
                  <stat.icon className="h-6 w-6 text-white" aria-hidden="true" />
                </div>
                <div className="ml-5">
                  <p className="text-sm font-medium text-gray-500 font-display">{stat.name}</p>
                  <p className="mt-1 text-3xl font-semibold text-gray-900 font-display">{stat.value}</p>
                </div>
              </div>
            </Card>
          </Link>
        ))}
      </div>

      <div className="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Quick Actions */}
        <Card title="Quick Actions">
          <div className="space-y-3">
            <p className="text-sm text-gray-500 font-body">
              Get started with these common tasks:
            </p>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <Button as={Link} to="/jobs/new" className="w-full justify-center">
                Add New Job
              </Button>
              <Button as={Link} to="/candidates/new" variant="secondary" className="w-full justify-center">
                Add New Candidate
              </Button>
              <Button as={Link} to="/matching" variant="outline" className="w-full justify-center">
                Match Candidates
              </Button>
            </div>
          </div>
        </Card>

        {/* System Status */}
        <Card title="System Status">
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className="h-2.5 w-2.5 rounded-full bg-green-400 mr-2"></div>
                <span className="text-sm font-medium text-gray-900 font-body">AI Services</span>
              </div>
              <span className="text-sm text-gray-500 font-body">Operational</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className="h-2.5 w-2.5 rounded-full bg-green-400 mr-2"></div>
                <span className="text-sm font-medium text-gray-900 font-body">Database</span>
              </div>
              <span className="text-sm text-gray-500 font-body">Connected</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className="h-2.5 w-2.5 rounded-full bg-green-400 mr-2"></div>
                <span className="text-sm font-medium text-gray-900 font-body">API Services</span>
              </div>
              <span className="text-sm text-gray-500 font-body">Operational</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className="h-2.5 w-2.5 rounded-full bg-green-400 mr-2"></div>
                <span className="text-sm font-medium text-gray-900 font-body">LLM Services</span>
              </div>
              <span className="text-sm text-gray-500 font-body">Running</span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
} 