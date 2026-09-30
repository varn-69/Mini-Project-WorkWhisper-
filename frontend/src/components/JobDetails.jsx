import React from 'react'
import './JobDetails.css'

const JobDetails = ({ job, onBack, onExplain, loading }) => {
  const matchPercentage = (job.final_score * 100).toFixed(0)

  return (
    <div className="details-container">
      <div className="details-header">
        <button onClick={onBack} className="back-button">
          ← Back
        </button>
      </div>

      <div className="details-card">
        <h1 className="job-title">{job.job_title}</h1>
        <p className="job-company">{job.company}</p>

        <div className="job-meta">
          <div className="detail-item">
            <span className="detail-label">Location</span>
            <span className="detail-value">{job.location}</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Experience</span>
            <span className="detail-value">{job.experience_required} years</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Salary</span>
            <span className="detail-value">
              ${job.salary_min.toLocaleString()} - ${job.salary_max.toLocaleString()}
              {job.currency && job.currency !== 'USD' && ` ${job.currency}`}
            </span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Education</span>
            <span className="detail-value">{job.education}</span>
          </div>
          {job.source && (
            <div className="detail-item">
              <span className="detail-label">Source</span>
              <span className="detail-value">{job.source}</span>
            </div>
          )}
        </div>

        {job.source_url && (
          <div className="source-link-section">
            <a
              href={job.source_url}
              target="_blank"
              rel="noopener noreferrer"
              className="source-link"
            >
              View original posting →
            </a>
          </div>
        )}

        <div className="score-section">
          <h3 className="section-title">Score Breakdown</h3>
          <div className="score-item">
            <span className="score-label">Skill Match</span>
            <div className="score-bar-container">
              <div className="score-bar score-fill skill" style={{ width: `${(job.skill_score * 100).toFixed(0)}%` }}></div>
            </div>
            <span className="score-value">{(job.skill_score * 100).toFixed(0)}%</span>
          </div>
          <div className="score-item">
            <span className="score-label">Experience</span>
            <div className="score-bar-container">
              <div className="score-bar score-fill experience" style={{ width: `${(job.experience_score * 100).toFixed(0)}%` }}></div>
            </div>
            <span className="score-value">{(job.experience_score * 100).toFixed(0)}%</span>
          </div>
          <div className="score-item">
            <span className="score-label">Location</span>
            <div className="score-bar-container">
              <div className="score-bar score-fill location" style={{ width: `${(job.location_score * 100).toFixed(0)}%` }}></div>
            </div>
            <span className="score-value">{(job.location_score * 100).toFixed(0)}%</span>
          </div>
          <div className="score-item">
            <span className="score-label">Salary</span>
            <div className="score-bar-container">
              <div className="score-bar score-fill salary" style={{ width: `${(job.salary_score * 100).toFixed(0)}%` }}></div>
            </div>
            <span className="score-value">{(job.salary_score * 100).toFixed(0)}%</span>
          </div>
          <div className="score-item">
            <span className="score-label">Education</span>
            <div className="score-bar-container">
              <div className="score-bar score-fill education" style={{ width: `${(job.education_score * 100).toFixed(0)}%` }}></div>
            </div>
            <span className="score-value">{(job.education_score * 100).toFixed(0)}%</span>
          </div>
          <div className="score-item">
            <span className="score-label">Final Match</span>
            <div className="score-bar-container">
              <div className="score-bar score-fill skill" style={{ width: `${matchPercentage}%` }}></div>
            </div>
            <span className="score-value final-score">{matchPercentage}%</span>
          </div>
        </div>

        <div className="skills-section">
          <h3 className="section-title">Skill Analysis</h3>
          <div className="skill-group">
            <h4 className="skill-group-title">Matched Skills</h4>
            <div className="skill-tags">
              {job.matched_skills.length > 0 ? (
                job.matched_skills.map((skill, index) => (
                  <span key={index} className="skill-tag matched">
                    {skill}
                  </span>
                ))
              ) : (
                <span className="skill-tag">No matched skills</span>
              )}
            </div>
          </div>
          <div className="skill-group">
            <h4 className="skill-group-title">Missing Skills</h4>
            <div className="skill-tags">
              {job.missing_skills.length > 0 ? (
                job.missing_skills.map((skill, index) => (
                  <span key={index} className="skill-tag missing">
                    {skill}
                  </span>
                ))
              ) : (
                <span className="skill-tag">No missing skills</span>
              )}
            </div>
          </div>
        </div>

        <div className="explanation-section">
          <h3 className="section-title">Why this role fits</h3>
          {!job.explanation ? (
            <button
              onClick={() => onExplain(job)}
              className="explain-button"
              disabled={loading}
            >
              {loading ? 'Generating explanation...' : 'Generate explanation'}
            </button>
          ) : (
            <div className="explanation-content">
              {job.explanation}
            </div>
          )}
        </div>

        {job.learning_roadmap && (
          <div className="roadmap-section">
            <h3 className="section-title">Learning roadmap</h3>
            <ul className="roadmap-list">
              {job.learning_roadmap.split('\n').map((item, index) => (
                item.trim() && (
                  <li key={index} className="roadmap-item">
                    <span className="roadmap-number">{index + 1}</span>
                    <span className="roadmap-text">{item.trim()}</span>
                  </li>
                )
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}

export default JobDetails
