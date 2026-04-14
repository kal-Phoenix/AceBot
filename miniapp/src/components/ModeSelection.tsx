import { Brain, Timer, ArrowRight } from 'lucide-react';
import { useState } from 'react';

interface ModeSelectionProps {
  examTitle: string;
  onSelectMode: (mode: 'practice' | 'exam') => void;
  onBack: () => void;
}

export function ModeSelection({ examTitle, onSelectMode, onBack }: ModeSelectionProps) {
  const [selectedMode, setSelectedMode] = useState<'practice' | 'exam' | null>(null);

  const handleContinue = () => {
    if (selectedMode) {
      onSelectMode(selectedMode);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-slate-900 dark:via-slate-900 dark:to-slate-800 flex items-center justify-center p-4">
      <div className="max-w-3xl w-full">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white mb-2">{examTitle}</h1>
          <p className="text-slate-600 dark:text-slate-400 mb-4">Choose your learning mode</p>
        </div>

        <div className="grid md:grid-cols-2 gap-6 mb-8">
          {/* Practice Mode */}
          <button
            onClick={() => setSelectedMode('practice')}
            className={`p-8 rounded-2xl border-2 transition-all duration-300 text-left ${
              selectedMode === 'practice'
                ? 'border-green-500 bg-green-50 shadow-lg scale-105'
                : 'border-slate-200 bg-white hover:border-green-300 hover:shadow-md'
            }`}
          >
            <div className={`w-16 h-16 rounded-xl flex items-center justify-center mb-4 ${
              selectedMode === 'practice' ? 'bg-green-500' : 'bg-green-100'
            }`}>
              <Brain className={`w-8 h-8 ${
                selectedMode === 'practice' ? 'text-white' : 'text-green-600'
              }`} />
            </div>
            
            <h3 className="text-xl font-bold text-slate-800 mb-2">Practice Mode</h3>
            <p className="text-sm text-slate-600 mb-4">
              Learn as you go with instant feedback
            </p>

            <ul className="space-y-2">
              <li className="flex items-start gap-2 text-sm text-slate-700">
                <span className="text-green-500 mt-0.5">✓</span>
                <span>See correct answers immediately</span>
              </li>
              <li className="flex items-start gap-2 text-sm text-slate-700">
                <span className="text-green-500 mt-0.5">✓</span>
                <span>Get detailed explanations</span>
              </li>
              <li className="flex items-start gap-2 text-sm text-slate-700">
                <span className="text-green-500 mt-0.5">✓</span>
                <span>No time pressure</span>
              </li>
            </ul>
          </button>

          {/* Exam Mode */}
          <button
            onClick={() => setSelectedMode('exam')}
            className={`p-8 rounded-2xl border-2 transition-all duration-300 text-left ${
              selectedMode === 'exam'
                ? 'border-blue-500 bg-blue-50 shadow-lg scale-105'
                : 'border-slate-200 bg-white hover:border-blue-300 hover:shadow-md'
            }`}
          >
            <div className={`w-16 h-16 rounded-xl flex items-center justify-center mb-4 ${
              selectedMode === 'exam' ? 'bg-blue-500' : 'bg-blue-100'
            }`}>
              <Timer className={`w-8 h-8 ${
                selectedMode === 'exam' ? 'text-white' : 'text-blue-600'
              }`} />
            </div>
            
            <h3 className="text-xl font-bold text-slate-800 mb-2">Exam Mode</h3>
            <p className="text-sm text-slate-600 mb-4">
              Test yourself under real exam conditions
            </p>

            <ul className="space-y-2">
              <li className="flex items-start gap-2 text-sm text-slate-700">
                <span className="text-blue-500 mt-0.5">✓</span>
                <span>Timed examination</span>
              </li>
              <li className="flex items-start gap-2 text-sm text-slate-700">
                <span className="text-blue-500 mt-0.5">✓</span>
                <span>Results shown after submission</span>
              </li>
              <li className="flex items-start gap-2 text-sm text-slate-700">
                <span className="text-blue-500 mt-0.5">✓</span>
                <span>Track your performance</span>
              </li>
            </ul>
          </button>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-4">
          <button
            onClick={onBack}
            className="bg-white dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 rounded-2xl p-8 hover:shadow-xl transition-all duration-300 hover:-translate-y-2 hover:border-blue-400 dark:hover:border-blue-500 group"
          >
            Back
          </button>
          
          <button
            onClick={handleContinue}
            disabled={!selectedMode}
            className={`flex-1 py-3 rounded-xl font-semibold flex items-center justify-center gap-2 transition-all duration-300 ${
              selectedMode
                ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:shadow-lg'
                : 'bg-slate-300 text-slate-500 cursor-not-allowed'
            }`}
          >
            <span>Continue</span>
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}
