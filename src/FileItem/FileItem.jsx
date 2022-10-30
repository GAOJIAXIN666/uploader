import axios from "axios";
import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faFileAlt,
  faSpinner,
  faTrash,
} from "@fortawesome/free-solid-svg-icons";
import "./FileItem.scss";

const FileItem = ({ file, removeFile }) => {
  const deleteFileHandler = (_name) => {
    axios
      .delete(`http://localhost:8080/upload?name=${_name}`)
      .then((res) => removeFile(_name))
      .catch((err) => console.error(err));
  };
  return (
    <li className="file-item" key={file.name}>
      <FontAwesomeIcon icon={faFileAlt} />
      <p>{file.name}</p>
      <div className="actions">
        <div className="loading"></div>
        {file.isUploading && (
          <FontAwesomeIcon
            icon={faSpinner}
            className="fa-spin"
            onClick={() => removeFile(file)}
          />
        )}
        {!file.isUploading && (
          <FontAwesomeIcon icon={faTrash} onClick={() => removeFile(file)} />
        )}
      </div>
    </li>
  );
};

export default FileItem;
