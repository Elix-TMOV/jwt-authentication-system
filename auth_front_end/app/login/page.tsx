'use client';
import { FormEvent, useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '../api';
import { useAuth } from '../context/AuthContext';
import Link from 'next/link';


export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth()
  const router = useRouter()

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    // Login logic will be added later
    try {
        const response = await api.post(`/login`, {
            email: email,
            password: password
        })
        if (response.status === 200) {
            console.log("successfully logged in", response);
        }
        login(response.data.username ,response.data.access_token) // store the user name and jwt in the local storage
        router.push('/')
    } catch (error) {
        console.log("error while registering", error)
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-80">
        <h1 className="text-2xl font-bold text-center">Login</h1>
        
        <div className="flex flex-col gap-2">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="border p-2 rounded"
          />
        </div>

        <div className="flex flex-col gap-2">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="border p-2 rounded"
          />
        </div>

        <button type="submit" className="bg-green-500 text-white p-2 rounded">
          Login
        </button>
        <Link href="/register" className="bg-blue-500 text-white p-2 rounded">Register</Link>
      </form>
      <p></p>
    </div>
  )
}
