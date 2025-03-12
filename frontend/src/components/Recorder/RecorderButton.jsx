import React, { useState, useRef } from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import { FaMicrophone } from 'react-icons/fa'; // Importar el ícono de micrófono de FontAwesome

const AudioRecorder = ({ onButtonClick }) => {
  const [isRecording, setIsRecording] = useState(false);
  const { transcript, resetTranscript } = useSpeechRecognition();
  const mediaRecorderRef = useRef(null);

  const handleRecordButtonClick = async () => {
    if (isRecording) {
      mediaRecorderRef.current.stop();
      SpeechRecognition.stopListening();
      setIsRecording(false);
      console.log('Transcripción:', transcript);
      onButtonClick(transcript);
    } else {
      resetTranscript();
      navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
          mediaRecorderRef.current = new MediaRecorder(stream);

          mediaRecorderRef.current.onstart = () => {
            SpeechRecognition.startListening({ continuous: true });
          };

          mediaRecorderRef.current.onstop = () => {
            SpeechRecognition.stopListening();
          };

          mediaRecorderRef.current.start();
          setIsRecording(true);
        })
        .catch(error => {
          console.error('Error al acceder al micrófono:', error);
        });
    }
  };

  return (
    <div>
      <button
        onClick={handleRecordButtonClick}
        style={{
          marginLeft: '20px',
          background: 'linear-gradient(135deg, #4CAF50, #52b0c4)',
          color: 'white',
          border: 'none',
          padding: '12px 20px',
          borderRadius: '10px',
          cursor: 'pointer',
          transition: '0.3s',
          display: 'flex',
          alignItems: 'center',
          gap: '8px', // Espacio entre el ícono y el texto
        }}
        onMouseOver={(e) => {
          e.target.style.transform = 'scale(1.05)';
        }}
        onMouseOut={(e) => {
          e.target.style.transform = 'scale(1)';
        }}
      >
        <FaMicrophone /> {/* Ícono de micrófono */}
        {isRecording ? 'Detener' : 'Grabar'}
      </button>
    </div>
  );
};

export default AudioRecorder;