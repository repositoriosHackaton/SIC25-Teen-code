import React, { useState } from "react";
import RecipeFinder from "./components/ChatBotInterface";
import Questions from "./components/Question/QuestionComponent";


const App = () => {
  const [isChatbotActive, setIsChatbotActive] = useState(localStorage.getItem("hasVisited") === "true");

  return isChatbotActive ? <RecipeFinder /> : <Questions onComplete={() => setIsChatbotActive(true)} />;
};

export default App;
