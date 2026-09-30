import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import ProfileForm from './components/ProfileForm'
import RecommendationResults from './components/RecommendationResults'
import './App.css'

function App() {
  const [recommendations, setRecommendations] = useState(null)
  const [candidateName, setCandidateName] = useState('')

  const handleRecommendations = (data) => {
    setRecommendations(data.recommendations)
    setCandidateName(data.candidate_name)
  }

  const handleBack = () => {
    setRecommendations(null)
    setCandidateName('')
  }

  return (
    <div className="app">
      <div className="ambient-background">
        <div className="ambient-blob ambient-blob-1"></div>
        <div className="ambient-blob ambient-blob-2"></div>
        <div className="ambient-blob ambient-blob-3"></div>
        <div className="ambient-blob ambient-blob-4"></div>
      </div>

      <header className="app-header">
        <h1>Work Whisper</h1>
        <p className="subtitle">
          AI-powered job matching that listens to what you want and delivers what you need.
        </p>
      </header>

      <main className="app-main">
        <AnimatePresence mode="wait">
          {!recommendations ? (
            <motion.div
              key="form"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.3 }}
            >
              <ProfileForm onRecommendations={handleRecommendations} />
            </motion.div>
          ) : (
            <motion.div
              key="results"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.3 }}
            >
              <RecommendationResults
                recommendations={recommendations}
                candidateName={candidateName}
                onBack={handleBack}
              />
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      <footer className="app-footer">
        <p>ABES Engineering College Mini Project | 5th Semester</p>
      </footer>
    </div>
  )
}

export default App
