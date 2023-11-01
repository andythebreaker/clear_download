const path = require('path');
const fs = require('fs');

const a4pic2pdf = require('a4pic2pdf');

// Check if there are enough command line arguments
if (process.argv.length < 5) {
    console.log('Usage: node script.js imgInputDir outputDir pdfFilename');
    process.exit(1);
}

// Get the command line arguments
const imgInputDir = process.argv[2];
const outputDir = process.argv[3];
const pdfFilename = process.argv[4];

// Filter and select only files with the specified extensions
const allowedExtensions = ['.jpg', '.jpeg', '.png', '.webm'];
const filesToUpload = fs.readdirSync(imgInputDir)
    .filter(file => allowedExtensions.includes(path.extname(file).toLowerCase()))
    .map(file => path.join(imgInputDir, file));

const outputLocationDir = path.join(process.cwd(), outputDir);

a4pic2pdf(filesToUpload, outputLocationDir, pdfFilename);

  
