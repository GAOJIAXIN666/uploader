import { useState } from "react";
import "./App.scss";
import FileUpload from "./FileUpload/FileUpload";
import FileItem from "./FileItem/FileItem";
import TextBoxs from "./TextBoxs/TextBoxs";

function App() {
  const [file, setFile] = useState(null);
  const [load, setLoad] = useState(true);
  const removeFile = () => {
    setFile(null);
  };
  const [table, setTableName] = useState("");
  const [column, setColumnName] = useState("");
  const [query, setqueryName] = useState("");

  return (
    <div className="App">
      <div className="title">Upload file</div>
      <TextBoxs
        setTableName={setTableName}
        setColumnName={setColumnName}
        setqueryName={setqueryName}
      />
      <FileUpload
        file={file}
        setFile={setFile}
        removeFile={removeFile}
        setLoad={setLoad}
      />
      {file && <FileItem file={file} load={load} removeFile={removeFile} />}
    </div>
  );
}

export default App;
