import express from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import crypto from 'crypto';
import { ObjectId } from 'mongodb';
import { getDatabase } from '../config/database.js';
import { authenticateToken } from '../middleware/auth.js';
import { UserModel } from '../models/User.js';

const router = express.Router();

// Initialize user model (will be set when database connects)
let userModel = null;

export function setUserModel(model) {
  userModel = model;
}

// Validate Telegram WebApp data
function validateTelegramWebAppData(initData, botToken) {
  const urlParams = new URLSearchParams(initData);
  const hash = urlParams.get('hash');
  urlParams.delete('hash');
  
  const dataCheckString = Array.from(urlParams.entries())
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([key, value]) => `${key}=${value}`)
    .join('\n');
  
  const secretKey = crypto
    .createHmac('sha256', 'WebAppData')
    .update(botToken)
    .digest();
  
  const calculatedHash = crypto
    .createHmac('sha256', secretKey)
    .update(dataCheckString)
    .digest('hex');
  
  return calculatedHash === hash;
}

// Telegram authentication endpoint
router.post('/telegram-auth', async (req, res) => {
  try {
    const { initData, user } = req.body;

    if (!user || !user.id) {
      return res.status(400).json({ error: 'Invalid Telegram user data' });
    }

    // In production, validate initData with your bot token
    // const isValid = validateTelegramWebAppData(initData, process.env.BOT_TOKEN);
    // if (!isValid) {
    //   return res.status(401).json({ error: 'Invalid Telegram data' });
    // }

    const telegramUserId = user.id.toString();
    const fullName = `${user.first_name || ''} ${user.last_name || ''}`.trim() || 'Telegram User';
    const username = user.username || null;
    const photoUrl = user.photo_url || null;

    // Check if user exists in database, create if not
    let dbUser = null;
    if (userModel) {
      dbUser = await userModel.findByTelegramId(telegramUserId);
      
      if (!dbUser) {
        // Create new user
        dbUser = await userModel.create({
          telegram_id: telegramUserId,
          username: username,
          first_name: user.first_name,
          last_name: user.last_name,
          full_name: fullName,
          profile_picture: photoUrl,
        });
      }
    }

    // Generate JWT token with Telegram user_id
    const token = jwt.sign(
      { 
        telegram_id: telegramUserId,
        username: username,
        full_name: fullName,
        profile_picture: photoUrl,
        type: 'telegram'
      },
      process.env.JWT_SECRET || 'dev-secret-key',
      { expiresIn: '30d' }
    );

    res.json({
      user: dbUser || {
        id: telegramUserId,
        telegram_id: telegramUserId,
        username: username,
        full_name: fullName,
        profile_picture: photoUrl,
        stream: null,
      },
      token,
    });
  } catch (error) {
    console.error('Telegram auth error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get current user - Updated for Telegram
router.get('/me', authenticateToken, async (req, res) => {
  try {
    const telegramId = req.user.telegram_id;
    
    // Try to get user from database if userModel is available
    if (userModel) {
      const dbUser = await userModel.findByTelegramId(telegramId);
      if (dbUser) {
        return res.json(dbUser);
      }
    }
    
    // Fallback to token data if database is not available
    res.json({
      id: req.user.telegram_id || req.user.id,
      telegram_id: req.user.telegram_id,
      username: req.user.username,
      full_name: req.user.full_name || 'Telegram User',
      profile_picture: req.user.profile_picture || null,
      stream: null,
      created_at: new Date().toISOString(),
    });
  } catch (error) {
    console.error('Get user error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Sign out (client-side only, just return success)
router.post('/signout', (req, res) => {
  res.json({ message: 'Signed out successfully' });
});

export default router;
