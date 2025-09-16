const express = require("express");
const bodyParser = require("body-parser");
const crypto = require("crypto");
const bot = require("./bot");

const app = express();
const PORT = 3000;

let notes = [];
app.use(bodyParser.urlencoded({ extended: true }));
function escapeHTML(str) {
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
}
app.use((req, res, next) => {
    const nonce = crypto.randomBytes(16).toString("hex");
    res.locals.nonce=nonce;
    res.setHeader("Content-Security-Policy", `
        default-src 'none';
        script-src 'nonce-${nonce}';
        style-src 'unsafe-inline';
    `.replace(/\n/g, "").trim());
    next();
});
app.get("/", (req, res) => {
    let listItems = notes.map((content, index) => {
        return `
        <li style="margin-bottom:15px;padding:10px;border:1px solid #ddd;border-radius:5px;background:#f9f9f9;">
            <a href="/note/${index}">Note ${index}</a>
            <div id='note-${index}' class="note-content"></div>
            <form action="/delete/${index}" method="POST" style="display:inline;">
                <button type="submit" style="margin-left:10px;background:#ff4d4f;color:white;border:none;border-radius:3px;cursor:pointer;">Delete</button>
            </form>
            <script src="/preview?index=${encodeURIComponent(index)}&content=${encodeURIComponent(content)}" nonce="${res.locals.nonce}"></script>
        </li>
        `;
    }).join("");

    res.send(`
    <html>
    <head>
        <title>📒 Notes</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            textarea { width: 400px; height: 80px; }
            button { margin-top: 5px; }
            ul { list-style: none; padding: 0; }
        </style>
    </head>
    <body>
        <h1>📒 Notes</h1>
        <form action="/add" method="POST">
            <textarea name="content"></textarea><br>
            <button type="submit">Add Note</button>
        </form>
        <hr>
        <ul>
            ${listItems}
        </ul>
    </body>
    </html>
    `);
});

app.get("/preview", (req, res) => {
    res.setHeader("Content-Type", "application/javascript");
    const index = req.query.index;
    let content = req.query.content || "";
    content=escapeHTML(content);
    const js = `
    (function(){
        const el = document.getElementById('note-${index}');
        if (!el) return;
        const text = '${content}';
        if (text.length > 50) {
            el.innerHTML = text.slice(0,50) + '...';
        } else {
            el.innerHTML = text;
        }
    })();
    `;
    res.send(js);
});

app.post("/add", (req, res) => {
    let content = (req.body.content || "").trim();
    if (content) notes.push(content);
    res.redirect("/");
});

app.get("/note/:id", (req, res) => {
    const id = parseInt(req.params.id);
    if (id >= 0 && id < notes.length) {
        res.send(`
            <h1>Note ${id}</h1>
            <p>${notes[id]}</p>
            <a href="/">Back</a>
            <form action="/delete/${id}" method="POST">
                <button type="submit">Delete this note</button>
            </form>
        `);
    } else {
        res.status(404).send("Note not found");
    }
});

app.post("/delete/:id", (req, res) => {
    const id = parseInt(req.params.id);
    if (id >= 0 && id < notes.length) notes.splice(id, 1);
    res.redirect("/");
});

app.post("/report", async (req, res) => {
    let url = req.body.url
    if (!url)
        return res.status(400).send("Missing url")

    if(typeof url !== "string")
        return res.status(400).send("Bad request")

    try {
        let result = await bot.visit(url)
        res.send("发送成功")
    } catch (err) {
        console.error(err)
        res.status(500).send("An error occurred")
    }
})

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
