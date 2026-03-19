import React, { useState } from 'react';
import './index.css';
import Navigation from './components/Navigation';
import HeroSection from './components/HeroSection';
import ProblemSection from './components/ProblemSection';
import VisionSection from './components/VisionSection';
import LearningSection from './components/LearningSection';
import ActivitiesSection from './components/ActivitiesSection';
import ParticipationSection from './components/ParticipationSection';
import JoinSection from './components/JoinSection';

function App() {
  const [modalOpen, setModalOpen] = useState(false);
  const [preselectedRole, setPreselectedRole] = useState('');

  const handleRoleSelect = (role) => {
    setPreselectedRole(role);
    setModalOpen(true);
  };

  const handleOpenModal = () => {
    setPreselectedRole('');
    setModalOpen(true);
  };

  return (
    <div className="min-h-screen bg-black text-white">
      <Navigation onJoinClick={handleOpenModal} />
      <HeroSection onJoinClick={handleOpenModal} />
      <ProblemSection />
      <VisionSection />
      <LearningSection />
      <ActivitiesSection />
      <ParticipationSection onRoleSelect={handleRoleSelect} />
      <JoinSection
        isModalOpen={modalOpen}
        onOpenModal={handleOpenModal}
        onCloseModal={() => setModalOpen(false)}
        preselectedRole={preselectedRole}
      />
    </div>
  );
}

export default App;

