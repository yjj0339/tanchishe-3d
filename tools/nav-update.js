const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const dir = path.resolve(__dirname, '..', '.tmp-nav');
function gh(args) {
  const r = spawnSync('gh', args, { encoding: 'utf8' });
  if (r.status !== 0) throw new Error(r.stderr);
  return r.stdout;
}
function put(file, contentPath, sha) {
  const body = JSON.stringify({ message: 'add tanchishe-3d card + qr', content: fs.readFileSync(contentPath).toString('base64'), sha });
  const bodyFile = path.join(dir, '_body.json');
  fs.writeFileSync(bodyFile, body);
  return JSON.parse(gh(['api', '-X', 'PUT', `repos/yjj0339/yjj0339.github.io/contents/${file}`, '--input', bodyFile])).content.sha;
}
const navSha = fs.readFileSync(path.join(dir, 'sha.txt'), 'utf8').trim();
console.log('index:', put('index.html', path.join(dir, 'index.html'), navSha).slice(0, 8));
console.log('qr:', put('qr-tanchishe-3d.png', path.resolve(__dirname, '..', 'qr-live.png')).slice(0, 8));
