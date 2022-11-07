const express = require("express");
//const multer = require("multer");
const app = express();
const cors = require("cors");
const bodyParser = require("body-parser");

// const storage = multer.diskStorage({
//   // eslint-disable-next-line object-shorthand
//   destination: function (req, file, cb) {
//     cb(null, path.join(__dirname, "./sqls/"));
//   },
//   // eslint-disable-next-line object-shorthand
//   filename: function (req, file, cb) {
//     cb(null, file.originalname);
//   },
// });

// const uploader = multer({ storage: storage });

app.use(cors());

app.use(bodyParser.urlencoded({ extended: true }));

app.post("/upload", (req, res, next) => {
  console.log(" file successfully uploaded !!");
  setTimeout(() => {
    return res.status(200).json({ result: true, msg: "file uploaded" });
  }, 3000);
});

app.post("/sendqueries", (req, res, next) => {
  console.log(`strings received`);
  console.log(req.body);
  return res.status(200).json({ result: true, msg: "message received" });
});

app.delete("/upload", (req, res) => {
  console.log(`File deleted`);
  return res.status(200).json({ result: true, msg: "file deleted" });
});

app.listen(8080, () => {
  console.log(`Server running on 8080`);
});
