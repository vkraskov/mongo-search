import express from 'express'
import {Filter} from 'mongodb'
import cors from 'cors'
import {mongoClient, MONGODB_COLLECTION} from './util'
import {User} from './util'
import {Page} from './util'
import {Word} from './util'

const app = express()

app.use(cors({credentials: true, origin: 'http://193.122.56.248:4000'}))

app.get('/search', async (req, res) => {
  const searchQuery = req.query.query as string
  const country = req.query.country as string

  if (!searchQuery || searchQuery.length < 2) {
    res.json([])
    return
  }

  const db = mongoClient.db('tutorial')
  const collection = db.collection<Page>(MONGODB_COLLECTION)

  const filter: Filter<Page> = {
    $text: {$search: searchQuery, $caseSensitive: false, $diacriticSensitive: false},
  }
  //if (country) filter.country = country

  const result = await collection
    .find(filter)
    .project({score: {$meta: 'textScore'}, _id: 0})
    .sort({score: {$meta: 'textScore'}})
    .limit(10)

  const array = await result.toArray()

  res.json(array)
})


app.get('/autocomplete', async (req, res) => {
  const searchQuery = req.query.query as string

  if (!searchQuery || searchQuery.length < 2) {
    res.json([])
    return
  }

  const db = mongoClient.db('tutorial')
  const collection = db.collection<Word>('combinedWordsPairs')

  const pipeline = [
    {
      $match: {
        _id: { $regex: "^" + searchQuery, $options: 'i' },
        count: { $gt: 1 }
      }
    },
    {
      $sort: { count: 1 } // -1 for descending order
    },
    {
      $limit: 10
    }
  ]

  const result = await collection.aggregate(pipeline).toArray()

  res.json(result)
})


async function main() {
  try {
    await mongoClient.connect()

    const db = mongoClient.db('tutorial')
    const collection = db.collection<User>(MONGODB_COLLECTION)

    // Text index for searching
    await collection.createIndexes([{name: 'ind_search_text', key: {title: 'text', body: 'text', comments: 'text', labels: 'text', editors: 'text', fuzzy: 'text'}}])

    app.listen(3000, () => console.log('http://localhost:3000/search?query=gilbert'))
  } catch (err) {
    console.log(err)
  }

  process.on('SIGTERM', async () => {
    await mongoClient.close()
    process.exit(0)
  })
}

main()
