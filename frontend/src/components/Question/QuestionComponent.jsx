import React, { useState, useEffect } from "react";
import styled from "styled-components";
import RecipeFinder from "../ChatBotInterface";

// Hook personalizado para detectar la primera visita
function useFirstVisit() {
  const [isFirstVisit, setIsFirstVisit] = useState(false);

  useEffect(() => {
    try {
      const hasVisited = localStorage.getItem("hasVisited");
      if (!hasVisited) {
        setIsFirstVisit(true);
        localStorage.setItem("hasVisited", "true");
      }
    } catch (error) {
      console.error("Error accessing localStorage:", error);
    }
  }, []);

  return isFirstVisit;
}

// Estilos básicos
const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #121212;
  color: white;
  font-family: Arial, sans-serif;
  text-align: center;
`;

const Title = styled.h1`
  font-size: 24px;
  color: #2ecc71;
  margin-bottom: 20px;
`;

const Question = styled.p`
  font-size: 18px;
  margin-bottom: 20px;
`;

const Input = styled.input`
  padding: 10px;
  width: 80%;
  max-width: 400px;
  border-radius: 8px;
  border: 1px solid #444;
  background-color: #1e1e1e;
  color: white;
  font-size: 16px;
  text-align: center;
`;

const Button = styled.button`
  background: linear-gradient(135deg, #2ecc71, #52b0c4);
  color: white;
  border: none;
  padding: 12px 20px;
  font-size: 18px;
  margin-top: 20px;
  border-radius: 10px;
  cursor: pointer;
  transition: 0.3s;

  &:hover {
    transform: scale(1.05);
    background: linear-gradient(135deg, #27ae60, #52b0c4);
  }
`;

// Pantallas de preguntas
const screens = [
  {
    key: "bienvenida",
    question: "🌟 Bienvenido a BotRamsey 🍽️",
    placeholder: "",
    isFirst: true,
  },
  {
    key: "nombre",
    question: "¿Cuál es tu nombre?",
    placeholder: "Escribe tu nombre",
  },
  {
    key: "apellido",
    question: "¿Cuál es tu apellido?",
    placeholder: "Escribe tu apellido",
  },
  {
    key: "edad",
    question: "¿Cuántos años tienes?",
    placeholder: "Escribe tu edad",
  },
  {
    key: "preferencias",
    question: "¿Tienes alguna preferencia alimentaria?",
    options: ["Sin gluten", "Sin lactosa", "Sin azúcar", "Sin sal"],
    isMultipleChoice: true,
  },
  {
    key: "alimentacion",
    question: "¿Sigues alguna dieta específica?",
    options: ["Vegetariano", "Vegano", "Macrobiótico", "Perder peso"],
    isMultipleChoice: true,
  },
];

const PreguntasBienvenida = () => {
  const isFirstVisit = useFirstVisit();
  const [screen, setScreen] = useState(0);
  const [answers, setAnswers] = useState({});
  const [completed, setCompleted] = useState(false);

  useEffect(() => {
    sessionStorage.setItem("usuario", JSON.stringify(answers));
  }, [answers]);

  const nextScreen = () => {
    if (screen < screens.length - 1) {
      setScreen(screen + 1);
    } else {
      setCompleted(true);;
    }
  };

  const handleInputChange = (e) => {
    setAnswers({ ...answers, [screens[screen].key]: e.target.value });
  };

  const handleOptionChange = (option) => {
    const currentAnswers = answers[screens[screen].key] || [];
    if (currentAnswers.includes(option)) {
      setAnswers({
        ...answers,
        [screens[screen].key]: currentAnswers.filter((item) => item !== option),
      });
    } else {
      setAnswers({
        ...answers,
        [screens[screen].key]: [...currentAnswers, option],
      });
    }
  };

  if (!isFirstVisit) return null;
  if (completed) return <RecipeFinder />; // Muestra RecipeFinder al terminar

  return (
    isFirstVisit &&
    <Container>
      <Title>BotRamsey</Title>
      <Question>{screens[screen].question}</Question>

      {screens[screen].isMultipleChoice ? (
        <div>
          {screens[screen].options.map((option, index) => (
            <div key={index}>
              <label>
                <input
                  type="checkbox"
                  checked={(answers[screens[screen].key] || []).includes(option)}
                  onChange={() => handleOptionChange(option)}
                />
                {option}
              </label>
            </div>
          ))}
          <Button onClick={nextScreen}>Siguiente</Button>
        </div>
      ) : (
        <div>
          <Input
            value={answers[screens[screen].key] || ""}
            placeholder={screens[screen].placeholder}
            onChange={handleInputChange}
          />
          <Button onClick={nextScreen}>Siguiente</Button>
        </div>

      )}
      
    </Container>
    
  );
};

export default PreguntasBienvenida;