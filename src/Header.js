import React from "react";
import Navigation from "./Navigation";
import { Link } from "react-router-dom";

function Header() {
  return (
    <header className="border-b p-3 flex justify-between items-center">
      <Link to="/" className="font-bold">
        MIT 6.5830 Database System Final Project
      </Link>

      <Navigation />
    </header>
  );
}

export default Header;
