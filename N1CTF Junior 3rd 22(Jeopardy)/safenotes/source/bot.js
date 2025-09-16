const puppeteer = require('puppeteer');
const FLAG = process.env.FLAG ?? 'flag{test}';
const HOST = 'localhost:3000';
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

const visit = async (url) => {
    const browser = await puppeteer.launch({
        executablePath:'/usr/bin/chromium',
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    await browser.setCookie({
        name: 'flag',
        value: FLAG,
        domain: HOST,
        path: '/',
        httpOnly: false
    });

    const page = await browser.newPage();

    await page.goto(url);
    await sleep(5000);
    await page.close();
}

module.exports = {visit};