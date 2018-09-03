import path from 'path';
import express from 'express';

const app = express();

app.use(express.static('dist'));

app.get('/static/app.js', (req, res) => {
  res.sendFile(path.join(process.cwd(), __dirname, 'dist', 'app.js'));
});

app.get('/:player/', (req, res) => {
  res.sendFile(path.join(process.cwd(), __dirname, 'index.html'));
});
// TODO: fix: app.get('/:player', (req, res) => {res.redirect(`/${res.player}/`);});

app.get('/:player/authenticate', (req, res) => {
  if (req.query.password == 'secret') {
    res.send(JSON.stringify(['a', 'b', 'c']))
  } else {
    res.status(401).send('no');
  }
});

app.listen(5000, function () {
  console.log(`cwd = ${process.cwd()}`);
  console.log(`__dirname = ${__dirname}`);
  console.log(`__filename = ${__filename}`);
  console.log('listening on port 5000');
});
