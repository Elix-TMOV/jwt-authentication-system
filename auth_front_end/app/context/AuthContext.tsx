'use client'
import {
  createContext,
  ReactNode,
  useEffect,
  useState,
  useContext,
} from "react";

// Define the interface of the Auth context
type AuthContextType = {
  currentUser: string | null;
  login: (username: string, jwt: string) => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthContextProvider = ({ children }: { children: ReactNode }) => {
  const [currentUser, setCurrentUser] = useState<string | null>(null);

  const login = (username: string, jwt: string) => {
    setCurrentUser(username);
    localStorage.setItem("jwt", jwt);
  };

  const logout = () => {
    setCurrentUser(null);
    localStorage.removeItem("jwt");
  };

  useEffect(() => {
    const user = localStorage.getItem("user");
    if (user) {
      setCurrentUser(JSON.parse(user));
    }
  }, []);

  useEffect(() => {
    localStorage.setItem("user", JSON.stringify(currentUser));
  }, [currentUser]);

  return (
    <AuthContext.Provider value={{ currentUser, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Create a hook 
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthContextProvider");
  }
  return context;
};

