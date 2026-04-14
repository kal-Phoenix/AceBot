import { MongoClient } from 'mongodb';
import dotenv from 'dotenv';

dotenv.config();

const uri = process.env.MONGODB_URI;
let client;
let db;

if (uri) {
  // Configure MongoDB client with SSL options
  client = new MongoClient(uri, {
    tls: true,
    tlsAllowInvalidCertificates: false,
    tlsAllowInvalidHostnames: false,
    serverSelectionTimeoutMS: 5000,
    connectTimeoutMS: 10000,
  });
}

export async function connectToDatabase() {
  if (!uri) {
    console.warn('⚠️  MONGODB_URI not configured - running in mock mode');
    return null;
  }

  try {
    await client.connect();
    console.log('✅ Connected to MongoDB Atlas');
    db = client.db();
    return db;
  } catch (error) {
    console.error('❌ MongoDB connection error:', error.message);
    console.warn('⚠️  Continuing in fallback mode without database');
    return null;
  }
}

export function getDatabase() {
  if (!db) {
    throw new Error('Database not initialized. Call connectToDatabase first.');
  }
  return db;
}

export { client };
