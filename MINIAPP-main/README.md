# Exam Platform - Telegram Mini App

A comprehensive exam and practice platform built as a Telegram Mini App with React, TypeScript, and Supabase.

## Features

### 🎯 Dual Mode System
- **Exam Mode**: Timed exams with leaderboard integration
- **Practice Mode**: Untimed practice with immediate feedback

### 📚 Content Organization
- **2 Streams**: Natural Sciences & Social Sciences
- **12 Subjects**: 6 per stream
- **4 Grade Levels**: Grades 9-12
- **Multiple Years**: Past exam papers from 2020-2024

### 🎮 Interactive Features
- Hint system (no penalty)
- Red flag marking for questions
- Question grid navigation
- Detailed explanations
- Question reporting system

### 📊 Progress Tracking
- Overall accuracy tracking
- Subject-wise performance
- Practice question count
- Exam history

### 🏆 Leaderboard
- Top 100 global rankings
- Badges for top 3 performers
- Real-time rank updates
- First attempt scoring

### 🎨 Design
- Light/Dark theme toggle
- Responsive mobile-first design
- Clean, professional interface
- Smooth animations

## Tech Stack

- **Frontend**: React 18 + TypeScript + Vite
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Database**: Supabase (PostgreSQL)
- **Authentication**: Telegram Mini App SDK
- **Deployment**: Vercel/Netlify (free tier)

## Setup

### Prerequisites
1. Node.js 18+
2. Supabase account
3. Telegram Bot (for mini app)

### Environment Variables
Create a `.env` file:

```env
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

### Build

```bash
npm run build
```

## Database Schema

The app uses the following tables:
- `users` - User profiles and statistics
- `exam_attempts` - Exam submissions and scores
- `practice_sessions` - Practice activity
- `user_progress` - Subject-specific progress
- `leaderboard` - Cached rankings
- `question_reports` - User-reported issues

All tables have Row Level Security (RLS) enabled.

## Adding Questions

Questions are stored in `/src/data/sampleQuestions.ts`. To add more questions:

1. Follow the `Question` interface in `/src/types/question.types.ts`
2. Add questions to the `sampleQuestions` array
3. Questions support:
   - Text and images
   - 4 multiple choice options
   - Hints and explanations
   - Difficulty levels
   - Topic categorization

## Key Features Implementation

### Red Flag Blocking
- Users cannot submit exams if red-flagged questions are unanswered
- Warning appears on submission attempt

### Leaderboard Logic
- Only first exam attempt counts
- Rankings based on overall accuracy
- Top 3 receive special badges
- Updates automatically via database triggers

### Theme System
- Syncs with Telegram theme
- Persistent user preference
- System-wide dark mode support

## Performance Considerations

- Optimized for 10,000+ concurrent users
- Lazy loading of question sets
- Database indexes on critical queries
- Cached leaderboard data

## License

MIT

## Support

For issues or questions, please open a GitHub issue.
