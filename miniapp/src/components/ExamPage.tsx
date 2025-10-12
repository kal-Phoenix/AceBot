import { useState, useEffect } from 'react';
import { ArrowLeft, ArrowRight, CheckCircle, XCircle, Clock, Flag } from 'lucide-react';
import { examsAPI, attemptsAPI } from '../lib/api';

interface ExamPageNewProps {
  examId: string;
  mode: 'practice' | 'exam';
  onComplete: (attemptId: string) => void;
  onBack: () => void;
}

export function ExamPage({ examId, mode, onComplete, onBack }: ExamPageNewProps) {
  const [exam, setExam] = useState<any>(null);
  const [questions, setQuestions] = useState<any[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<string>('');
  const [answers, setAnswers] = useState<Map<number, string>>(new Map());
  const [showFeedback, setShowFeedback] = useState(false);
  const [attemptId, setAttemptId] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [timeLeft, setTimeLeft] = useState(0);
  const [startTime] = useState(Date.now());

  useEffect(() => {
    loadExam();
  }, [examId]);

  useEffect(() => {
    if (mode === 'exam' && exam && timeLeft > 0) {
      const timer = setInterval(() => {
        setTimeLeft((prev) => {
          if (prev <= 1) {
            handleSubmitExam();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);

      return () => clearInterval(timer);
    }
  }, [mode, exam, timeLeft]);

  const loadExam = async () => {
    try {
      const examData = await examsAPI.getById(examId);
      const questionsData = await examsAPI.getQuestions(examId);
      
      setExam(examData);
      setQuestions(questionsData);
      
      if (mode === 'exam') {
        setTimeLeft(examData.duration_minutes * 60);
      }

      // Create attempt
      const attempt = await attemptsAPI.create({
        exam_id: examId,
        exam_title: examData.title,
        exam_type: (examData as any).exam_type,
        subject: (examData as any).subject,
        mode: mode,
        max_points: questionsData.reduce((sum: number, q: any) => sum + q.points, 0),
      });
      
      setAttemptId(attempt._id);
    } catch (error) {
      console.error('Error loading exam:', error);
    } finally {
      setLoading(false);
    }
  };

  const currentQuestion = questions[currentQuestionIndex];

  const handleAnswerSelect = (answer: string) => {
    setSelectedAnswer(answer);
    
    if (mode === 'practice') {
      setShowFeedback(true);
    }
  };

  const handleNext = async () => {
    if (!selectedAnswer) return;

    // Save answer
    const newAnswers = new Map(answers);
    newAnswers.set(currentQuestionIndex, selectedAnswer);
    setAnswers(newAnswers);

    // Submit answer to backend (for practice mode tracking)
    if (mode === 'practice' && attemptId) {
      try {
        await attemptsAPI.submitAnswer(attemptId, {
          question_id: currentQuestion.question_id,
          question_number: currentQuestion.question_number,
          selected_answer: selectedAnswer,
          correct_answer: currentQuestion.correct_answer,
          points: currentQuestion.points,
        });
      } catch (error) {
        console.error('Error submitting answer:', error);
      }
    }

    // Move to next question or finish
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setSelectedAnswer('');
      setShowFeedback(false);
    } else {
      // Last question - submit exam
      await handleSubmitExam();
    }
  };

  const handleSubmitExam = async () => {
    try {
      const timeSpent = Math.floor((Date.now() - startTime) / 1000);
      
      const answersArray = questions.map((q, index) => ({
        question_id: q.question_id,
        question_number: q.question_number,
        selected_answer: answers.get(index) || '',
        correct_answer: q.correct_answer,
        is_correct: answers.get(index) === q.correct_answer,
        points_earned: answers.get(index) === q.correct_answer ? q.points : 0,
        answered_at: new Date().toISOString(),
      }));

      await attemptsAPI.complete(attemptId, {
        answers: answersArray,
        max_points: questions.reduce((sum, q) => sum + q.points, 0),
        time_spent_seconds: timeSpent,
      });

      onComplete(attemptId);
    } catch (error) {
      console.error('Error submitting exam:', error);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!currentQuestion) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center">
        <p className="text-slate-600 dark:text-slate-400">No questions available</p>
      </div>
    );
  }

  const isCorrect = selectedAnswer === currentQuestion.correct_answer;
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100;

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900">
      {/* Header */}
      <div className="bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between mb-3">
            <button
              onClick={onBack}
              className="w-10 h-10 flex items-center justify-center rounded-full hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
            >
              <ArrowLeft className="w-5 h-5 text-slate-600 dark:text-slate-400" />
            </button>

            <div className="flex items-center gap-4">
              {mode === 'exam' && (
                <div className="flex items-center gap-2 text-orange-600 font-semibold">
                  <Clock className="w-5 h-5" />
                  <span>{formatTime(timeLeft)}</span>
                </div>
              )}
              
              <div className="flex items-center gap-2 text-slate-600">
                <Flag className="w-5 h-5" />
                <span className="font-semibold">
                  {currentQuestionIndex + 1} / {questions.length}
                </span>
              </div>
            </div>
          </div>

          {/* Progress Bar */}
          <div className="w-full bg-slate-200 rounded-full h-2">
            <div
              className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto p-6">
        {/* Question */}
        <div className="bg-white rounded-2xl p-8 shadow-sm border border-slate-200 mb-6">
          <div className="mb-2 text-sm font-medium text-blue-600">
            Question {currentQuestion.question_number}
          </div>
          <h2 className="text-xl font-bold text-slate-800 mb-6">
            {currentQuestion.question_text}
          </h2>

          {/* Options */}
          <div className="space-y-3">
            {Object.entries(currentQuestion.options).map(([key, value]) => {
              const optionKey = key.toUpperCase();
              const isSelected = selectedAnswer === optionKey;
              const isCorrectOption = optionKey === currentQuestion.correct_answer;
              
              let optionClass = 'bg-white border-2 border-slate-200 hover:border-blue-300';
              
              if (showFeedback && mode === 'practice') {
                if (isSelected && isCorrect) {
                  optionClass = 'bg-green-50 border-2 border-green-500';
                } else if (isSelected && !isCorrect) {
                  optionClass = 'bg-red-50 border-2 border-red-500';
                } else if (isCorrectOption) {
                  optionClass = 'bg-green-50 border-2 border-green-500';
                }
              } else if (isSelected) {
                optionClass = 'bg-blue-50 border-2 border-blue-500';
              }

              return (
                <button
                  key={key}
                  onClick={() => !showFeedback && handleAnswerSelect(optionKey)}
                  disabled={showFeedback && mode === 'practice'}
                  className={`w-full p-4 rounded-xl text-left transition-all duration-300 ${optionClass} ${
                    showFeedback && mode === 'practice' ? 'cursor-default' : 'cursor-pointer'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${
                      isSelected ? 'bg-blue-500 text-white' : 'bg-slate-100 text-slate-600'
                    }`}>
                      {optionKey}
                    </div>
                    <span className="flex-1 text-slate-800">{value as string}</span>
                    
                    {showFeedback && mode === 'practice' && (
                      <>
                        {isSelected && isCorrect && (
                          <CheckCircle className="w-6 h-6 text-green-600" />
                        )}
                        {isSelected && !isCorrect && (
                          <XCircle className="w-6 h-6 text-red-600" />
                        )}
                        {!isSelected && isCorrectOption && (
                          <CheckCircle className="w-6 h-6 text-green-600" />
                        )}
                      </>
                    )}
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Feedback (Practice Mode Only) */}
        {showFeedback && mode === 'practice' && (
          <div className={`rounded-2xl p-6 mb-6 ${
            isCorrect ? 'bg-green-50 border-2 border-green-200' : 'bg-red-50 border-2 border-red-200'
          }`}>
            <div className="flex items-start gap-3 mb-3">
              {isCorrect ? (
                <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
              ) : (
                <XCircle className="w-6 h-6 text-red-600 flex-shrink-0 mt-1" />
              )}
              <div>
                <h3 className={`font-bold mb-2 ${isCorrect ? 'text-green-800' : 'text-red-800'}`}>
                  {isCorrect ? 'Correct!' : 'Incorrect'}
                </h3>
                <p className="text-slate-700 leading-relaxed">
                  {currentQuestion.explanation}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Navigation */}
        <div className="flex gap-4">
          <button
            onClick={handleNext}
            disabled={!selectedAnswer || (mode === 'practice' && !showFeedback)}
            className={`flex-1 py-4 rounded-xl font-semibold flex items-center justify-center gap-2 transition-all duration-300 ${
              selectedAnswer && (mode === 'exam' || showFeedback)
                ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:shadow-lg'
                : 'bg-slate-300 text-slate-500 cursor-not-allowed'
            }`}
          >
            <span>
              {currentQuestionIndex === questions.length - 1 ? 'Submit Exam' : 'Next Question'}
            </span>
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}
