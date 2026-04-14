import express from 'express';
import { authenticateToken } from '../middleware/auth.js';
import { cacheMiddleware } from '../utils/cache.js';
import { validateExamQuery, validateExamId } from '../middleware/validator.js';

export function createExamRoutes(examController) {
  const router = express.Router();

  // All routes require authentication
  router.use(authenticateToken);

  // Get all exams (with optional filters) - cache for 10 minutes
  router.get('/', validateExamQuery, cacheMiddleware(600), (req, res) => 
    examController.getAllExams(req, res)
  );

  // Get subjects by stream - cache for 15 minutes (rarely changes)
  router.get('/subjects', validateExamQuery, cacheMiddleware(900), (req, res) => 
    examController.getSubjects(req, res)
  );

  // Get exams by type and subject - cache for 10 minutes
  router.get('/type/:examType/subject/:subject', cacheMiddleware(600), (req, res) => 
    examController.getExamsByTypeAndSubject(req, res)
  );

  // Get exam by ID - cache for 15 minutes
  router.get('/:id', validateExamId, cacheMiddleware(900), (req, res) => 
    examController.getExamById(req, res)
  );

  // Get questions for an exam - cache for 15 minutes
  router.get('/:id/questions', validateExamId, cacheMiddleware(900), (req, res) => 
    examController.getQuestions(req, res)
  );

  // Create new exam (admin only - can add auth check later)
  router.post('/', (req, res) => examController.createExam(req, res));

  return router;
}
