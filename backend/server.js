const express = require("express");
const multer = require("multer");
const path = require("path");
const app = express();
const cors = require("cors");

const storage = multer.diskStorage({
  // eslint-disable-next-line object-shorthand
  destination: function (req, file, cb) {
    cb(null, path.join(__dirname, "./sqls/"));
  },
  // eslint-disable-next-line object-shorthand
  filename: function (req, file, cb) {
    cb(null, file.originalname);
  },
});

const uploader = multer({ storage: storage });

app.use(cors());

app.post("/upload", uploader.single("newFile"), (req, res, next) => {
  // use modules such as express-fileupload, Multer, Busboy
  console.log(req.file.originalname + " file successfully uploaded !!");
  setTimeout(() => {
    return res.status(200).json({ result: true, msg: "file uploaded" });
  }, 3000);
});

app.delete("/upload", (req, res) => {
  console.log(`File deleted`);
  return res.status(200).json({ result: true, msg: "file deleted" });
});

app.listen(8080, () => {
  console.log(`Server running on 8080`);
});
