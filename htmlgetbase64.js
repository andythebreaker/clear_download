var base64ToImage = require('base64-to-image');
const regex = /(data:image\/jpeg;base64.+)\)/mg;

// Alternative syntax using RegExp constructor
// const regex = new RegExp('(data:image\\/jpeg;base64.+)\\)', 'mg')
var fs = require('fs');
fs.readdir('.', function (err, files) {
    if (err) throw err;
    files
        .filter(function (file) { return file.substr(-5) === '.html'; })
        .forEach(function (file) {
            fs.readFile(file, 'utf-8', function (err2, contents) { //inspectFile(contents); }); });
                //});
                //fs.readFile('TestFile.txt', function (err, data) {
                if (err2) throw err2;


                const str = contents.toString();//data.toString();
                let m;

                while ((m = regex.exec(str)) !== null) {
                    // This is necessary to avoid infinite loops with zero-width matches
                    if (m.index === regex.lastIndex) {
                        regex.lastIndex++;
                    }

                    // The result can be accessed through the `m`-variable.
                    m.forEach((match, groupIndex) => {
                        //console.log(`Found match, group ${groupIndex}: ${match}`);
                        console.log(`=>${groupIndex}; `);
                        if (groupIndex === 1) { base64ToImage(match, 'pic'); }
                    });
                }
                //console.log(data.toString());
                //});
            });
            //fs.rename(oldPath, newPath, callback)
        });
});