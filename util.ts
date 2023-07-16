import * as mongodb from 'mongodb'

export const MONGODB_DATABASE = 'tutorial'
export const MONGODB_COLLECTION = 'pages'

const MONGODB_HOST = process.env.MONGODB_HOST!
const MONGODB_USER = process.env.MONGODB_USERNAME
const MONGODB_PASS = process.env.MONGODB_PASSWORD

export const mongoClient = new mongodb.MongoClient(MONGODB_HOST, {
  auth: {username: MONGODB_USER, password: MONGODB_PASS},
})

export interface User {
  userId: string
  fullName: string
  email: string
  avatar: string
  registeredAt: Date
  country: string
}

export interface Page {
  pageId: string
  title: string
  body: string
  comments: string
  labels: string
  editors: string
  fuzzy: string
  url: string
}

export interface Word {
  _id: string
  count: number
}

