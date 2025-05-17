// src/index.tsx - Entry point ของแอพพลิเคชัน React

import React from "react";
import ReactDOM from "react-dom";
import DishcoveryApp from "./DishcoveryApp";
import "./index.css";

ReactDOM.render(
  <React.StrictMode>
    <DishcoveryApp />
  </React.StrictMode>,
  document.getElementById("root")
);