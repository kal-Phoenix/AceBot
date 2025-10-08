# Development Guide

## Testing Without Telegram

Since this is a Telegram Mini App, testing in a regular browser requires some modifications.

### Option 1: Mock Telegram User (Recommended for Development)

Update `src/lib/telegram.ts` temporarily:

```typescript
getUser(): TelegramUser | null {
  // For development: return mock user
  if (import.meta.env.DEV) {
    return {
      id: 123456789,
      first_name: 'Test',
      last_name: 'User',
      username: 'testuser',
    };
  }

  const user = this.webApp.initDataUnsafe?.user;
  if (!user) return null;
  return {
    id: user.id,
    first_name: user.first_name,
    last_name: user.last_name,
    username: user.username,
    language_code: user.language_code,
    is_premium: user.is_premium,
  };
}
```

### Option 2: Use Telegram Web Dev Tools

1. Install: https://github.com/twa-dev/vite-plugin-telegram
2. Add to `vite.config.ts`
3. Use the browser extension for testing

## Database Setup

### 1. Create Supabase Project
1. Go to https://supabase.com
2. Create new project
3. Copy URL and anon key to `.env`

### 2. Run Migration
The migration was already applied via the MCP tool. Verify tables exist:
- users
- exam_attempts
- practice_sessions
- user_progress
- leaderboard
- question_reports

### 3. Test Database Connection
```bash
npm run dev
```
Check browser console for any connection errors.

## Adding Real Questions

Currently, there are only 8 sample questions. To add 1M questions:

### Structure
```typescript
{
  id: 'nat_eng_9_2024_001',
  stream: 'Natural',
  subject: 'English',
  grade: 9,
  topic: 'Grammar',
  year: 2024,
  difficulty: 'easy',
  questionText: 'Your question here',
  options: [
    { text: 'Option A' },
    { text: 'Option B' },
    { text: 'Option C' },
    { text: 'Option D' },
  ],
  correctAnswer: 0, // index of correct option
  hint: 'Helpful hint',
  explanation: 'Detailed explanation',
}
```

### Best Practices
1. Use consistent ID format: `{stream}_{subject}_{grade}_{year}_{number}`
2. Keep questions under 200 characters
3. Provide clear, helpful hints
4. Write detailed explanations
5. Test each question thoroughly

### Large-Scale Question Management

For 1M questions:
1. Split into separate files by subject/grade
2. Use dynamic imports
3. Consider moving to database if needed
4. Implement search/filter optimization

## Telegram Bot Setup

### 1. Create Bot
1. Open @BotFather in Telegram
2. Create new bot: `/newbot`
3. Save bot token

### 2. Set Menu Button
```
/setmenubutton
Select your bot
Add Button
Text: "Open Exam Platform"
URL: https://your-app-url.vercel.app
```

### 3. Configure Mini App
```
/newapp
Select your bot
Add app details
Upload icon (512x512 PNG)
Set web app URL
```

## Deployment

### Vercel (Recommended)
```bash
npm install -g vercel
vercel login
vercel
```

### Environment Variables in Vercel
Add in project settings:
- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`

### Post-Deployment
1. Update Telegram bot URL
2. Test in Telegram
3. Monitor Supabase usage
4. Check error logs

## Performance Optimization

### For 10K Users
1. Enable Supabase connection pooling
2. Add Redis caching (if needed)
3. Use CDN for images
4. Optimize bundle size
5. Enable compression

### Monitoring
- Supabase dashboard for queries
- Vercel analytics for traffic
- Browser console for errors

## Common Issues

### Issue: "User not authenticated"
- Check Supabase RLS policies
- Verify `.env` variables
- Check browser console

### Issue: Questions not loading
- Verify question data format
- Check imports
- Ensure filter logic works

### Issue: Leaderboard not updating
- Run `update_leaderboard_rankings()` function
- Check database triggers
- Verify RLS policies

## Testing Checklist

- [ ] User registration works
- [ ] Exam mode timer works
- [ ] Practice mode gives immediate feedback
- [ ] Red flags prevent submission
- [ ] Leaderboard updates correctly
- [ ] Progress tracking accurate
- [ ] Question reporting works
- [ ] Theme toggle works
- [ ] Mobile responsive
- [ ] Dark mode works

## Next Steps

1. Add more questions (expand from 8 sample questions)
2. Implement image uploads for questions
3. Add admin panel for question management
4. Implement analytics dashboard
5. Add push notifications
6. Create study streak tracking
7. Add social sharing features
8. Implement peer-to-peer challenges
