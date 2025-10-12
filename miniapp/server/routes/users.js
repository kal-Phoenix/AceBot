import express from 'express';
import { authenticateToken } from '../middleware/auth.js';

export function createUserRoutes(userController) {
  const router = express.Router();

  // All routes require authentication
  router.use(authenticateToken);

  // Get current user
  router.get('/me', (req, res) => userController.getUser(req, res));

  // Select stream (one-time only)
  router.post('/stream', (req, res) => userController.selectStream(req, res));

  // Get stream selection status
  router.get('/stream/status', (req, res) => userController.getStreamStatus(req, res));

  // Admin endpoint for forcing stream changes (add admin auth middleware in production)
  router.post('/stream/force', (req, res) => userController.forceUpdateStream(req, res));

  // Update stats
  router.patch('/stats', (req, res) => userController.updateStats(req, res));

  // Reset user data
  router.post('/reset', (req, res) => userController.resetData(req, res));

  // Leaderboard routes
  router.get('/leaderboard', (req, res) => userController.getLeaderboard(req, res));
  router.get('/rank', (req, res) => userController.getUserRank(req, res));

  return router;
}
