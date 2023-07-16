from pymongo import MongoClient
from bson.code import Code



def drop_collections():
    client = MongoClient("mongodb://admin:password@localhost:27017")
    db = client['tutorial']

    db['distinctWordPairs'].drop()
    db['distinctWordTriplets'].drop()
    db['distinctWords'].drop()


def aggregate_words():
    client = MongoClient("mongodb://admin:password@localhost:27017")
    db = client['tutorial']

    collection_name = 'pages'  # Replace with your actual collection name

    pipeline = [
                    {"$project": {"words": {"$split": ["$body", " "]}}},
                    {"$unwind": "$words"},
                    {"$group": {"_id": "$words", "count": {"$sum": 1}}},
                    {"$out": "distinctWords"}
               ]

    cursor = db[collection_name].aggregate(pipeline)
#    for document in cursor:
#        print(document)
#    print(cursor)


def aggregate_word_pairs():
    client = MongoClient("mongodb://admin:password@localhost:27017")
    db = client['tutorial']

    collection_name = 'pages'  # Replace with your actual collection name

    pipeline = [
        {
            "$project": {
                "wordPairs": {
                    "$function": {
                        "body": '''
                            function(data) {
                                var pairs = [];
                                for (var i = 0; i < data.length - 1; i++) {
                                    var x = (data[i] + " " + data[i + 1]).trim()
                                    x = x.replace(/\s+/g, ' '); // Replace multiple spaces with a single space
                                    pairs.push(x);
                                }
                                return pairs;
                            }
                        ''',
                        "args": [{"$split": ["$body", " "]}],
                        "lang": "js"
                    }
                }
            }
        },
        {"$unwind": "$wordPairs"},
        {"$group": {"_id": "$wordPairs", "count": {"$sum": 1}}},
        {"$out": "distinctWordPairs"}
    ]

    db[collection_name].aggregate(pipeline)

def aggregate_word_triplets():
    client = MongoClient("mongodb://admin:password@localhost:27017")
    db = client['tutorial']

    collection_name = 'pages'  # Replace with your actual collection name

    pipeline = [
        {
            "$project": {
                "wordTriplets": {
                    "$function": {
                        "body": '''
                            function(data) {
                                var triplets = [];
                                for (var i = 0; i < data.length - 2; i++) {
                                    var x = (data[i] + " " + data[i + 1] + " " + data[i + 2]).trim()
                                    x = x.replace(/\s+/g, ' '); // Replace multiple spaces with a single space
                                    triplets.push(x);
                                }
                                return triplets;
                            }
                        ''',
                        "args": [{"$split": ["$body", " "]}],
                        "lang": "js"
                    }
                }
            }
        },
        {"$unwind": "$wordTriplets"},
        {"$group": {"_id": "$wordTriplets", "count": {"$sum": 1}}},
        {"$out": "distinctWordTriplets"}
    ]

    db[collection_name].aggregate(pipeline)


def combine_collections():
    client = MongoClient("mongodb://admin:password@localhost:27017")
    db = client['tutorial']

    # Collection names to be combined
    collection1 = 'distinctWords'
    collection2 = 'distinctWordPairs'
    collection3 = 'distinctWordTriplets'

    combined_collection = 'combinedWordsPairs'  # The combined collection

    # Copy the first collection to the combined collection
    pipeline1 = [
        {
            "$merge": {
                "into": combined_collection
            }
        }
    ]
    db[collection1].aggregate(pipeline1)

    # Merge the second collection into the combined collection
    pipeline2 = [
        {
            "$merge": {
                "into": combined_collection,
                "whenMatched": "merge",
                "whenNotMatched": "insert"
            }
        }
    ]
    db[collection2].aggregate(pipeline2)

    # Merge the second collection into the combined collection
    pipeline3 = [
        {
            "$merge": {
                "into": combined_collection,
                "whenMatched": "merge",
                "whenNotMatched": "insert"
            }
        }
    ]
    db[collection3].aggregate(pipeline3)


if __name__ == "__main__":
    drop_collections()
    aggregate_words()
    aggregate_word_pairs()
    aggregate_word_triplets()
    combine_collections()


