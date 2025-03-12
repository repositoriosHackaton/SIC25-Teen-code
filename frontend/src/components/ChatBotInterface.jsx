import React, { useState, useRef, useEffect } from "react";
import styled, { createGlobalStyle } from "styled-components";
import { FaUtensils } from "react-icons/fa"; // Kitchen icon
import { buscarReceta, recomendaciones, preparacion } from "../api/apiController";
import AudioRecorder from "./Recorder/RecorderButton";

// Function to format the presentation of the data
function formato_presentacion(data) {
  if (!data || typeof data !== "object") {
    return "<p style='color: red; font-weight: bold;'>⚠️ Error al cargar la receta.</p>";
  }
  return `
    <style>
      h1, h2, p, strong {
        margin: 0;
      }
    </style>
    <h1 style="text-align: center; font-size: 24px; color: #FFD700;">${data.titulo || "Receta no encontrada"}</h1>
    <h2 style="color: #FFD700;">🌟 Propiedades</h2>
    <p>${data.propiedades}</p>
    <h2 style="color: #4CAF50;">🥄 Ingredientes</h2>
    <p>${data.ingredientes}</p>
    <h2 style="color: #FFAA33;">⭐ Valoración</h2>
    <p><strong>${data.valoracion}</strong></p>
    <h2 style="color: #FF69B4;">🍽️ Tipo</h2>
    <p>${data.tipo}</p>
  `;
}



const extraerMinutos = (texto) => {
  const match = texto.match(/(\d+)\s*minuto/); // Busca números antes de "minuto"
  return match ? parseInt(match[1], 10) : null;
};


