import { type FormEvent, useState } from "react";
import { Link } from "react-router-dom";
import type { Prefab, PrefabSearchResponse } from "../types/prefab";

const API_BASE_URL = "http://localhost:8000";

export default function DiscoverPrefabs() {
  const [query, setQuery] = useState<string>("");
  const [results, setResults] = useState<Prefab[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const limit = 20;
  const offset = 0;

  async function searchPrefabs(searchQuery: string): Promise<void> {
    if (searchQuery.trim().length < 1) {
      console.warn("[DiscoverPrefabs] Search aborted: empty query");
      return;
    }

    console.log("[DiscoverPrefabs] Searching prefabs", {
      q: searchQuery,
      limit,
      offset,
    });

    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams({
        q: searchQuery,
        limit: String(limit),
        offset: String(offset),
      });

      const url = `${API_BASE_URL}/prefabs/search?${params.toString()}`;
      console.log("[DiscoverPrefabs] Request URL:", url);

      const response = await fetch(url, {
        headers: {
          accept: "application/json",
        },
      });

      if (!response.ok) {
        const body = await response.text();
        console.error("[DiscoverPrefabs] API error", {
          status: response.status,
          body,
        });
        throw new Error(`API error ${response.status}`);
      }

      const data: PrefabSearchResponse = await response.json();
      console.log("[DiscoverPrefabs] Response received:", data);

      setResults(data.results);
      setTotal(data.total);
    } catch (err) {
      console.error("[DiscoverPrefabs] Search failed:", err);
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    console.log("[DiscoverPrefabs] Submit search:", query);
    searchPrefabs(query);
  }

  return (
    <div>
      <h1>Discover Prefabs</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Search prefabs..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit" disabled={loading}>
          Search
        </button>
      </form>

      {loading && <p>Searching...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {!loading && results.length > 0 && (
        <>
          <p>{total} results found</p>

          <ul>
            {results.map((prefab) => (
              <li key={prefab._id}>
                <Link to={`/prefab/${prefab._id}`}>
                  <h3>{prefab.name}</h3>
                </Link>
                <p>{prefab.description}</p>
                <small>
                  {prefab.is_free ? "Free" : "Paid"} · {prefab.licence_type}
                </small>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}
