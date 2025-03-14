import express from 'express';
import path from 'path';
import { generateReceipt } from './services/receiptGenerator';

const app = express();
const port = 3000;

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

// Start the server
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
}); 