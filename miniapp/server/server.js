import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';
import { connectToDatabase } from './config/database.js';
import { validateEnv } from './config/validateEnv.js';
import { createIndexes } from './config/indexes.js';
import logger from './utils/logger.js';
import { apiLimiter, authLimiter } from './middleware/rateLimiter.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

dotenv.config();

// Validate environment variables before starting
validateEnv();

import authRoutes, { setUserModel } from './routes/auth.js';
import { createUserRoutes } from './routes/users.js';
import { createExamRoutes } from './routes/exams.js';
import { createAttemptRoutes } from './routes/attempts.js';
import { createMockRoutes } from './routes/mockRoutes.js';
import { UserModel } from './models/User.js';
import { ExamModel } from './models/Exam.js';
import { AttemptModel } from './models/Attempt.js';
import { UserController } from './controllers/userController.js';
import { ExamController } from './controllers/examController.js';
import { AttemptController } from './controllers/attemptController.js';

const app = express();
const PORT = process.env.PORT || 8080;

// Middleware
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Serve static files from the React app
app.use(express.static(path.join(__dirname, 'public')));

// Request logging
app.use((req, res, next) => {
  logger.info(`${req.method} ${req.path}`, {
    ip: req.ip,
    userAgent: req.get('user-agent'),
  });
  next();
});

// Apply rate limiting to all API routes
app.use('/api/', apiLimiter);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', mode: res.locals.mode || 'unknown' });
});

// Start server with MVC architecture
async function startServer() {
  // Always setup auth routes first with stricter rate limiting
  app.use('/api/auth', authLimiter, authRoutes);

  try {
    // Try to connect to MongoDB
    const db = await connectToDatabase();
    
    if (db) {
      // Database connected - use full MVC architecture
      logger.info('✅ MongoDB connected - Full mode');
      console.log('✅ MongoDB connected - Full mode');
      
      // Initialize Models
      const userModel = new UserModel(db);
      const examModel = new ExamModel(db);
      const attemptModel = new AttemptModel(db);

      // Set user model for auth routes
      setUserModel(userModel);

      // Create database indexes for performance
      await createIndexes(db);

      // Initialize Controllers
      const userController = new UserController(userModel);
      const examController = new ExamController(examModel);
      const attemptController = new AttemptController(attemptModel, userModel);

      // Setup Routes
      app.use('/api/users', createUserRoutes(userController));
      app.use('/api/exams', createExamRoutes(examController));
      app.use('/api/attempts', createAttemptRoutes(attemptController));

      app.locals.mode = 'database';
      logger.info('📊 MVC architecture initialized');
      console.log('📊 MVC architecture initialized');
    } else {
      // No database - use mock routes
      logger.warn('⚠️  Running in MOCK mode (no database)');
      console.log('⚠️  Running in MOCK mode (no database)');
      console.log('💡 All data is temporary and stored in memory');
      
      // Setup mock routes
      app.use('/api', createMockRoutes());
      
      app.locals.mode = 'mock';
    }

    // Serve React app for all non-API routes (must be after API routes)
    app.get('*', (req, res) => {
      res.sendFile(path.join(__dirname, 'public', 'index.html'));
    });

    app.listen(PORT, () => {
      const mode = app.locals.mode === 'database' ? 'Full (with MongoDB)' : 'Mock (in-memory)';
      logger.info(`🚀 Server started on port ${PORT} in ${mode} mode`);
      console.log(`\n🚀 Server running on http://localhost:${PORT}`);
      console.log(`📍 Mode: ${mode}`);
      console.log(`\n✨ Ready to accept requests!\n`);
    });
  } catch (error) {
    logger.error('❌ Failed to start server:', error);
    console.error('❌ Failed to start server:', error);
    process.exit(1);
  }
}

// Global error handler
app.use((err, req, res, next) => {
  logger.error('Unhandled error:', {
    error: err.message,
    stack: err.stack,
    path: req.path,
    method: req.method,
  });
  
  res.status(err.status || 500).json({
    success: false,
    error: process.env.NODE_ENV === 'production' 
      ? 'Internal server error' 
      : err.message,
  });
});

// Handle unhandled promise rejections
process.on('unhandledRejection', (reason, promise) => {
  logger.error('Unhandled Rejection:', { reason, promise });
});

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  logger.error('Uncaught Exception:', error);
  process.exit(1);
});

startServer();
