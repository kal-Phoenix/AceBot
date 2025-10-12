import express from 'express';
import { authenticateToken } from '../middleware/auth.js';
import { loadExamsFromJSON, getFilteredExams, getExamById, getQuestionsForExam } from '../utils/examLoader.js';

// Mock data store (in-memory)
const mockUsers = new Map();
const mockAttempts = [];

// Load exams from JSON files
let allExams = [];
try {
  allExams = loadExamsFromJSON();
} catch (error) {
  console.error('Failed to load exams:', error);
}

// Create mock routes for when database is not available
export function createMockRoutes() {
  const router = express.Router();

  // Mock Users Routes
  router.post('/users/stream', authenticateToken, (req, res) => {
    const { stream } = req.body;
    const telegramId = req.user.telegram_id;
    
    console.log('Stream selection request:', { stream, telegramId });
    
    if (!stream || !['natural', 'social'].includes(stream)) {
      return res.status(400).json({ error: 'Invalid stream. Must be "natural" or "social"' });
    }
    
    // Get existing user or create new one
    let user = mockUsers.get(telegramId);
    if (!user) {
      user = { 
        telegram_id: telegramId,
        profile_picture: req.user.profile_picture || null,
        stats: {
          total_exams_taken: 0,
          total_practice_sessions: 0,
          average_score: 0,
          best_subject: null,
          weakest_subject: null,
          total_time_spent: 0,
        }
      };
    }
    
    console.log('Current user before stream selection:', user);
    
    // Check if stream is already selected
    if (user.stream) {
      console.log('Stream already selected, rejecting request');
      return res.status(400).json({ 
        error: 'Stream has already been selected and cannot be changed. Contact admin if needed.',
        code: 'STREAM_ALREADY_SELECTED'
      });
    }
    
    // Set stream with timestamp
    user.stream = stream;
    user.stream_selected_at = new Date();
    user.updated_at = new Date();
    mockUsers.set(telegramId, user);
    
    console.log('Stream selected successfully, updated user:', user);
    
    res.json({ 
      message: 'Stream selected successfully. This selection is permanent.',
      user: { ...user, id: telegramId, full_name: req.user.full_name },
      permanent: true
    });
  });

  router.get('/users/stream/status', authenticateToken, (req, res) => {
    const telegramId = req.user.telegram_id;
    const user = mockUsers.get(telegramId) || { telegram_id: telegramId };
    
    res.json({
      hasStream: !!user.stream,
      stream: user.stream || null,
      streamSelectedAt: user.stream_selected_at || null,
      canChange: false
    });
  });

  // Admin endpoint for forcing stream changes
  router.post('/users/stream/force', authenticateToken, (req, res) => {
    const { telegramId, stream } = req.body;
    
    if (!telegramId || !stream || !['natural', 'social'].includes(stream)) {
      return res.status(400).json({ error: 'Invalid parameters' });
    }
    
    const user = mockUsers.get(telegramId) || { telegram_id: telegramId };
    user.stream = stream;
    user.stream_selected_at = new Date();
    user.updated_at = new Date();
    mockUsers.set(telegramId, user);
    
    res.json({ 
      message: 'Stream forcefully updated by admin',
      user: { ...user, id: telegramId, full_name: req.user.full_name }
    });
  });

  router.get('/users/me', authenticateToken, (req, res) => {
    const telegramId = req.user.telegram_id;
    
    // Check if user exists in mock storage
    let user = mockUsers.get(telegramId);
    
    if (!user) {
      // Create new user and store it
      user = {
        telegram_id: telegramId,
        stream: null,
        profile_picture: req.user.profile_picture || null,
        stats: {
          total_exams_taken: 0,
          total_practice_sessions: 0,
          average_score: 0,
          best_subject: null,
          weakest_subject: null,
          total_time_spent: 0,
        }
      };
      mockUsers.set(telegramId, user);
      console.log('Created new mock user:', user);
    } else {
      console.log('Found existing mock user:', user);
    }
    
    res.json({
      id: telegramId,
      telegram_id: telegramId,
      username: req.user.username,
      full_name: req.user.full_name,
      profile_picture: user.profile_picture || req.user.profile_picture || null,
      ...user
    });
  });

  router.post('/users/reset', authenticateToken, (req, res) => {
    const telegramId = req.user.telegram_id;
    mockUsers.delete(telegramId);
    res.json({ message: 'User data reset successfully' });
  });

  router.get('/users/leaderboard', authenticateToken, (req, res) => {
    const { stream, limit = 50 } = req.query;
    
    // Convert mock users to array and filter
    const users = Array.from(mockUsers.values())
      .filter(user => user.stream === (stream || user.stream))
      .filter(user => user.stats?.total_exams_taken > 0)
      .map(user => ({
        ...user,
        id: user.telegram_id,
        leaderboard_score: (user.stats?.average_score * 0.7) + (user.stats?.total_exams_taken * 2) + (user.stats?.total_practice_sessions / 10)
      }))
      .sort((a, b) => b.leaderboard_score - a.leaderboard_score)
      .slice(0, parseInt(limit))
      .map((user, index) => ({
        ...user,
        rank: index + 1
      }));

    res.json(users);
  });

  router.get('/users/rank', authenticateToken, (req, res) => {
    const telegramId = req.user.telegram_id;
    const user = mockUsers.get(telegramId);
    
    if (!user || !user.stats?.total_exams_taken) {
      return res.json({ 
        message: 'User has not taken any exams yet',
        rank: null,
        total_users: 0,
        score: 0
      });
    }

    const userScore = (user.stats.average_score * 0.7) + (user.stats.total_exams_taken * 2) + (user.stats.total_practice_sessions / 10);
    
    // Count users with better scores
    const usersAhead = Array.from(mockUsers.values())
      .filter(u => u.stream === user.stream && u.stats?.total_exams_taken > 0)
      .filter(u => {
        const score = (u.stats.average_score * 0.7) + (u.stats.total_exams_taken * 2) + (u.stats.total_practice_sessions / 10);
        return score > userScore;
      }).length;

    const totalUsers = Array.from(mockUsers.values())
      .filter(u => u.stream === user.stream && u.stats?.total_exams_taken > 0).length;

    res.json({
      rank: usersAhead + 1,
      total_users: totalUsers,
      score: userScore
    });
  });

  // Mock Exams Routes
  router.get('/exams', authenticateToken, (req, res) => {
    // Return exams from JSON with filters
    const filters = {
      exam_type: req.query.exam_type,
      subject: req.query.subject,
      stream: req.query.stream,
      year: req.query.year,
    };
    
    const filtered = getFilteredExams(allExams, filters);
    
    // Add _id field (using array index)
    const examsWithIds = filtered.map((exam, index) => ({
      ...exam,
      _id: index.toString(),
      total_questions: exam.questions?.length || 0,
    }));
    
    res.json(examsWithIds);
  });

  router.get('/exams/subjects', authenticateToken, (req, res) => {
    const { stream } = req.query;
    const subjects = stream === 'natural'
      ? ['English', 'Maths', 'SAT', 'Chemistry', 'Biology', 'Physics']
      : ['English', 'Maths', 'SAT', 'History', 'Geography', 'Economics'];
    res.json(subjects);
  });

  router.get('/exams/type/:examType/subject/:subject', authenticateToken, (req, res) => {
    const { examType, subject } = req.params;
    const { stream, year } = req.query;
    
    const filters = {
      exam_type: examType,
      subject: subject,
      stream: stream,
      year: year,
    };
    
    const filtered = getFilteredExams(allExams, filters);
    
    // Add _id field
    const examsWithIds = filtered.map((exam, index) => ({
      ...exam,
      _id: allExams.indexOf(exam).toString(),
      total_questions: exam.questions?.length || 0,
    }));
    
    res.json(examsWithIds);
  });

  router.get('/exams/:id', authenticateToken, (req, res) => {
    const exam = getExamById(allExams, req.params.id);
    
    if (!exam) {
      return res.status(404).json({ error: 'Exam not found' });
    }
    
    res.json({
      ...exam,
      _id: req.params.id,
      total_questions: exam.questions?.length || 0,
    });
  });

  router.get('/exams/:id/questions', authenticateToken, (req, res) => {
    const exam = getExamById(allExams, req.params.id);
    
    if (!exam) {
      return res.status(404).json({ error: 'Exam not found' });
    }
    
    const questions = getQuestionsForExam(exam);
    res.json(questions);
  });

  // Mock Attempts Routes
  router.get('/attempts', authenticateToken, (req, res) => {
    const telegramId = req.user.telegram_id;
    const userAttempts = mockAttempts.filter(a => a.telegram_id === telegramId);
    res.json(userAttempts);
  });

  router.get('/attempts/stats', authenticateToken, (req, res) => {
    res.json([]);
  });

  router.get('/attempts/:id', authenticateToken, (req, res) => {
    const attempt = mockAttempts.find(a => a._id === req.params.id);
    if (attempt) {
      res.json(attempt);
    } else {
      res.status(404).json({ error: 'Attempt not found' });
    }
  });

  router.post('/attempts', authenticateToken, (req, res) => {
    const attempt = {
      _id: Date.now().toString(),
      telegram_id: req.user.telegram_id,
      ...req.body,
      started_at: new Date(),
      completed_at: null,
      status: 'in_progress',
      answers: [],
    };
    mockAttempts.push(attempt);
    res.status(201).json(attempt);
  });

  router.post('/attempts/:id/answer', authenticateToken, (req, res) => {
    const attempt = mockAttempts.find(a => a._id === req.params.id);
    if (attempt) {
      attempt.answers.push(req.body);
      res.json(attempt);
    } else {
      res.status(404).json({ error: 'Attempt not found' });
    }
  });

  router.post('/attempts/:id/complete', authenticateToken, (req, res) => {
    const attempt = mockAttempts.find(a => a._id === req.params.id);
    if (attempt) {
      attempt.completed_at = new Date();
      attempt.status = 'completed';
      attempt.answers = req.body.answers;
      attempt.score = req.body.answers.reduce((sum, a) => sum + a.points_earned, 0);
      attempt.total_points = attempt.score;
      attempt.max_points = req.body.max_points;
      attempt.percentage = Math.round((attempt.score / req.body.max_points) * 100);
      attempt.time_spent_seconds = req.body.time_spent_seconds;
      res.json(attempt);
    } else {
      res.status(404).json({ error: 'Attempt not found' });
    }
  });

  return router;
}
