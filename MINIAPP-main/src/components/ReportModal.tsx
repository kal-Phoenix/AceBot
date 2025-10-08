import { useState } from 'react';
import { X } from 'lucide-react';
import { Button } from './Button';
import { Card } from './Card';
import { supabase } from '../lib/supabase';
import { useAuth } from '../contexts/AuthContext';
import type { Question } from '../types/question.types';

interface ReportModalProps {
  question: Question;
  onClose: () => void;
}

export function ReportModal({ question, onClose }: ReportModalProps) {
  const { user } = useAuth();
  const [reason, setReason] = useState('');
  const [description, setDescription] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const reasons = [
    'Incorrect answer marked as correct',
    'Question text has errors',
    'Answer options are unclear',
    'Explanation is wrong or unclear',
    'Image not loading or incorrect',
    'Other issue',
  ];

  async function handleSubmit() {
    if (!user || !reason) return;

    setSubmitting(true);

    const { error } = await supabase.from('question_reports').insert({
      user_id: user.id,
      question_id: question.id,
      subject: question.subject,
      grade: question.grade,
      reason,
      description: description || null,
    });

    if (error) {
      console.error('Error submitting report:', error);
      alert('Failed to submit report. Please try again.');
    } else {
      setSubmitted(true);
      setTimeout(() => {
        onClose();
      }, 2000);
    }

    setSubmitting(false);
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
      <Card className="w-full max-w-md max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">
              Report Question
            </h2>
            <button
              onClick={onClose}
              className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              <X className="w-5 h-5 text-gray-600 dark:text-gray-400" />
            </button>
          </div>

          {submitted ? (
            <div className="text-center py-8">
              <div className="w-16 h-16 bg-green-100 dark:bg-green-900 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg
                  className="w-8 h-8 text-green-600 dark:text-green-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              </div>
              <p className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                Report Submitted
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Thank you for helping us improve the quality of our questions!
              </p>
            </div>
          ) : (
            <>
              <div className="mb-4 p-3 bg-gray-100 dark:bg-gray-700 rounded-lg">
                <p className="text-sm text-gray-700 dark:text-gray-300">
                  <strong>Question:</strong> {question.questionText}
                </p>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Select a reason <span className="text-red-500">*</span>
                  </label>
                  <div className="space-y-2">
                    {reasons.map((r) => (
                      <button
                        key={r}
                        onClick={() => setReason(r)}
                        className={`w-full px-4 py-2 rounded-lg text-left text-sm transition-colors ${
                          reason === r
                            ? 'bg-blue-600 text-white'
                            : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                        }`}
                      >
                        {r}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Additional details (optional)
                  </label>
                  <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={4}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Please provide more details if needed..."
                  />
                </div>

                <div className="flex space-x-3">
                  <Button
                    variant="secondary"
                    onClick={onClose}
                    fullWidth
                    disabled={submitting}
                  >
                    Cancel
                  </Button>
                  <Button
                    variant="primary"
                    onClick={handleSubmit}
                    fullWidth
                    disabled={!reason || submitting}
                  >
                    {submitting ? 'Submitting...' : 'Submit Report'}
                  </Button>
                </div>
              </div>
            </>
          )}
        </div>
      </Card>
    </div>
  );
}
