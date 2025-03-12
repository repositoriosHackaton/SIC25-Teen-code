import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api"; // Ajusta la URL según tu backend


// 🔍 Buscar receta por nombre
export const buscarReceta = async (query) => {
  try {
    const response = await axios.get(`${API_URL}/buscar_receta/`, {
      params: { query },
    });
    // Ahora, la respuesta incluye la preparación
    const receta = response.data;
    return receta;  // Devuelve toda la receta, que incluye preparación
  } catch (error) {
    console.error("Error al buscar la receta:", error);
    throw new Error("Hubo un error al buscar la receta.");
  }
};

// 📝 Enviar feedback
export const enviarFeedback = async (recipeTitle, type, comment) => {
  try {
    await axios.post(`${API_URL}/feedback/`, {
      recipe: recipeTitle,
      type,
      comment,
    });
    return true;
  } catch (error) {
    console.error("Error enviando feedback:", error);
    throw new Error("No se pudo enviar el feedback.");
  }
};

export const recomendaciones = async () => {
  try {
    const response = await axios.get(`${API_URL}/recomendacion/`);

    if (!response.data) {
      throw new Error("La API devolvió datos vacíos");
    }

    return response.data;
  } catch (error) {
    console.error("Error al buscar recomendaciones:", error);
    throw new Error("Hubo un error al buscar recomendaciones");
  }
};

export const preparacion = async (query) => {
  try {
    const response = await axios.get(`${API_URL}/preparacion/`, {
      params: { query },
    });

    if (!response.data) {
      throw new Error("La API devolvió datos vacíos");
    }

    return response.data;
  } catch (error) {
    console.error("Error al buscar recomendaciones:", error);
    throw new Error("Hubo un error al buscar recomendaciones");
  }
};


// 📌 Enviar los datos del usuario al backend
export const guardarUsuario = async (usuario) => {
  console.log("Enviando usuario:", usuario);
  try {
    const response = await axios.post(`${API_URL}/guardar_user/`, usuario);
    return response.data; // Devuelve la respuesta de la API
  } catch (error) {
    console.error("Error al guardar el usuario:", error);
    throw new Error("No se pudo guardar el usuario.");
  }
};