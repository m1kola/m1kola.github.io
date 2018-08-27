import React from 'react'
import NotFoundGif from './404.gif'

const NotFoundPage = () => (
  <div>
    <h1>Not found</h1>
    <p>404. Nothing.</p>
    <div>
      <img src={NotFoundGif} alt='White noise'></img>
    </div>
  </div>
)

export default NotFoundPage
