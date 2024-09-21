const path = require('path');
const fs = require('fs');
const a4pic2pdf = require('a4pic2pdf');

// Check if there are enough command line arguments
if (process.argv.length < 6) {
    console.log('Usage: node script.js imgInputDir outputDir pdfFilename imgPrefix');
    process.exit(1);
}

// Get the command line arguments
const imgInputDir = process.argv[2];
const outputDir = process.argv[3];
const pdfFilename = process.argv[4];
const imgPrefix = process.argv[5]; // New argument for image filename prefix

// Filter and select only files with the specified extensions and prefix
const allowedExtensions = ['.jpg', '.jpeg', '.png', '.webm'];
const filesToUpload = fs.readdirSync(imgInputDir)
    .filter(file => allowedExtensions.includes(path.extname(file).toLowerCase()) && path.basename(file).startsWith(imgPrefix))
    .map(file => path.join(imgInputDir, file));

if (filesToUpload.length === 0) {
    console.log(`No files found with prefix "${imgPrefix}" in the specified directory.`);
    process.exit(1);
}

const outputLocationDir = path.join(process.cwd(), outputDir);

a4pic2pdf(filesToUpload, outputLocationDir, pdfFilename);
