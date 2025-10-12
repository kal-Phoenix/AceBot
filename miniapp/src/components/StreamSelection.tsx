import { useState } from 'react';
import { Microscope, Users, ArrowRight } from 'lucide-react';

interface StreamSelectionProps {
  onSelectStream: (stream: 'natural' | 'social') => void;
}

export function StreamSelection({ onSelectStream }: StreamSelectionProps) {
  const [selectedStream, setSelectedStream] = useState<'natural' | 'social' | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async () => {
    if (!selectedStream) return;
    
    // Show confirmation dialog for permanent selection
    const confirmed = window.confirm(
      `You are about to select "${selectedStream === 'natural' ? 'Natural Science' : 'Social Science'}" as your stream.\n\n⚠️ WARNING: This selection is PERMANENT and cannot be changed later!\n\nAre you sure you want to continue?`
    );
    
    if (!confirmed) return;
    
    setIsSubmitting(true);
    try {
      console.log('Starting stream selection for:', selectedStream);
      await onSelectStream(selectedStream);
      console.log('Stream selection completed successfully');
    } catch (error) {
      console.error('Error selecting stream:', error);
      console.error('Error details:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status,
        config: error.config
      });
      
      // Show more detailed error message
      const errorMessage = error.response?.data?.error || error.message || 'Unknown error occurred';
      alert(`Failed to save stream selection: ${errorMessage}\n\nPlease check your internet connection and try again.`);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white mb-3">
            Choose Your Stream
          </h1>
          <p className="text-slate-600 dark:text-slate-400 mb-4">
            Select the stream that matches your academic focus
          </p>
          
          {/* Warning Message */}
          <div className="bg-amber-50 dark:bg-amber-900/20 border-2 border-amber-200 dark:border-amber-700 rounded-2xl p-4 mb-6">
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 bg-amber-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                <span className="text-white text-xs font-bold">!</span>
              </div>
              <div className="text-left">
                <h3 className="text-sm font-bold text-amber-800 dark:text-amber-200 mb-1">
                  ⚠️ Permanent Selection
                </h3>
                <p className="text-xs text-amber-700 dark:text-amber-300 leading-relaxed">
                  This is a <strong>one-time selection</strong> that cannot be changed later. Choose carefully!
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-4 mb-8">
          {/* Natural Science */}
          <button
            onClick={() => setSelectedStream('natural')}
            className={`w-full p-6 rounded-3xl border-2 transition-all duration-300 text-left ${
              selectedStream === 'natural'
                ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20 shadow-xl scale-[1.02]'
                : 'border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:border-blue-300 hover:shadow-lg active:scale-98'
            }`}
          >
            <div className="flex items-center gap-4 mb-4">
              <div className={`w-14 h-14 rounded-2xl flex items-center justify-center shadow-lg ${
                selectedStream === 'natural'
                  ? 'bg-gradient-to-br from-blue-500 to-blue-600'
                  : 'bg-gradient-to-br from-blue-100 to-blue-200 dark:from-blue-900/30 dark:to-blue-800/30'
              }`}>
                <Microscope className={`w-7 h-7 ${
                  selectedStream === 'natural' ? 'text-white' : 'text-blue-600'
                }`} />
              </div>
              <div>
                <h3 className="text-lg font-bold text-slate-800 dark:text-white">Natural Science</h3>
                <p className="text-sm text-slate-600 dark:text-slate-400">🧬 Science & Mathematics</p>
              </div>
            </div>

            <div className="space-y-2">
              <p className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Subjects:</p>
              <div className="flex flex-wrap gap-2">
                {['English', 'Maths', 'SAT', 'Chemistry', 'Biology', 'Physics'].map((subject) => (
                  <span
                    key={subject}
                    className={`px-3 py-1 rounded-full text-xs font-medium ${
                      selectedStream === 'natural'
                        ? 'bg-blue-500 text-white shadow-md'
                        : 'bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300'
                    }`}
                  >
                    {subject}
                  </span>
                ))}
              </div>
            </div>
          </button>

          {/* Social Science */}
          <button
            onClick={() => setSelectedStream('social')}
            className={`w-full p-6 rounded-3xl border-2 transition-all duration-300 text-left ${
              selectedStream === 'social'
                ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20 shadow-xl scale-[1.02]'
                : 'border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:border-purple-300 hover:shadow-lg active:scale-98'
            }`}
          >
            <div className="flex items-center gap-4 mb-4">
              <div className={`w-14 h-14 rounded-2xl flex items-center justify-center shadow-lg ${
                selectedStream === 'social'
                  ? 'bg-gradient-to-br from-purple-500 to-purple-600'
                  : 'bg-gradient-to-br from-purple-100 to-purple-200 dark:from-purple-900/30 dark:to-purple-800/30'
              }`}>
                <Users className={`w-7 h-7 ${
                  selectedStream === 'social' ? 'text-white' : 'text-purple-600'
                }`} />
              </div>
              <div>
                <h3 className="text-lg font-bold text-slate-800 dark:text-white">Social Science</h3>
                <p className="text-sm text-slate-600 dark:text-slate-400">📚 Humanities & Social Studies</p>
              </div>
            </div>

            <div className="space-y-2">
              <p className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Subjects:</p>
              <div className="flex flex-wrap gap-2">
                {['English', 'Maths', 'SAT', 'History', 'Geography', 'Economics'].map((subject) => (
                  <span
                    key={subject}
                    className={`px-3 py-1 rounded-full text-xs font-medium ${
                      selectedStream === 'social'
                        ? 'bg-purple-500 text-white shadow-md'
                        : 'bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300'
                    }`}
                  >
                    {subject}
                  </span>
                ))}
              </div>
            </div>
          </button>
        </div>

        {/* Continue Button */}
        <button
          onClick={handleSubmit}
          disabled={!selectedStream || isSubmitting}
          className={`w-full py-4 rounded-2xl font-bold text-lg transition-all duration-300 flex items-center justify-center gap-3 ${
            selectedStream && !isSubmitting
              ? 'bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 text-white shadow-2xl hover:shadow-3xl transform hover:scale-[1.02] active:scale-98'
              : 'bg-slate-300 dark:bg-slate-700 text-slate-500 dark:text-slate-400 cursor-not-allowed'
          }`}
        >
          {isSubmitting ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              <span>Saving...</span>
            </>
          ) : (
            <>
              <span>Continue</span>
              <ArrowRight className="w-5 h-5" />
            </>
          )}
        </button>

        <p className="text-center text-sm text-slate-500 dark:text-slate-400 mt-6">
          You can change your stream later in settings
        </p>
      </div>
    </div>
  );
}
