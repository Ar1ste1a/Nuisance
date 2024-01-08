const express = require('express')
const payments = require('./payments')
const pdf = require('./pdf')
const app = express()
const port = 4011
const { v4: uuidv4 } = require('uuid');
const { readFile } = require('fs/promises')
const path = require('node:path');
const cookieParser = require('cookie-parser')

var quote = null

app.use(express.urlencoded({extended: true}));
app.use(express.static('static'))
app.use(cookieParser())

app.get('/', (req, res) => {
  res.sendFile('index.html', { root: path.join(__dirname, 'templates')})
})

app.get('/create', (req, res) => {
    res.sendFile('create.html', { root: path.join(__dirname, 'templates')})
})

app.post('/quote', async (req, res) => {
  let bonusRate = 100
  let id = uuidv4();

  let total = 2134

  //TODO: add this bonus value to quote
  let pdffile = await pdf.renderPdf(req.body)
  res.setHeader('Content-Type', 'application/pdf');
  res.setHeader('Content-Disposition', 'inline; filename=invoice.pdf')
  return res.send(pdffile)
})

app.get('/renderQuote', async (req, res) => {
  if (!quote) {
    quote = await readFile('templates/quote.html', 'utf8')
  }

  let html = quote
  .replaceAll("{{ name }}", req.query.name)
  .replaceAll("{{ address }}", req.query.address)
  .replaceAll("{{ phone }}", req.query.phone)
  .replaceAll("{{ email }}", req.query.email)
  .replaceAll("{{ role }}", req.query.role)
  res.setHeader("Content-Type", "text/html")
  res.setHeader("Content-Security-Policy", "default-src 'unsafe-inline' maxcdn.bootstrapcdn.com; object-src 'none'; script-src 'none'; img-src 'self' dummyimage.com;")
  res.send(html)
})

app.get('/secret', (req, res) => {
  if (req.socket.remoteAddress != "::ffff:127.0.0.1") {
    return res.send("err1")
  }
  if (req.cookies['bot']) {
    return res.send("err2")
  }
  res.setHeader('X-Frame-Options', 'none');
  res.send('secret')
})

app.listen(port, () => {
  console.log(`Nuisance Quote app listening on port ${port}`)
})
