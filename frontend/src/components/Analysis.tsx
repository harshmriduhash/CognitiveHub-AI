import { useState } from 'react'
import axios from 'axios'

export default function Analysis() {
  const [systemDescription, setSystemDescription] = useState('')
  const [analysisResult, setAnalysisResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const handleAnalyze = async () => {
    setLoading(true)
    try {
      const response = await axios.post('/analysis/analyze', {
        system_description: {
          name: 'System',
          description: systemDescription,
          tech_stack: [],
        },
        analysis_types: ['architecture'],
      })
      setAnalysisResult(response.data)
    } catch (error) {
      console.error('Error analyzing system:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div className="px-4 py-6 sm:px-0">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">System Analysis</h1>

        <div className="bg-white shadow rounded-lg p-6 mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            System Description
          </label>
          <textarea
            value={systemDescription}
            onChange={(e) => setSystemDescription(e.target.value)}
            className="w-full border border-gray-300 rounded-md px-3 py-2"
            rows={6}
            placeholder="Describe your system architecture, tech stack, and requirements..."
          />
          <button
            onClick={handleAnalyze}
            disabled={loading || !systemDescription}
            className="mt-4 bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 disabled:opacity-50"
          >
            {loading ? 'Analyzing...' : 'Analyze System'}
          </button>
        </div>

        {analysisResult && (
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Analysis Results</h2>
            <div className="space-y-4">
              {analysisResult.results?.strengths && (
                <div>
                  <h3 className="font-medium text-gray-900 mb-2">Strengths</h3>
                  <ul className="list-disc list-inside space-y-1 text-gray-700">
                    {analysisResult.results.strengths.map((s: string, i: number) => (
                      <li key={i}>{s}</li>
                    ))}
                  </ul>
                </div>
              )}
              {analysisResult.results?.weaknesses && (
                <div>
                  <h3 className="font-medium text-gray-900 mb-2">Weaknesses</h3>
                  <ul className="list-disc list-inside space-y-1 text-gray-700">
                    {analysisResult.results.weaknesses.map((w: string, i: number) => (
                      <li key={i}>{w}</li>
                    ))}
                  </ul>
                </div>
              )}
              {analysisResult.results?.recommendations && (
                <div>
                  <h3 className="font-medium text-gray-900 mb-2">Recommendations</h3>
                  <ul className="list-disc list-inside space-y-1 text-gray-700">
                    {analysisResult.results.recommendations.map((r: string, i: number) => (
                      <li key={i}>{r}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

