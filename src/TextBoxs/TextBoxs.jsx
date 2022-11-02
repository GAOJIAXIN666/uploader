import { useState } from "react";
import "./TextBoxs.scss";

const TextBoxs = (setTableName, setColumnName, setQueryName) => {
  return (
    <li className="textBoxs">
      <form>
        <label>Table Name:</label>
        <input
          type="text"
          required
          value={title}
          onChange={(e) => setTableName(e.target.value)}
        />
        <label>Column Name:</label>
        <textarea
          required
          value={body}
          onChange={(e) => setColumnName(e.target.value)}
        ></textarea>
        <label>SQL query you want to perform:</label>
        <textarea
          required
          value={body}
          onChange={(e) => setQueryName(e.target.value)}
        ></textarea>
        <button>submit</button>
      </form>
    </li>
  );
};

export default TextBoxs;
