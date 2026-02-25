# Qdrant Collection Configuration

## Create Collection
**Endpoint:** `PUT /collections/properties`

**Payload:**
```json
{
  "vectors": {
    "size": 1536,
    "distance": "Cosine"
  }
}
```
*(Note: Size 1536 is for text-embedding-3-small/large or text-embedding-ada-002)*

## Payload Schema
The following fields will be stored in the point payload for filtering and display:
- `tenant_id`: UUID (Keyword)
- `price`: Numeric
- `parish`: Keyword
- `bedrooms`: Integer
- `persona`: Keyword
- `competitiveness`: Keyword

## Recommended Indexes (Payload)
To ensure multi-tenant performance, create an index on `tenant_id`:

**Endpoint:** `POST /collections/properties/index`
```json
{
    "field_name": "tenant_id",
    "field_schema": "keyword"
}
```
