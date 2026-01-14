# Data Structure

## MongoDB Collections

### Prefabs
```json
{
    "_id": "ObjectID",
    "name": "Name of Prefab",
    "description": "Short Description of the prefab",

    "content": {
        "en": "Markdown of the content of the page in english"
    }

    "creator_id": "ObjectID of USER",

    "use_cases": ["Avatar", "World"],
    "categories": ["Physics"],
    "tags": ["physbones", "utility"],

    "external_links": [
        {
        "type": "gumroad",
        "url": "https://gumroad.com/l/physbones-toolkit"
        },
        {
        "type": "booth",
        "url": "https://booth.pm/en/items/123456"
        }
        {
        "type": "vcc",
        "url": "https://vpm.techanon.dev/index.json"
        }
    ],

    "status": "published",      // draft | published | archived
    "visibility": "public",      // public | unlisted | private


    "created_at": "2026-01-14T12:43:21Z",
    "updated_at": "2026-01-14T12:43:21Z",

    "ranking": {
        "quality_score": 0.52,
        "popularity_score": 0.07,
        "freshness_score": 1.0
    },

    "moderation": {
        "state": "approved",
        "reports": 0
    }
}
```

### Neo4J

#### Nodes
```
(:Prefab {
  id: "prefab_456",
  name: "Advanced PhysBones Toolkit"
})
```

```
(:UseCase { name: "Avatar" })
(:UseCase { name: "World" })
```

```
(:Category { name: "Physics" })
(:Category { name: "Animation" })
```

```
(:Tag { name: "physbones" })
(:Tag { name: "utility" })
```

```
(:Marketplace { name: "Gumroad" })
(:Marketplace { name: "Booth" })
```

```
(:User {
  id: "user_123",
  role: "Creator"
})
```

#### Relationships
**Declared (creator intent)**
```
(Prefab)-[:POPULAR_IN]->(UseCase)
(Prefab)-[:IN_CATEGORY]->(Category:Physics)
(Prefab)-[:HAS_TAG]->(Tag:physbones)
(Prefab)-[:AVAILABLE_ON]->(Marketplace:Gumroad)
```

**Observed (user behavior)**
```
(User:user_789)-[:CLICKED]->(Prefab)
(User:user_789)-[:FAVORITED]->(Prefab)
```

**Inferred (system-generated)**
```
(Prefab)-[:SIMILAR_TO { confidence: 0.81 }]->(Prefab)
(Prefab)-[:POPULAR_WITH]->(UseCase:Avatar)
```

#### Constraints
```
CREATE CONSTRAINT prefab_id IF NOT EXISTS
FOR (p:Prefab) REQUIRE p.id IS UNIQUE;

CREATE CONSTRAINT usecase_name IF NOT EXISTS
FOR (u:UseCase) REQUIRE u.name IS UNIQUE;

CREATE CONSTRAINT category_name IF NOT EXISTS
FOR (c:Category) REQUIRE c.name IS UNIQUE;

CREATE CONSTRAINT tag_name IF NOT EXISTS
FOR (t:Tag) REQUIRE t.name IS UNIQUE;

```

### Open Search
```json
{
    "prefab_id": "prefab_456",
    "name": "Advanced PhysBones Toolkit",
    "description": "A toolkit providing fine-grained control over PhysBones...",

    "use_cases": ["Avatar"],
    "categories": ["Physics"],
    "tags": ["physbones", "avatar", "utility"],

    "marketplaces": ["gumroad", "booth"],

    "score_quality": 0.52,
    "score_popularity": 0.07,
    "score_freshness": 1.0,

    "status": "published",
    "visibility": "public",

    "created_at": "2026-01-14T12:43:21Z"
}

```

### Redis
#### Rate limiting
```
key: rate:user:user_789
value: 14
ttl: 60s
```

#### Recent interactions
```
key: recent_clicks:prefab_456
value: 23
ttl: 5m
```

#### Search experiments / A-B tests
```
key: experiment:freshness_boost
value: enabled
ttl: 1h
```

### Interaction Events (Write-Only Log)
```json
{
    "_id": "event_987",
    "user_id": "user_789",
    "prefab_id": "prefab_456",
    "action": "clicked_external_link",
    "timestamp": "2026-01-14T13:01:02Z"
}
```

### Derived Ranking Signals (Computed, Not Authored)
```json
{
    "prefab_id": "prefab_456",

    "quality_signals": {
        "favorite_rate": 0.21,
        "report_rate": 0.0,
        "dwell_time_avg": 42.3
    },

    "popularity_signals": {
        "clicks_7d": 82,
        "unique_users_7d": 61
    },

    "final_scores": {
        "quality": 0.68,
        "popularity": 0.34,
        "freshness": 0.87
    }
}

```