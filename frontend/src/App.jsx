import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Jobs from './pages/Jobs';
import Matching from './pages/Matching';
import Candidates from './pages/Candidates';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/jobs" element={<Jobs />} />
          <Route path="/candidates" element={<Candidates />} />
          <Route path="/matching" element={<Matching />} />
          {/* Add other routes as we develop more features */}
        </Routes>
      </Layout>
    </Router>
  );
}

export default App; 