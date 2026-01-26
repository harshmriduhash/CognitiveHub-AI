import React, { createContext, useContext, useState, useEffect } from 'react'
import axios from 'axios'

interface AuthContextType {
  isAuthenticated: boolean
  token: string | null
  user: any | null
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, fullName: string, tenantName: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'))
  const [user, setUser] = useState<any | null>(null)

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      fetchUser()
    }
  }, [token])

  const fetchUser = async () => {
    try {
      const response = await axios.get('/auth/me')
      setUser(response.data)
    } catch (error) {
      logout()
    }
  }

  const login = async (email: string, password: string) => {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)
    
    const response = await axios.post('/auth/token', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    
    const accessToken = response.data.access_token
    setToken(accessToken)
    localStorage.setItem('token', accessToken)
    axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`
    await fetchUser()
  }

  const register = async (email: string, password: string, fullName: string, tenantName: string) => {
    await axios.post('/auth/register', {
      email,
      password,
      full_name: fullName,
      tenant_name: tenantName
    })
    await login(email, password)
  }

  const logout = () => {
    setToken(null)
    setUser(null)
    localStorage.removeItem('token')
    delete axios.defaults.headers.common['Authorization']
  }

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated: !!token,
        token,
        user,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

