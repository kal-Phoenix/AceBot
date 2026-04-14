import { body, param, query, validationResult } from 'express-validator';
import { validationError } from '../utils/response.js';

// Middleware to check validation results
export const validate = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return validationError(res, errors);
  }
  next();
};

// Validation rules for different endpoints

export const validateStreamSelection = [
  body('stream')
    .isIn(['natural', 'social'])
    .withMessage('Stream must be either "natural" or "social"'),
  validate,
];

export const validateAttemptCreation = [
  body('exam_id')
    .isString()
    .trim()
    .notEmpty()
    .withMessage('Exam ID is required'),
  body('exam_title')
    .isString()
    .trim()
    .notEmpty()
    .withMessage('Exam title is required'),
  body('exam_type')
    .isIn(['past', 'mock', 'model'])
    .withMessage('Invalid exam type'),
  body('subject')
    .isString()
    .trim()
    .notEmpty()
    .withMessage('Subject is required'),
  body('mode')
    .isIn(['practice', 'exam'])
    .withMessage('Mode must be either "practice" or "exam"'),
  body('max_points')
    .isInt({ min: 0 })
    .withMessage('Max points must be a positive integer'),
  validate,
];

export const validateAnswerSubmission = [
  param('attemptId')
    .isString()
    .trim()
    .notEmpty()
    .withMessage('Attempt ID is required'),
  body('question_id')
    .isString()
    .trim()
    .notEmpty()
    .withMessage('Question ID is required'),
  body('question_number')
    .isInt({ min: 1 })
    .withMessage('Question number must be a positive integer'),
  body('selected_answer')
    .isIn(['A', 'B', 'C', 'D'])
    .withMessage('Selected answer must be A, B, C, or D'),
  body('correct_answer')
    .isIn(['A', 'B', 'C', 'D'])
    .withMessage('Correct answer must be A, B, C, or D'),
  body('points')
    .isInt({ min: 0 })
    .withMessage('Points must be a positive integer'),
  validate,
];

export const validateExamCompletion = [
  param('attemptId')
    .isString()
    .trim()
    .notEmpty()
    .withMessage('Attempt ID is required'),
  body('time_spent_seconds')
    .isInt({ min: 0 })
    .withMessage('Time spent must be a positive integer'),
  body('answers')
    .isArray()
    .withMessage('Answers must be an array'),
  validate,
];

export const validateExamQuery = [
  query('stream')
    .optional()
    .isIn(['natural', 'social'])
    .withMessage('Stream must be either "natural" or "social"'),
  validate,
];

export const validateExamId = [
  param('id')
    .isString()
    .trim()
    .notEmpty()
    .withMessage('Exam ID is required'),
  validate,
];
