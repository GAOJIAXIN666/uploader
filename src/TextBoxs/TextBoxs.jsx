import { useEffect, useState } from "react";
import "./TextBoxs.scss";

const TextBoxs = ({ onChange }) => {
  const [table, setTableName] = useState("");
  const [column, setColumnName] = useState("");
  const [query, setqueryName] = useState("");

  useEffect(() => {
    onChange && onChange({ table, column, query });
  }, [table, column, query]);

  return (
    <li className="textBoxs">
      <form>
        <label>Table Name:</label>
        <textarea
          required
          onChange={(e) => setTableName(e.target.value)}
        ></textarea>
        <label>Column Name:</label>
        <textarea
          required
          onChange={(e) => setColumnName(e.target.value)}
        ></textarea>
        <label>SQL query you want to perform:</label>
        <textarea
          required
          onChange={(e) => setqueryName(e.target.value)}
        ></textarea>
        <button>submit</button>
      </form>
    </li>
  );
};

export default TextBoxs;
