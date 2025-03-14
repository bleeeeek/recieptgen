import express from 'express';
import path from 'path';
import { generateReceipt } from './services/receiptGenerator';

const app = express();
// Use environment port or default to 3000
const port = process.env.PORT || 3000;

// Set up EJS as the view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'templates'));

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, '../public')));

// Main route
app.get('/', (req, res) => {
  const receiptData = generateReceipt();
  res.render('receipt', receiptData);
});

// Health check endpoint for Vercel
app.get('/api/health', (req, res) => {
  res.status(200).send('OK');
});

// Start the server
if (process.env.NODE_ENV !== 'production') {
  app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
  });
}

// Export for Vercel serverless deployment
export default app; 