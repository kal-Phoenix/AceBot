import { useState } from 'react';
import { ChevronLeft, ChevronRight, Flag as FlagIcon, Lightbulb, AlertCircle } from 'lucide-react';
import { Layout } from '../components/Layout';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import type { Question, UserAnswer } from '../types/question.types';

interface ReviewAnswersProps {
  questions: Question[];
  answers: UserAnswer[];
  onReportQuestion: (questionId: string) => void;
  onBack: () => void;
}

export function ReviewAnswers({
  questions,
  answers,
  onReportQuestion,
  onBack,
}: ReviewAnswersProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [filter, setFilter] = useState<'all' | 'incorrect' | 'flagged'>('all');

  const filteredIndices = questions
    .map((_, index) => index)
    .filter((index) => {
      if (filter === 'incorrect') return !answers[index].isCorrect;
      if (filter === 'flagged') return answers[index].isFlagged;
      return true;
    });

  const currentFilteredIndex = filteredIndices.indexOf(currentIndex);
  const currentQuestion = questions[currentIndex];
  const currentAnswer = answers[currentIndex];

  function handleNext() {
    const nextIndex = filteredIndices[currentFilteredIndex + 1];
    if (nextIndex !== undefined) {
      setCurrentIndex(nextIndex);
    }
  }

  function handlePrevious() {
    const prevIndex = filteredIndices[currentFilteredIndex - 1];
    if (prevIndex !== undefined) {
      setCurrentIndex(prevIndex);
    }
  }

  function handleQuestionSelect(index: number) {
    setCurrentIndex(index);
  }

  return (
    <Layout>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <button
            onClick={onBack}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
          >
            <ChevronLeft className="w-6 h-6 text-gray-700 dark:text-gray-300" />
          </button>

          <h1 className="text-xl font-bold text-gray-900 dark:text-white">
            Review Answers
          </h1>

          <div className="w-10" />
        </div>

        <div className="flex space-x-2 overflow-x-auto pb-2">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-lg whitespace-nowrap font-medium transition-colors ${
              filter === 'all'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
            }`}
          >
            All ({questions.length})
          </button>
          <button
            onClick={() => {
              setFilter('incorrect');
              const firstIncorrect = answers.findIndex((a) => !a.isCorrect);
              if (firstIncorrect !== -1) setCurrentIndex(firstIncorrect);
            }}
            className={`px-4 py-2 rounded-lg whitespace-nowrap font-medium transition-colors ${
              filter === 'incorrect'
                ? 'bg-red-600 text-white'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
            }`}
          >
            Incorrect ({answers.filter((a) => !a.isCorrect).length})
          </button>
          <button
            onClick={() => {
              setFilter('flagged');
              const firstFlagged = answers.findIndex((a) => a.isFlagged);
              if (firstFlagged !== -1) setCurrentIndex(firstFlagged);
            }}
            className={`px-4 py-2 rounded-lg whitespace-nowrap font-medium transition-colors ${
              filter === 'flagged'
                ? 'bg-orange-600 text-white'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
            }`}
          >
            Flagged ({answers.filter((a) => a.isFlagged).length})
          </button>
        </div>

        <div className="grid grid-cols-5 sm:grid-cols-10 gap-2">
          {filteredIndices.map((index) => (
            <button
              key={index}
              onClick={() => handleQuestionSelect(index)}
              className={`aspect-square rounded-lg font-semibold text-sm transition-colors ${
                index === currentIndex
                  ? 'bg-blue-600 text-white ring-2 ring-blue-400 ring-offset-2'
                  : answers[index].isCorrect
                  ? 'bg-green-500 text-white'
                  : 'bg-red-500 text-white'
              }`}
            >
              {index + 1}
            </button>
          ))}
        </div>

        <Card className="p-6">
          <div className="flex items-start justify-between mb-4">
            <div>
              <div className="flex items-center space-x-2 mb-2">
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  Question {currentIndex + 1} of {questions.length}
                </span>
                {currentAnswer.isFlagged && (
                  <FlagIcon className="w-4 h-4 text-red-500 fill-current" />
                )}
              </div>
              <div
                className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold ${
                  currentAnswer.isCorrect
                    ? 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200'
                    : 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200'
                }`}
              >
                {currentAnswer.isCorrect ? 'Correct' : 'Incorrect'}
              </div>
            </div>

            <button
              onClick={() => onReportQuestion(currentQuestion.id)}
              className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
              title="Report this question"
            >
              <AlertCircle className="w-5 h-5 text-gray-600 dark:text-gray-400" />
            </button>
          </div>

          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            {currentQuestion.questionText}
          </h2>

          {currentQuestion.questionImage && (
            <img
              src={currentQuestion.questionImage}
              alt="Question"
              className="mb-4 rounded-lg max-w-full"
            />
          )}

          {currentAnswer.usedHint && (
            <div className="mb-4 p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border-l-4 border-yellow-400">
              <div className="flex items-start space-x-2">
                <Lightbulb className="w-5 h-5 text-yellow-600 dark:text-yellow-400 mt-0.5" />
                <div>
                  <p className="text-sm font-semibold text-yellow-800 dark:text-yellow-200 mb-1">
                    Hint Used
                  </p>
                  <p className="text-sm text-yellow-800 dark:text-yellow-200">
                    {currentQuestion.hint}
                  </p>
                </div>
              </div>
            </div>
          )}

          <div className="space-y-3 mb-4">
            {currentQuestion.options.map((option, index) => {
              const isSelected = currentAnswer.selectedAnswer === index;
              const isCorrect = index === currentQuestion.correctAnswer;

              return (
                <div
                  key={index}
                  className={`p-4 rounded-lg border-2 ${
                    isCorrect
                      ? 'bg-green-100 dark:bg-green-900/30 border-green-500'
                      : isSelected && !isCorrect
                      ? 'bg-red-100 dark:bg-red-900/30 border-red-500'
                      : 'bg-gray-100 dark:bg-gray-700 border-transparent'
                  }`}
                >
                  <div className="flex items-start space-x-3">
                    <span className="font-semibold text-gray-700 dark:text-gray-300">
                      {String.fromCharCode(65 + index)}.
                    </span>
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <span className="text-gray-900 dark:text-white">{option.text}</span>
                        {isCorrect && (
                          <span className="text-sm font-semibold text-green-600 dark:text-green-400">
                            Correct Answer
                          </span>
                        )}
                        {isSelected && !isCorrect && (
                          <span className="text-sm font-semibold text-red-600 dark:text-red-400">
                            Your Answer
                          </span>
                        )}
                      </div>
                      {option.image && (
                        <img
                          src={option.image}
                          alt={`Option ${String.fromCharCode(65 + index)}`}
                          className="mt-2 rounded max-w-xs"
                        />
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border-l-4 border-blue-400">
            <p className="text-sm font-semibold text-blue-800 dark:text-blue-200 mb-2">
              Explanation
            </p>
            <p className="text-sm text-blue-800 dark:text-blue-200">
              {currentQuestion.explanation}
            </p>
          </div>
        </Card>

        <div className="flex items-center justify-between">
          <Button
            onClick={handlePrevious}
            disabled={currentFilteredIndex === 0}
            variant="secondary"
          >
            <ChevronLeft className="w-4 h-4 inline mr-1" />
            Previous
          </Button>

          <span className="text-sm text-gray-600 dark:text-gray-400">
            {currentFilteredIndex + 1} / {filteredIndices.length}
          </span>

          <Button
            onClick={handleNext}
            disabled={currentFilteredIndex === filteredIndices.length - 1}
            variant="secondary"
          >
            Next
            <ChevronRight className="w-4 h-4 inline ml-1" />
          </Button>
        </div>
      </div>
    </Layout>
  );
}
