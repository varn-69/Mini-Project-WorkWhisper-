import React from 'react'
import './JobCard.css'

const JobCard = ({ job, rank, onSelect }) => {
  const matchPercentage = (job.final_score * 100).toFixed(0)

  return (
    <div
      className="job-card"
      onClick={onSelect}
    >
      <div className="job-rank">#{rank}</div>
      <div className="job-header">
        <h3 className="job-title">{job.job_title}</h3>
      </div>

      <div className="job-company">{job.company}</div>

      <div className="job-location">{job.location}</div>

      {job.source && (
        <div className="job-source">Source: {job.source}</div>
      )}

      <div className="job-salary">
        ${job.salary_min.toLocaleString()} - ${job.salary_max.toLocaleString()}
      </div>

      <div className="match-section">
        <div className="match-badge">Match</div>
        <div className="match-percentage">{matchPercentage}%</div>
      </div>

      <div className="skills-preview">
        {job.matched_skills.slice(0, 3).map((skill, index) => (
          <span key={index} className="skill-tag matched">
            {skill}
          </span>
        ))}
        {job.missing_skills.length > 0 && (
          <span className="skill-tag missing">
            +{job.missing_skills.length} more
          </span>
        )}
      </div>

      <button className="view-details-button">
        View details
      </button>
    </div>
  )
}

export default JobCard
