'use client';
import { FormEvent, use, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
// import axios from 'axios';
import api from '../api';

export default function Register() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter()


  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    // Register logic will be added later
    try {
        const response = await api.post(`/register`, {
            username: username,
            email: email,
            password: password
        })
        if (response.status === 201) {
            console.log("successfully created the user", response);
            // redirect the user to the login page
            router.push('/login')
        }
    } catch (error) {
        console.log("error while registering", error)
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-80">
        <h1 className="text-2xl font-bold text-center">Register</h1>
        
        <div className="flex flex-col gap-2">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            className="border p-2 rounded"
          />
        </div>

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
          Register
        </button>
        <Link href="/login" className="bg-blue-500 text-white p-2 rounded">login</Link>
      </form>
    </div>
  )
}