const Temporizador = ({ minutos, onFinish }) => {
  const [tiempo, setTiempo] = useState(minutos * 60); // Convertir minutos a segundos


  useEffect(() => {
    if (tiempo <= 0) {
      onFinish(); // Llamar función cuando el tiempo termine
      return;
    }

    const interval = setInterval(() => {
      setTiempo((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(interval);
  }, [tiempo]);

  const minutosRestantes = Math.floor(tiempo / 60);
  const segundosRestantes = tiempo % 60;

  return (
    <div>
      <h3>Tiempo restante: {minutosRestantes}m : {segundosRestantes}s</h3>
      {tiempo <= 0 && <p>¡Tiempo finalizado!</p>}
    </div>
  );
};


// 🌑 Global styles
const GlobalStyle = createGlobalStyle`
  body {
    background-color: #121212;
    color: white;
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    overflow: hidden;
  }
`;

// 📌 Main container
const ChatContainer = styled.div`
  display: flex;
  width: 100%;
  height: 100vh;
  background-color: #1e1e1e;
  margin: 0;
  padding: 0;
  overflow: auto;
`;

// 📌 Sidebar
const Sidebar = styled.div`
  width: 20%;
  background-color: #2c2c2c;
  padding: 3%;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-right: 1px solid #444;
  overflow-y: auto;
  overflow-x: hidden;

  &::-webkit-scrollbar {
    width: 8px;
  }

  &::-webkit-scrollbar-track {
    background: #2c2c2c;
    border-radius: 4px;
  }

  &::-webkit-scrollbar-thumb {
    background: #4CAF50;
    border-radius: 4px;
  }

  &::-webkit-scrollbar-thumb:hover {
    background: #52b0c4;
  }

  scrollbar-width: thin;
  scrollbar-color: #4CAF50 #2c2c2c;
`;

const SidebarTitle = styled.h2`
  display: flex;
  align-items: center;
  gap: 10px;
  color: #4CAF50;
  font-size: 24px;
`;

const SidebarIcon = styled(FaUtensils)`
  font-size: 28px;
  color: #4CAF50;
`;

// 📌 User recommendation
const UserRecomendation = styled.div`
  width: 100%;
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #2A2A2A;
  border-radius: 12px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
  cursor: pointer;
  margin-bottom: 10px;
  color: #FFFFFF;
  text-align: center;

  &:hover {
    transform: scale(1.05);
    box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.25);
  }
`;

// 📌 Chat area
const ChatArea = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  padding: 5% 5% 0 5%;
  max-height: 100vh;
  width: 100%;

  &::-webkit-scrollbar {
    width: 8px;
  }

  &::-webkit-scrollbar-track {
    background: #2c2c2c;
    border-radius: 4px;
  }

  &::-webkit-scrollbar-thumb {
    background: #4CAF50;
    border-radius: 4px;
  }

  &::-webkit-scrollbar-thumb:hover {
    background: #52b0c4;
  }

  scrollbar-width: thin;
  scrollbar-color: #4CAF50 #2c2c2c;
`;

// 📌 Messages container
const MessagesContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex-grow: 1;
  margin: 0;
  padding: 0;
`;

// Animation for messages
const slideInAnimation = `
  @keyframes slide-in {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
`;

// 📌 Base style for messages
const MessageBase = styled.div`
  ${slideInAnimation}
  padding: 1%;
  border-radius: 10px;
  animation: slide-in 0.3s ease-out;
  word-wrap: break-word;
  white-space: pre-wrap;
  width: fit-content;
  max-width: 70%;
  min-width: 10%;
  display: block;
`;

// 📌 User message
const UserMessage = styled(MessageBase)`
  background-color: #4CAF50;
  color: white;
  align-self: flex-end;
  border-bottom-right-radius: 0;
`;

// 📌 Bot message
const BotMessage = styled(MessageBase)`
  background-color: #444;
  color: white;
  align-self: flex-start;
  border-bottom-left-radius: 0;
`;

// 📌 Preparacion message
const PreparacionMark = styled.div`
  display: ${(props) => (props.visible ? "block" : "none")};
  ${slideInAnimation}
  padding: 1%;
  border-radius: 10px;
  animation: slide-in 0.3s ease-out;
  word-wrap: break-word;
  white-space: pre-wrap;
  width: fit-content;
  max-width: 70%;
  min-width: 10%;
  background-color: #444;
  color: white;
  align-self: flex-start;
  border-bottom-left-radius: 0;
`;

// 📌 Chat input
const ChatInput = styled.input`
  padding: 10px;
  margin: 2%;
  width: 100%;
  border-radius: 8px;
  border: 1px solid #444;
  background-color: #1e1e1e;
  color: white;
  font-size: 16px;
  box-sizing: border-box;
  transition: border-color 0.3s ease, transform 0.3s ease;

  &:focus {
    border-color: #4CAF50;
    transform: scale(1.02);
    outline: none;
  }
`;

// 📌 Button
const Button = styled.button`
  background: linear-gradient(135deg, #4CAF50, #52b0c4);
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 10px;
  cursor: pointer;
  transition: 0.3s;

  &:hover {
    transform: scale(1.05);
    background: linear-gradient(135deg, #4CAF50, #52b0c4);
  }
`;

// 📌 Input container
const InputContainer = styled.div`
  width: 100%;
  display: flex;
  align-items: center;
  margin: 0;
  position: sticky;
  bottom: 0;
  background-color: #1e1e1e;
`;

const RecipeFinder = () => {
  const [preparacion_data, setPreparacion] = useState([]);
  useEffect(() => {
    sessionStorage.clear(); // Limpia la sesión al cargar la página
  }, []);  

  const [paso, setPaso] = useState(0); // Asegura que siempre inicie en 0
  const [recomendation, setRecomendation] = useState({ link: [] });
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(false);
  const [mostrarCronometro, setMostrarCronometro] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const fetchRecomendations = async () => {
      const recomendationData = await recomendaciones();
      setRecomendation(recomendationData);
    };
    fetchRecomendations();
  }, []);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  useEffect(() => {
    sessionStorage.setItem("paso", paso);
  }, [paso]);

  const avanzar = () => {
    setPaso((prev) => prev + 1);
  };

  const regresar = () => {
    setPaso((prev) => (prev > 0 ? prev - 1 : 0));
  };

  const salir = () => {
    setPaso(0);
    sessionStorage.removeItem("paso"); // 🗑 Borra de la sesión
    setPreparacion([])
  };

  const handleSendMessage = async () => {
    if (inputValue.trim() === "") return;

    setMessages((prev) => [...prev, { role: "user", content: inputValue }]);
    setLoading(true); // Start loading

    try {
      const recipeData = await buscarReceta(inputValue); // Await the API call
      const formattedResponse = formato_presentacion(recipeData);
      setMessages((prev) => [...prev, { role: "bot", content: formattedResponse }]);
      setData(recipeData); // Store the recipe data for later use
    } catch (error) {
      setMessages((prev) => [...prev, { role: "bot", content: "<p>Error al buscar la receta.</p>" }]);
    } finally {
      setLoading(false); // End loading
    }

    setInputValue("");
  };
  
  const cargar_pasos = async () => {
    const datos = await preparacion(data.link);
    setPreparacion(datos);
  };

  return (
    <>
      <GlobalStyle />
      <ChatContainer>
        {/* Sidebar */}
        <Sidebar>
          <SidebarTitle>
            <SidebarIcon /> <span>BotRamsey</span>
          </SidebarTitle>
          <SidebarTitle style={{ color: "#FFFFFF", fontSize: "24px", margin: "5%" }}>Para Ti</SidebarTitle>
          {recomendation.link.length > 0 ? (
            recomendation.link.map((i, index) => (
              <UserRecomendation key={index}>
                <a href={i} style={{ textDecoration: "none", color: "inherit" }}>
                  <img
                    style={{
                      width: "100px",
                      height: "100px",
                      objectFit: "cover",
                      borderRadius: "10px",
                      boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
                      transition: "box-shadow 0.3s ease-in-out"
                    }}
                    src={recomendation.imagen[index]}
                    alt={`Recomendación ${index}`}
                  />
                  <h3 style={{ fontSize: "1.2em", fontWeight: "bold", margin: "10px 0", color: "#4CAF50" }}>
                    {recomendation.nombre[index]}
                  </h3>
                </a>
                <p style={{ margin: "5px 0", fontSize: "0.9em", color: "#CCCCCC" }}>
                  🍽️ Comensales: {recomendation.comensales[index]}
                </p>
                <p style={{ margin: "5px 0", fontSize: "0.9em", color: "#CCCCCC" }}>
                  ⚖️ {recomendation.dificultad[index]}
                </p>
                <p style={{ margin: "5px 0", fontSize: "0.9em", color: "#CCCCCC" }}>
                  ⏳ Duración: {recomendation.duracion[index]}
                </p>
              </UserRecomendation>
            ))
          ) : (
            <p style={{ textAlign: "center", color: "#888", fontStyle: "italic" }}>Cargando recomendaciones...</p>
          )}
        </Sidebar>

        {/* Chat area */}
        <ChatArea>
          <MessagesContainer>
            {messages.map((message, index) => (
              <React.Fragment key={index}>
                {message.role === "user" ? (
                  <UserMessage>{message.content}</UserMessage>
                ) : (
                  <BotMessage>
                    <span dangerouslySetInnerHTML={{ __html: message.content }} />
                    <button 
                      onClick={cargar_pasos} 
                      style={{
                        backgroundColor: "#28a745",
                        color: "#ffffff",
                        border: "none",
                        padding: "12px 20px",
                        borderRadius: "8px",
                        fontSize: "16px",
                        fontWeight: "bold",
                        cursor: "pointer",
                        display: "block",
                        width: "100%",
                        textAlign: "center",
                        transition: "background 0.3s ease",
                        boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.2)"
                      }}
                      onMouseOver={(e) => e.target.style.backgroundColor = "#218838"}
                      onMouseOut={(e) => e.target.style.backgroundColor = "#28a745"}
                    >
                      Ver preparación
                    </button>
                  </BotMessage>
                )}
              </React.Fragment>
            ))}
            {loading && <BotMessage><p>Cargando...</p></BotMessage>}

            <PreparacionMark visible={!!preparacion_data.length}>
              {preparacion_data[paso]}
              {preparacion_data?.[paso]?.includes('minuto') && (
                <div>
                <button
                  onClick={() => setMostrarCronometro(true)}
                  disabled={!preparacion_data?.[paso] || !preparacion_data[paso].includes('minuto')}
                  style={{
                    background: "linear-gradient(135deg, #007bff, #0056b3)", // Azul degradado
                    color: "#ffffff",
                    border: "none",
                    padding: "12px 24px",
                    borderRadius: "8px",
                    fontSize: "16px",
                    fontWeight: "bold",
                    cursor: "pointer",
                    transition: "all 0.3s ease",
                    boxShadow: "0px 4px 8px rgba(0, 0, 0, 0.2)",
                    margin: "10px 0",
                    width: "100%", // Ocupa todo el ancho disponible
                    maxWidth: "250px", // No crece demasiado
                    textAlign: "center",
                  }}
                  onMouseOver={(e) => e.target.style.background = "#0056b3"}
                  onMouseOut={(e) => e.target.style.background = "linear-gradient(135deg, #007bff, #0056b3)"}
                >
                  ⏳ Iniciar Cronómetro
                </button> 

                {mostrarCronometro && <Temporizador minutos={extraerMinutos(preparacion_data[paso])} onFinish={() => setMostrarCronometro(false)} />}
                
                
                </div>
              )}
              <div style={{
                display: "flex",
                justifyContent: "space-between",  // Espacia los botones uniformemente
                gap: "10px",                      // Espaciado entre botones
                width: "100%",                     // Ajusta el ancho según necesites
              }}>
              <button onClick={regresar} style={{
                        backgroundColor: "#28a745",
                        color: "#ffffff",
                        border: "none",
                        padding: "12px 20px",
                        borderRadius: "8px",
                        fontSize: "16px",
                        fontWeight: "bold",
                        cursor: "pointer",
                        flex: "1", // Para que todos los botones tengan el mismo ancho
                        textAlign: "center",
                        transition: "background 0.3s ease",
                        boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.2)"
                      }}>Regresar</button>
              <button onClick={avanzar} style={{
                        backgroundColor: "#28a745",
                        color: "#ffffff",
                        border: "none",
                        padding: "12px 20px",
                        borderRadius: "8px",
                        fontSize: "16px",
                        fontWeight: "bold",
                        cursor: "pointer",
                        flex: "1", // Para que todos los botones tengan el mismo ancho
                        textAlign: "center",
                        transition: "background 0.3s ease",
                        boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.2)"
                      }}>Avanzar</button>
              <button onClick={salir} style={{
                        backgroundColor: "#28a745",
                        color: "#ffffff",
                        border: "none",
                        padding: "12px 20px",
                        borderRadius: "8px",
                        fontSize: "16px",
                        fontWeight: "bold",
                        cursor: "pointer",
                        flex: "1", // Para que todos los botones tengan el mismo ancho
                        textAlign: "center",
                        transition: "background 0.3s ease",
                        boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.2)"
                      }}>Salir</button></div>
            </PreparacionMark>

            <div ref={messagesEndRef} />
          </MessagesContainer>
          <InputContainer>
            <ChatInput
              value={inputValue}
              placeholder="Escribe el nombre de la receta..."
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") handleSendMessage();
              }}
            />
            <Button onClick={handleSendMessage}>Enviar</Button>
            <AudioRecorder onButtonClick={setInputValue}/>
          </InputContainer>
        </ChatArea>
      </ChatContainer>
    </>
  );
};

export default RecipeFinder;