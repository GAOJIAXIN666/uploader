import { useState } from "react";
import "./App.scss";
import FileUpload from "./FileUpload/FileUpload";
import FileItem from "./FileItem/FileItem";

function App() {
  const [file, setFile] = useState(null);

  const removeFile = () => {
    setFile(null);
  };

  return (
    <div className="App">
      <div className="title">Upload file</div>
      <FileUpload file={file} setFile={setFile} removeFile={removeFile} />
      {file && <FileItem file={file} removeFile={removeFile} />}
    </div>
  );
}

export default App;
