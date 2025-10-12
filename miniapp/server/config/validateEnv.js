/**
 * Environment variable validation
 * Ensures all required environment variables are present before starting the server
 */

export function validateEnv() {
  const required = ['JWT_SECRET'];
  const missing = [];

  for (const key of required) {
    if (!process.env[key]) {
      missing.push(key);
    }
  }

  if (missing.length > 0) {
    console.error('❌ Missing required environment variables:');
    missing.forEach(key => console.error(`   - ${key}`));
    console.error('\n💡 Please create a .env file in the server directory with:');
    console.error('   PORT=3001');
    console.error('   MONGODB_URI=your_mongodb_connection_string');
    console.error('   JWT_SECRET=your_secret_key');
    console.error('   BOT_TOKEN=your_telegram_bot_token\n');
    throw new Error('Missing required environment variables');
  }

  // Warn about optional but recommended variables
  if (!process.env.MONGODB_URI) {
    console.warn('⚠️  MONGODB_URI not set - running in MOCK mode');
  }

  console.log('✅ Environment variables validated');
}
