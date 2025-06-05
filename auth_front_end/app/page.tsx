'use client'

import Link from "next/link";
import { useAuth } from "./context/AuthContext";
import { useState } from "react";
import api from "./api";
import { useRouter } from "next/navigation";
import { AxiosError } from "axios";

export default function Home() {
  const { currentUser, logout } = useAuth()
  const [secret, setSecret] = useState('') // the secret will be what he jwt token encodes
  const router = useRouter()

  const handleSecret = async () => {
    try {
      const response = await api.get("/protected_route")
      setSecret(response.data.message)
    }
    catch(error) {
      const axiosError = error as AxiosError;
      if (axiosError.response?.status === 401) {
          router.push("/login");
      }
}
  }


  return (
    <div className="flex flex-col items-center gap-4 p-4">
      {currentUser ? (
        <p>Welcome {currentUser}</p>
      ) : (
        <p>Please Login to access the secret</p>
      )}
      <button
        className="p-4 bg-purple-500 rounded-md text-white text-2xl"
        onClick={() => handleSecret()}
      >
        See the Secret
      </button>
      {!currentUser ? (
        <div className="flex gap-4">
          <Link href="/login" className="p-2 bg-yellow-200 rounded-md">Login</Link>
          <Link href="/register" className="p-2 bg-blue-200 rounded-md">Register</Link>
        </div>
      ) : (
        <button className="p-2 bg-yellow-200 rounded-md hover:bg-amber-100" onClick={() => logout()}>Logout</button>
      )}
      {secret && <p>{secret}</p>}
    </div>
  );
}
