import React, { useState } from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import { FaMicrophone } from 'react-icons/fa';

const AudioRecorder = ({ onButtonClick }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [permissionError, setPermissionError] = useState(false);
  const { transcript, resetTranscript, browserSupportsSpeechRecognition } = useSpeechRecognition();

  if (!browserSupportsSpeechRecognition) {
    return <div>¡Tu navegador no soporta reconocimiento de voz!</div>;
  }

  const getMicrophone = async () => {
    const devices = await navigator.mediaDevices.enumerateDevices();
    const audioDevices = devices.filter(device => device.kind === 'audioinput');
  
    console.log('Dispositivos de audio:', audioDevices);
  
    if (audioDevices.length > 0) {
      const deviceId = audioDevices[audioDevices.length - 1].deviceId; // Tomar el último dispositivo disponible (puede ser DroidCam)
      return navigator.mediaDevices.getUserMedia({ audio: { deviceId } });
    } else {
      throw new Error("No hay dispositivos de audio disponibles.");
    }
  };

  

  const handleRecordButtonClick = async () => {

    navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => console.log("Micrófono detectado:", stream))
    .catch(error => console.error("Error en getUserMedia:", error));

    if (isRecording) {
      SpeechRecognition.stopListening();
      setIsRecording(false);
      console.log(transcript)
      onButtonClick(transcript);
    } else {
      resetTranscript();
      setPermissionError(false);
  
      try {
        const stream = await getMicrophone(); // Obtiene el micrófono correcto
        SpeechRecognition.startListening({ continuous: true });
        setIsRecording(true);
      } catch (error) {
        console.error('Error al acceder al micrófono:', error);
        setPermissionError(true);
      }
    }
  };
  

  return (
    <div>
      <button
        onClick={handleRecordButtonClick}
        style={{
          marginLeft: "20px",
          background: isRecording ? "#d9534f" : "linear-gradient(135deg, #4CAF50, #52b0c4)",
          color: "white",
          border: "none",
          padding: "12px 20px",
          borderRadius: "10px",
          cursor: "pointer",
          transition: "0.3s",
          display: "flex",
          alignItems: "center",
          gap: "8px",
        }}
        onMouseOver={(e) => e.target.style.transform = 'scale(1.05)'}
        onMouseOut={(e) => e.target.style.transform = 'scale(1)'}
      >
        <FaMicrophone />
        {isRecording ? 'Detener' : 'Grabar'}
      </button>
      {permissionError && <p style={{ color: 'red' }}>Error: Acceso al micrófono denegado</p>}
    </div>
  );
};

export default AudioRecorder;