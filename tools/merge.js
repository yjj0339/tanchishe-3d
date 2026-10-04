const fs = require('fs');
const html = fs.readFileSync('part1.html', 'utf8');
const code = fs.readFileSync('game.js', 'utf8');
if (!html.includes('/*__GAME_CODE__*/')) throw new Error('placeholder missing');
fs.writeFileSync('index.html', html.replace('/*__GAME_CODE__*/', code));
console.log('merged bytes', fs.statSync('index.html').size);
