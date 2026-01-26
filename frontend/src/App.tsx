import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Login from './components/Login'
import Dashboard from './components/Dashboard'
import Projects from './components/Projects'
import Workflows from './components/Workflows'
import Analysis from './components/Analysis'
import Navbar from './components/Navbar'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import axios from 'axios'

// Configure axios
axios.defaults.baseURL = '/api'

function AppRoutes() {
  const { isAuthenticated } = useAuth()

  if (!isAuthenticated) {
    return <Login />
  }

  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/projects" element={<Projects />} />
        <Route path="/workflows" element={<Workflows />} />
        <Route path="/analysis" element={<Analysis />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  )
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <AppRoutes />
        </div>
      </Router>
    </AuthProvider>
  )
}

export default App

