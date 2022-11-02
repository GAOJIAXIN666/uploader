import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import "./FileUpload.scss";
import axios from "axios";

const FileUpload = ({ queryStr, file, setFile, removeFile, setLoad }) => {
  const uploadHandler = (event) => {
    file = event.target.files[0];
    if (!file) return;
    setFile(file);
    // upload file
    const formData = new FormData();
    formData.append("newFile", file, file.name);

    console.log("三个输入款的查询条件", queryStr);

    axios
      .post("http://localhost:8080/upload", formData)
      .then((res) => {
        setLoad(false);
      })
      .catch((err) => {
        // inform the user
        console.error(err);
        //removeFile();
      });
  };

  return (
    <>
      <div className="file-card">
        <div className="file-inputs">
          <input type="file" onChange={uploadHandler} />
          <button>
            <i>
              <FontAwesomeIcon icon={faPlus} />
            </i>
            Upload
          </button>
        </div>
        <p className="main">Supported type</p>
        <p className="info">SQL</p>
      </div>
    </>
  );
};

export default FileUpload;
