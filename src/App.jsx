import { useState } from "react";
import "./App.scss";
import FileUpload from "./FileUpload/FileUpload";
import FileItem from "./FileItem/FileItem";

function App() {
  const [file, setFile] = useState([]);

  const removeFile = () => {
    setFile();
  };

  return (
    <div className="App">
      <div className="title">Upload file</div>
      <FileUpload file={file} setFile={setFile} removeFile={removeFile} />
      <FileItem file={file} removeFile={removeFile} />
    </div>
  );
}

export default App;
