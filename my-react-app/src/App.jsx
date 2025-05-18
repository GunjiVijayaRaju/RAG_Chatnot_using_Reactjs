import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Chatbot from "./Chatbot";
// import UploadedFiles from "./UploadedFiles";


const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Chatbot />} />
        {/* <Route path="/chatbot-introduction" element={<ChatbotIntroduction />} /> */}
      </Routes>
    </Router>
  );
};

// const App = () => (
//   <Router>
//     <Routes>
//       <Route path="/" element={<Chatbot />} />
//       <Route path="/chatbot-introduction" element={<ChatbotIntroduction />} />
//     </Routes>
//   </Router>
// );

// export default App;


export default App;