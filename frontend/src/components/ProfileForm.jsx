import React, { useState } from 'react'
import axios from 'axios'
import './ProfileForm.css'

const ProfileForm = ({ onRecommendations }) => {
  const [formData, setFormData] = useState({
    name: '',
    skills: '',
    education: '',
    experience: 0,
    location: '',
    expected_salary: 0
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await axios.post('/api/recommend', {
        candidate: formData
      })
      onRecommendations(response.data)
    } catch (err) {
      setError('Failed to get recommendations. Please make sure the backend is running.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="profile-form-container">
      <div className="form-card">
        <h2>Profile</h2>
        <p className="form-description">
          Tell us about yourself so we can find roles that fit you.
        </p>

        <form onSubmit={handleSubmit} className="profile-form">
          <div className="form-group">
            <label htmlFor="name">Name *</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              placeholder="Your full name"
            />
          </div>

          <div className="form-group">
            <label htmlFor="skills">Skills *</label>
            <input
              type="text"
              id="skills"
              name="skills"
              value={formData.skills}
              onChange={handleChange}
              required
              placeholder="Python, SQL, Pandas, Git, FastAPI"
            />
            <small className="form-hint">Separate skills with commas</small>
          </div>

          <div className="form-group">
            <label htmlFor="education">Education *</label>
            <input
              type="text"
              id="education"
              name="education"
              value={formData.education}
              onChange={handleChange}
              required
              placeholder="B.Tech Computer Science"
            />
          </div>

          <div className="form-group">
            <label htmlFor="experience">Experience (years) *</label>
            <input
              type="number"
              id="experience"
              name="experience"
              value={formData.experience}
              onChange={handleChange}
              required
              min="0"
              step="0.5"
              placeholder="0"
            />
          </div>

          <div className="form-group">
            <label htmlFor="expected_salary">Expected Salary ($) *</label>
            <input
              type="number"
              id="expected_salary"
              name="expected_salary"
              value={formData.expected_salary}
              onChange={handleChange}
              required
              min="0"
              step="10000"
              placeholder="100000"
            />
          </div>

          <div className="form-group">
            <label htmlFor="location">Preferred Location *</label>
            <input
              type="text"
              id="location"
              name="location"
              value={formData.location}
              onChange={handleChange}
              required
              placeholder="Remote, Noida, Bangalore, Mumbai"
            />
          </div>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <button
            type="submit"
            className="submit-button"
            disabled={loading}
          >
            {loading ? 'Finding Jobs...' : 'Find matching jobs'}
          </button>
        </form>
      </div>

      <div className="product-introduction">
        <div className="intro-section">
          <h3 className="intro-heading">What is Work Whisper?</h3>
          <p className="intro-text">
            Work Whisper helps you discover job opportunities that align with your skills, experience, education, location, and expectations. Instead of showing a generic list of openings, it evaluates your profile against available roles and presents the positions that best fit what you are looking for.
          </p>
        </div>

        <div className="intro-section">
          <h3 className="intro-heading">Why it helps</h3>
          <p className="intro-text">
            The system looks beyond simple keyword matching. It combines skill overlap with text similarity and practical factors such as experience, location, salary, and education to create an explainable match score. You can also see which skills already fit the role and which ones you may need to develop.
          </p>
        </div>

        <div className="intro-section">
          <h3 className="intro-heading">How it works</h3>
          <p className="intro-text">
            Work Whisper processes your profile through its recommendation engine, ranks relevant jobs, and highlights the strongest matches. An AI layer then explains why a role fits your profile and turns the identified skill gaps into a focused learning roadmap.
          </p>
        </div>
      </div>
    </div>
  )
}

export default ProfileForm
