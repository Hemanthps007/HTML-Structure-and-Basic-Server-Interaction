
const express = require("express");
const app = express();

app.use(express.urlencoded({ extended: true }));
app.use(express.static("public"));

app.set("view engine", "ejs");

let users = [];

app.get("/", (req, res) => {
    res.render("index", { users });
});

app.post("/submit", (req, res) => {
    const { name, email } = req.body;
    users.push({ name, email });
    res.redirect("/");
});

app.listen(3000, () => {
    console.log("Server running on http://localhost:3000");
});
