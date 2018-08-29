import React from 'react'
import Helmet from 'react-helmet'
import Link from 'gatsby-link'

import Bio from '../components/Bio'
import { rhythm, scale } from '../utils/typography'

class BlogPostTemplate extends React.Component {
  render() {
    const post = this.props.data.markdownRemark
    const { previous, next } = this.props.pathContext

    const meta = [
      {property: 'og:title', content: post.frontmatter.title},
      {name: 'twitter:title', content: post.frontmatter.title},
    ]
    if (post.frontmatter.subtitle) {
      meta.push({name: 'description', content: post.frontmatter.subtitle})
      meta.push({name: 'twitter:description', content: post.frontmatter.subtitle})
      meta.push({property: 'og:description', content: post.frontmatter.subtitle})
    }
    if (post.frontmatter.shareImage) {
      const imageURL = this.props.data.site.siteMetadata.siteUrl + post.frontmatter.shareImage.childImageSharp.resize.src;
      meta.push({name: 'twitter:image', content: imageURL})
      meta.push({property: 'og:image', content: imageURL})
      meta.push({property: 'og:image:width', content: post.frontmatter.shareImage.childImageSharp.resize.width})
      meta.push({property: 'og:image:height', content: post.frontmatter.shareImage.childImageSharp.resize.height})
    }

    return (
      <div>
        <Helmet title={post.frontmatter.title} meta={meta} />
        <p
          style={{
            ...scale(-1 / 5),
            display: 'block',
            marginTop: rhythm(2),
            marginBottom: rhythm(-1.5),
          }}
        >
          {post.frontmatter.date}
        </p>
        <h1>{post.frontmatter.title}</h1>
        <h2 style={{
          ...scale(1 / 3),
          marginTop: rhythm(0),
        }}>
          {post.frontmatter.subtitle}
        </h2>

        <div dangerouslySetInnerHTML={{ __html: post.html }} />
        <hr
          style={{
            marginBottom: rhythm(1),
          }}
        />
        <Bio />

        <ul
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            justifyContent: 'space-between',
            listStyle: 'none',
            padding: 0,
          }}
        >
          <li>
            {
              previous &&
              <Link to={previous.fields.slug} rel="prev">
                ← {previous.frontmatter.title}
              </Link>
            }
          </li>
          <li>
            {
              next &&
              <Link to={next.fields.slug} rel="next">
                {next.frontmatter.title} →
              </Link>
            }
          </li>
        </ul>
      </div>
    )
  }
}

export default BlogPostTemplate

export const pageQuery = graphql`
  query BlogPostBySlug($slug: String!) {
    site {
      siteMetadata {
        siteUrl
      }
    }
    markdownRemark(fields: { slug: { eq: $slug } }) {
      id
      html
      frontmatter {
        title
        subtitle
        date(formatString: "ll")
        shareImage {
          childImageSharp {
            resize(width: 800) {
              width
              height
              src
            }
          }
        }
      }
    }
  }
`