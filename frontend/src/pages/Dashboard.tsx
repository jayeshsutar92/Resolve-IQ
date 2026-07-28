import React from 'react';
import ComplaintPanel from '../components/ComplaintPanel/ComplaintPanel';
import ChatPanel from '../components/ChatPanel/ChatPanel';

const Dashboard: React.FC = () => {
  return (
    <div className="app-container">
      <ComplaintPanel />
      <ChatPanel />
    </div>
  );
};

export default Dashboard;
