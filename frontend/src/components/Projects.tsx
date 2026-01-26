import { useState, useEffect } from 'react'
import axios from 'axios'

interface Project {
  id: string
  name: string
  description: string
  tech_stack: string[]
  architecture_type: string
}

export default function Projects() {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    tech_stack: '',
    architecture_type: '',
  })

  useEffect(() => {
    fetchProjects()
  }, [])

  const fetchProjects = async () => {
    try {
      // In production, get tenant_id from auth context
      const response = await axios.get('/projects/projects?tenant_id=test-tenant')
      setProjects(response.data)
    } catch (error) {
      console.error('Error fetching projects:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await axios.post('/projects/projects?tenant_id=test-tenant', {
        ...formData,
        tech_stack: formData.tech_stack.split(',').map(s => s.trim()).filter(Boolean),
      })
      setShowForm(false)
      setFormData({ name: '', description: '', tech_stack: '', architecture_type: '' })
      fetchProjects()
    } catch (error) {
      console.error('Error creating project:', error)
    }
  }

  if (loading) {
    return <div className="p-8">Loading...</div>
  }

  return (
    <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div className="px-4 py-6 sm:px-0">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Projects</h1>
          <button
            onClick={() => setShowForm(!showForm)}
            className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700"
          >
            {showForm ? 'Cancel' : 'New Project'}
          </button>
        </div>

        {showForm && (
          <form onSubmit={handleSubmit} className="bg-white shadow rounded-lg p-6 mb-6">
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Name</label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                  rows={3}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Tech Stack (comma-separated)</label>
                <input
                  type="text"
                  value={formData.tech_stack}
                  onChange={(e) => setFormData({ ...formData, tech_stack: e.target.value })}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                  placeholder="Python, FastAPI, PostgreSQL"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Architecture Type</label>
                <input
                  type="text"
                  value={formData.architecture_type}
                  onChange={(e) => setFormData({ ...formData, architecture_type: e.target.value })}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                  placeholder="microservices, monolith, etc."
                />
              </div>
              <button
                type="submit"
                className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700"
              >
                Create Project
              </button>
            </div>
          </form>
        )}

        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {projects.map((project) => (
            <div key={project.id} className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-2">{project.name}</h3>
              <p className="text-sm text-gray-600 mb-4">{project.description}</p>
              {project.tech_stack && project.tech_stack.length > 0 && (
                <div className="mb-2">
                  <span className="text-xs font-medium text-gray-500">Tech Stack:</span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {project.tech_stack.map((tech, idx) => (
                      <span key={idx} className="px-2 py-1 bg-primary-100 text-primary-800 text-xs rounded">
                        {tech}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              {project.architecture_type && (
                <div>
                  <span className="text-xs font-medium text-gray-500">Architecture: </span>
                  <span className="text-xs text-gray-700">{project.architecture_type}</span>
                </div>
              )}
            </div>
          ))}
        </div>

        {projects.length === 0 && (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <p className="text-gray-500">No projects yet. Create your first project to get started.</p>
          </div>
        )}
      </div>
    </div>
  )
}

