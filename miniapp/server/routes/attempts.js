import express from 'express';
import { authenticateToken } from '../middleware/auth.js';
import { examLimiter } from '../middleware/rateLimiter.js';
import {
  validateAttemptCreation,
  validateAnswerSubmission,
  validateExamCompletion,
} from '../middleware/validator.js';

export function createAttemptRoutes(attemptController) {
  const router = express.Router();

  // All routes require authentication
  router.use(authenticateToken);

  // Get all attempts for current user
  router.get('/', (req, res) => attemptController.getAllAttempts(req, res));

  // Get stats by subject
  router.get('/stats', (req, res) => attemptController.getStats(req, res));

  // Get attempt by ID
  router.get('/:id', (req, res) => attemptController.getAttemptById(req, res));

  // Create new attempt
  router.post('/', validateAttemptCreation, (req, res) => attemptController.createAttempt(req, res));

  // Submit answer for an attempt (with rate limiting for rapid submissions)
  router.post('/:attemptId/answer', examLimiter, validateAnswerSubmission, (req, res) => attemptController.submitAnswer(req, res));

  // Complete attempt
  router.post('/:attemptId/complete', validateExamCompletion, (req, res) => attemptController.completeAttempt(req, res));

  return router;
}
