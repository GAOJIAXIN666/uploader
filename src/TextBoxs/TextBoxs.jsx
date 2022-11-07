import { useEffect, useState } from "react";
import "./TextBoxs.scss";
import axios from "axios";

const TextBoxs = ({ onChange, queryStr }) => {
  const [table, setTableName] = useState("");
  const [column, setColumnName] = useState("");
  const [foreignKey, setForeignKey] = useState("");
  const [query, setqueryName] = useState("");

  const sendStringsHandler = () => {
    console.log("四个输入款的查询条件", queryStr);
    axios
      .post("http://localhost:8080/sendqueries", queryStr)
      .then((res) => {})
      .catch((err) => {
        console.error(err);
      });
  };

  useEffect(() => {
    onChange && onChange({ table, column, foreignKey, query });
  }, [table, column, foreignKey, query]);

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
        <label>Foreign Key:</label>
        <textarea
          required
          onChange={(e) => setForeignKey(e.target.value)}
        ></textarea>
        <label>SQL query you want to perform:</label>
        <textarea
          required
          onChange={(e) => setqueryName(e.target.value)}
        ></textarea>
        <button onClick={sendStringsHandler}>submit </button>
      </form>
    </li>
  );
};

export default TextBoxs;
