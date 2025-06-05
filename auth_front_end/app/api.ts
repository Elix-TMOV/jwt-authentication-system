import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_URL,
});

// now I will create some configs so that the api always uses the stored jwt token when making a request
api.interceptors.request.use((config) => {
        const running_on_browser: boolean = typeof window !== "undefined";
        if (running_on_browser) {
            const jwt_token = localStorage.getItem("jwt");
            if (jwt_token) { // if the token is present use that for the auth header
                config.headers.Authorization = `Bearer ${jwt_token}`;
                console.log("attached the jwt token to the request", jwt_token)
            }
        }
        return config;
    }, 
    (error) => {
        return Promise.reject(error);
    }
)



export default api;