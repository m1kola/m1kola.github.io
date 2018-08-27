import React from 'react'

import profilePic from './profile-pic.jpg'
import { rhythm } from '../utils/typography'

class Bio extends React.Component {
  render() {
    return (
      <div
        style={{
          display: 'flex',
          marginBottom: rhythm(2.5),
        }}
      >
        <img
          src={profilePic}
          alt={`Mikalai Radchuk`}
          style={{
            marginRight: rhythm(1 / 2),
            marginBottom: 0,
            width: rhythm(2),
            height: rhythm(2),
            borderRadius: "50%",
          }}
        />
        <p>
          Mikalai is a Python and Wagtail developer by day. At night he turns into a Gopher and
          attempts to contribute into Kubernetes
        </p>
      </div>
    )
  }
}

export default Bio
