import { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
import { ErrorBoundary } from './components/ErrorBoundary';
import { WelcomePage } from './components/WelcomePage';
import { StreamSelection } from './components/StreamSelection';
import { Dashboard } from './components/Dashboard';
import { OrganizationSelection } from './components/OrganizationSelection';
import { SubjectSelection } from './components/SubjectSelection';
import { YearSelection } from './components/YearSelection';
import { ExamList } from './components/ExamList';
import { ModeSelection } from './components/ModeSelection';
import { ExamPage } from './components/ExamPage';
import { ResultsPage } from './components/ResultsPage';
import { ProgressPage } from './components/ProgressPage';
import { ProfilePage } from './components/ProfilePage';
import { LeaderboardPage } from './components/LeaderboardPage';
import { userAPI } from './lib/api';
import WebApp from '@twa-dev/sdk';

type PageType = 
  | 'welcome' 
  | 'stream-selection' 
  | 'dashboard' 
  | 'organization-selection'
  | 'subject-selection'
  | 'year-selection'
  | 'exam-list' 
  | 'mode-selection'
  | 'exam' 
  | 'results' 
  | 'progress' 
  | 'leaderboard'
  | 'settings';

function AppContent() {
  const { user, loading, updateUser } = useAuth();
  const [currentPage, setCurrentPage] = useState<PageType>('welcome');
  const [showWelcome, setShowWelcome] = useState(true);
  
  // Navigation state
  const [selectedExamType, setSelectedExamType] = useState<'past' | 'mock' | 'model'>('past');
  const [selectedOrganization, setSelectedOrganization] = useState<'year' | 'topic'>('year');
  const [selectedSubject, setSelectedSubject] = useState<string>('');
  const [selectedYear, setSelectedYear] = useState<number>(2017);
  const [selectedExamId, setSelectedExamId] = useState<string>('');
  const [selectedExam, setSelectedExam] = useState<{ title: string; _id: string } | null>(null);
  const [selectedMode, setSelectedMode] = useState<'practice' | 'exam'>('practice');
  const [selectedAttemptId, setSelectedAttemptId] = useState<string>('');

  useEffect(() => {
    // Apply Telegram theme to the app
    document.body.style.backgroundColor = WebApp.backgroundColor || '#f8fafc';
  }, []);

  useEffect(() => {
    if (user && !loading) {
      console.log('User data in App.tsx:', user);
      console.log('User stream:', user.stream);
      
      // If user already has a stream selected, go directly to dashboard
      if (user.stream) {
        console.log('Stream already selected - going to dashboard');
        setCurrentPage('dashboard');
        setShowWelcome(false);
        return;
      }
      
      // Check if this is a first-time visitor
      const hasSeenWelcome = localStorage.getItem('hasSeenWelcome');
      
      if (!hasSeenWelcome) {
        // First-time visitor - show welcome page
        console.log('First-time visitor - showing welcome page');
        setCurrentPage('welcome');
        setShowWelcome(true);
      } else {
        // Returning user without stream - show stream selection
        console.log('Returning user without stream - showing stream selection');
        setShowWelcome(false);
        setCurrentPage('stream-selection');
      }
    }
  }, [user, loading]);

  const handleGetStarted = () => {
    // Mark that user has seen the welcome page
    localStorage.setItem('hasSeenWelcome', 'true');
    setShowWelcome(false);
    if (user?.stream) {
      setCurrentPage('dashboard');
    } else {
      setCurrentPage('stream-selection');
    }
  };

  const handleSelectStream = async (stream: 'natural' | 'social') => {
    try {
      console.log('Selecting stream:', stream);
      console.log('Current user:', user);
      console.log('Auth token:', localStorage.getItem('auth_token'));
      
      const response = await userAPI.selectStream(stream);
      console.log('Stream selection response:', response);
      
      // Update user in context with the response from backend
      if (response.user) {
        console.log('Updating user with response:', response.user);
        updateUser(response.user);
        // Also update localStorage to ensure persistence
        localStorage.setItem('user', JSON.stringify(response.user));
      } else {
        const updatedUser = { ...user, stream: stream };
        console.log('Updating user with fallback:', updatedUser);
        updateUser(updatedUser);
        localStorage.setItem('user', JSON.stringify(updatedUser));
      }
      
      // Navigate to dashboard
      console.log('Navigating to dashboard');
      setCurrentPage('dashboard');
    } catch (error: any) {
      console.error('Error selecting stream:', error);
      console.error('Error response:', error.response?.data);
      console.error('Error status:', error.response?.status);
      
      // Show more detailed error message
      const errorMessage = error.response?.data?.error || error.message || 'Unknown error occurred';
      alert(`Failed to save stream selection: ${errorMessage}\n\nPlease make sure you are logged in and try again.`);
    }
  };

  const handleSelectExamType = (type: 'past' | 'mock' | 'model') => {
    setSelectedExamType(type);
    // Only Past Exams need organization selection
    if (type === 'past') {
      setCurrentPage('organization-selection');
    } else {
      setCurrentPage('subject-selection');
    }
  };

  const handleSelectOrganization = (organization: 'year' | 'topic') => {
    setSelectedOrganization(organization);
    setCurrentPage('subject-selection');
  };

  const handleSelectSubject = (subject: string) => {
    setSelectedSubject(subject);
    // If organized by year, go to year selection; otherwise go to exam list
    if (selectedOrganization === 'year' && selectedExamType === 'past') {
      setCurrentPage('year-selection');
    } else {
      setCurrentPage('exam-list');
    }
  };

  const handleSelectYear = (year: number) => {
    setSelectedYear(year);
    setCurrentPage('exam-list');
  };

  const handleSelectExam = (examId: string, exam: { title: string; _id: string }) => {
    setSelectedExamId(examId);
    setSelectedExam(exam);
    setCurrentPage('mode-selection');
  };

  const handleSelectMode = (mode: 'practice' | 'exam') => {
    setSelectedMode(mode);
    setCurrentPage('exam');
  };

  const handleExamComplete = (attemptId: string) => {
    setSelectedAttemptId(attemptId);
    setCurrentPage('results');
  };

  const handleBackToDashboard = () => {
    setCurrentPage('dashboard');
    setSelectedExamId('');
    setSelectedAttemptId('');
    setSelectedExamType('past');
    setSelectedOrganization('year');
    setSelectedSubject('');
    setSelectedYear(2017);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-slate-600">Connecting to Telegram...</p>
        </div>
      </div>
    );
  }

  // Show welcome page on first visit
  if (showWelcome && currentPage === 'welcome') {
    return <WelcomePage onGetStarted={handleGetStarted} />;
  }

  // Stream selection
  if (currentPage === 'stream-selection') {
    return <StreamSelection onSelectStream={handleSelectStream} />;
  }

  // Dashboard
  if (currentPage === 'dashboard') {
    return (
      <Dashboard
        onSelectExamType={handleSelectExamType}
        onNavigate={(page: 'progress' | 'leaderboard' | 'settings') => setCurrentPage(page)}
      />
    );
  }

  // Organization selection (for Past Exams only)
  if (currentPage === 'organization-selection') {
    return (
      <OrganizationSelection
        examType={selectedExamType}
        onSelectOrganization={handleSelectOrganization}
        onBack={handleBackToDashboard}
      />
    );
  }

  // Subject selection
  if (currentPage === 'subject-selection' && user.stream) {
    return (
      <SubjectSelection
        examType={selectedExamType}
        stream={user.stream}
        onSelectSubject={handleSelectSubject}
        onBack={() => {
          // Go back to organization selection if it's Past Exams, otherwise go to dashboard
          if (selectedExamType === 'past') {
            setCurrentPage('organization-selection');
          } else {
            handleBackToDashboard();
          }
        }}
      />
    );
  }

  // Year selection (for Past Exams organized by year)
  if (currentPage === 'year-selection') {
    return (
      <YearSelection
        subject={selectedSubject}
        onSelectYear={handleSelectYear}
        onBack={() => setCurrentPage('subject-selection')}
      />
    );
  }

  // Exam list
  if (currentPage === 'exam-list' && user.stream) {
    return (
      <ExamList
        examType={selectedExamType}
        subject={selectedSubject}
        stream={user.stream}
        year={selectedOrganization === 'year' ? selectedYear : undefined}
        onSelectExam={handleSelectExam}
        onBack={() => {
          // Go back to year selection if organized by year, otherwise to subject selection
          if (selectedOrganization === 'year' && selectedExamType === 'past') {
            setCurrentPage('year-selection');
          } else {
            setCurrentPage('subject-selection');
          }
        }}
      />
    );
  }

  // Mode selection
  if (currentPage === 'mode-selection' && selectedExam) {
    return (
      <ModeSelection
        examTitle={selectedExam.title}
        onSelectMode={handleSelectMode}
        onBack={() => setCurrentPage('exam-list')}
      />
    );
  }

  if (currentPage === 'exam' && selectedExamId) {
    return (
      <ExamPage
        examId={selectedExamId}
        mode={selectedMode}
        onComplete={handleExamComplete}
        onBack={handleBackToDashboard}
      />
    );
  }

  if (currentPage === 'results' && selectedAttemptId) {
    return <ResultsPage attemptId={selectedAttemptId} onBack={handleBackToDashboard} onNavigate={(page) => setCurrentPage(page)} />;
  }

  if (currentPage === 'progress') {
    return <ProgressPage onBack={handleBackToDashboard} />;
  }

  if (currentPage === 'leaderboard') {
    return <LeaderboardPage onBack={handleBackToDashboard} />;
  }

  if (currentPage === 'settings') {
    return <ProfilePage onBack={handleBackToDashboard} onNavigate={(page: 'progress' | 'leaderboard' | 'settings') => setCurrentPage(page)} />;
  }

  // Fallback to dashboard
  return (
    <Dashboard
      onSelectExamType={handleSelectExamType}
      onNavigate={(page: 'progress' | 'leaderboard' | 'settings') => setCurrentPage(page)}
    />
  );
}

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider>
        <AuthProvider>
          <AppContent />
        </AuthProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
