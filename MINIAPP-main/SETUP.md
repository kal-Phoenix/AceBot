# Quick Setup Guide

## 🚀 Getting Started in 5 Minutes

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Environment
Your Supabase credentials are already in `.env` file. Verify they're correct:
```bash
cat .env
```

### 3. Verify Database
The database tables have been created automatically. You should see:
- users
- exam_attempts
- practice_sessions
- user_progress
- leaderboard
- question_reports

### 4. Start Development
```bash
npm run dev
```

The app will open at `http://localhost:5173`

## ⚠️ Important Notes

### Testing Without Telegram
The app is built for Telegram Mini App. To test in a regular browser:

**Option A: Mock User (Quick Test)**
The app will show "Please open this app in Telegram" message in browser. To bypass for testing:

1. Open `src/lib/telegram.ts`
2. Find the `getUser()` method
3. Temporarily add:
```typescript
getUser(): TelegramUser | null {
  // DEV ONLY: Mock user for testing
  if (import.meta.env.DEV) {
    return {
      id: 123456789,
      first_name: 'Test',
      last_name: 'User',
      username: 'testuser',
    };
  }
  // ... rest of code
}
```

**Option B: Test in Telegram**
1. Create a Telegram Bot via @BotFather
2. Set up Mini App
3. Deploy to Vercel/Netlify
4. Add URL to bot

## 📝 What's Included

### ✅ Fully Working Features
- User authentication via Telegram
- Exam mode (timed, scored, leaderboard)
- Practice mode (untimed, immediate feedback)
- Progress tracking
- Leaderboard with top 100
- Question hints & flags
- Dark/Light theme
- Review answers
- Report questions
- Mobile responsive

### ⚠️ Sample Data
Currently includes **8 sample questions** for testing:
- Natural: English, Maths, Chemistry, Biology, Physics
- Social: History, Geography, Economics

**You need to add more questions** to reach 1M target!

## 📦 What to Do Next

### Immediate (Before Production)
1. **Add Questions**: Expand from 8 to thousands/millions
2. **Test All Flows**: Exam, Practice, Review, Leaderboard
3. **Configure Time Limits**: Set per-exam time limits in config
4. **Add Question Images**: Upload to Supabase Storage

### Deployment
1. **Build**: `npm run build`
2. **Deploy to Vercel**: `vercel` (or Netlify)
3. **Set Environment Variables**: Add VITE_SUPABASE_* keys
4. **Test in Production**: Verify Supabase connection works

### Telegram Bot Setup
1. Create bot via @BotFather
2. Set menu button to app URL
3. Test in Telegram
4. Invite beta testers

## 🎯 Key Files to Know

### Questions
- `/src/data/sampleQuestions.ts` - Add questions here
- `/src/types/question.types.ts` - Question structure

### Pages
- `/src/pages/Home.tsx` - Main dashboard
- `/src/pages/QuestionInterface.tsx` - Question display
- `/src/pages/Leaderboard.tsx` - Rankings
- `/src/pages/Progress.tsx` - User stats

### Database
- Schema defined in migration (already applied)
- RLS policies enabled for security
- Triggers auto-update stats

## 🐛 Troubleshooting

### Build Fails
```bash
rm -rf node_modules
npm install
npm run build
```

### Database Issues
- Check `.env` has correct Supabase credentials
- Verify tables exist in Supabase dashboard
- Check RLS policies are enabled

### No Questions Showing
- Verify questions in `sampleQuestions.ts`
- Check filter logic in selection pages
- Console log question arrays

## 📞 Need Help?

Read detailed guides:
- `README.md` - Full feature overview
- `DEVELOPMENT.md` - Detailed dev guide
- Check browser console for errors
- Review Supabase logs for database issues

## 🎉 You're Ready!

The platform is fully built and working. Add your questions and deploy!
