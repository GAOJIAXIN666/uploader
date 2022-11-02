import React, { useState } from "react";
import "./App.scss";
import FileUpload from "./FileUpload/FileUpload";
import FileItem from "./FileItem/FileItem";
import TextBoxs from "./TextBoxs/TextBoxs";

function App() {
  const [file, setFile] = useState(null);
  const [load, setLoad] = useState(true);
  const [queryStr, setQueryStr] = useState({});

  const removeFile = () => {
    setFile(null);
  };

  const handleChange = (data) => {
    setQueryStr(data);
  };

  return (
    <div className="App">
      <div className="title">SQL file</div>
      <TextBoxs onChange={handleChange} />
      <FileUpload
        file={file}
        setFile={setFile}
        removeFile={removeFile}
        setLoad={setLoad}
        queryStr={queryStr}
      />
      {file && <FileItem file={file} load={load} removeFile={removeFile} />}
    </div>
  );
}

export default App;
