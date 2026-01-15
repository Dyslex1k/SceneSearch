import { type FormEvent, useState } from "react";
import { Link } from "react-router-dom";
import type { Prefab, PrefabSearchResponse, UseCase, Category, LicenceType } from "../types/prefab";

const API_BASE_URL = "http://localhost:8000";

const USE_CASES: UseCase[] = ["Worlds", "Avatars", "Osc"];
const CATEGORIES: Category[] = [
  "3D Models",
  "Animations",
  "Materials",
  "Audio",
  "Visual Effects",
  "Particles",
  "Tooling",
  "Lighting",
  "UI",
  "Udon",
  "Shaders",
];
const LICENCES: LicenceType[] = ["Open Source", "Proprietary", "Custom"];

export default function DiscoverPrefabs() {
  const [query, setQuery] = useState<string>("");
  const [useCaseFilter, setUseCaseFilter] = useState<UseCase[]>([]);
  const [categoryFilter, setCategoryFilter] = useState<Category[]>([]);
  const [licenceFilter, setLicenceFilter] = useState<LicenceType | "">("");
  const [isFreeFilter, setIsFreeFilter] = useState<"" | "true" | "false">("");
  const [limit, setLimit] = useState<number>(20);
  const [offset, setOffset] = useState<number>(0);

  const [results, setResults] = useState<Prefab[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  async function searchPrefabs() {
    if (query.trim().length < 1) return;

    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams({
        q: query,
        limit: String(limit),
        offset: String(offset),
      });

      useCaseFilter.forEach((uc) => params.append("use_cases", uc));
      categoryFilter.forEach((cat) => params.append("categories", cat));
      if (licenceFilter) params.append("licence_type", licenceFilter);
      if (isFreeFilter) params.append("is_free", isFreeFilter);

      const url = `${API_BASE_URL}/prefabs/search?${params.toString()}`;
      const response = await fetch(url, { headers: { accept: "application/json" } });
      if (!response.ok) throw new Error(`API error ${response.status}`);

      const data: PrefabSearchResponse = await response.json();
      setResults(data.results);
      setTotal(data.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    searchPrefabs();
  }

  function toggleArrayItem<T>(arr: T[], item: T): T[] {
    return arr.includes(item) ? arr.filter((x) => x !== item) : [...arr, item];
  }

  return (
    <div className="max-w-7xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6 text-gray-900">Discover Prefabs</h1>

      <form
        onSubmit={handleSubmit}
        className="grid gap-4 mb-8 bg-white p-6 rounded-lg shadow-md"
      >
        <input
          type="text"
          placeholder="Search prefabs..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="border rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />

        {/* Use Cases */}
        <fieldset className="grid gap-2 border-t pt-4">
          <legend className="font-semibold">Use Cases</legend>
          <div className="flex flex-wrap gap-3">
            {USE_CASES.map((uc) => (
              <label key={uc} className="flex items-center gap-1">
                <input
                  type="checkbox"
                  checked={useCaseFilter.includes(uc)}
                  onChange={() =>
                    setUseCaseFilter(toggleArrayItem(useCaseFilter, uc))
                  }
                  className="w-4 h-4"
                />
                <span className="text-gray-700">{uc}</span>
              </label>
            ))}
          </div>
        </fieldset>

        {/* Categories */}
        <fieldset className="grid gap-2 border-t pt-4">
          <legend className="font-semibold">Categories</legend>
          <div className="flex flex-wrap gap-3">
            {CATEGORIES.map((cat) => (
              <label key={cat} className="flex items-center gap-1">
                <input
                  type="checkbox"
                  checked={categoryFilter.includes(cat)}
                  onChange={() =>
                    setCategoryFilter(toggleArrayItem(categoryFilter, cat))
                  }
                  className="w-4 h-4"
                />
                <span className="text-gray-700">{cat}</span>
              </label>
            ))}
          </div>
        </fieldset>

        {/* Filters */}
        <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-4 pt-4">
          <select
            value={licenceFilter}
            onChange={(e) =>
              setLicenceFilter(e.target.value as LicenceType | "")
            }
            className="border rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="">All Licences</option>
            {LICENCES.map((lic) => (
              <option key={lic} value={lic}>
                {lic}
              </option>
            ))}
          </select>

          <select
            value={isFreeFilter}
            onChange={(e) =>
              setIsFreeFilter(e.target.value as "" | "true" | "false")
            }
            className="border rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="">All</option>
            <option value="true">Free</option>
            <option value="false">Paid</option>
          </select>

          <input
            type="number"
            placeholder="Limit"
            min={1}
            value={limit}
            onChange={(e) => setLimit(Number(e.target.value))}
            className="border rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />

          <input
            type="number"
            placeholder="Offset"
            min={0}
            value={offset}
            onChange={(e) => setOffset(Number(e.target.value))}
            className="border rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="bg-indigo-600 text-white font-semibold py-2 px-4 rounded-md hover:bg-indigo-700 disabled:opacity-50"
        >
          {loading ? "Searching..." : "Search"}
        </button>

        {error && <p className="text-red-600">{error}</p>}
      </form>

      {/* Results */}
      {results.length > 0 && (
        <>
          <p className="mb-4 text-gray-700">{total} results found</p>
          <ul className="grid gap-6">
            {results.map((prefab) => (
              <li
                key={prefab._id} // ✅ Use API id to fix React key warning
                className="bg-white p-4 rounded-lg shadow hover:shadow-lg transition-shadow"
              >
                <Link to={`/prefab/${prefab._id}`} className="hover:underline">
                  <h3 className="text-xl font-semibold text-gray-900">
                    {prefab.name}
                  </h3>
                </Link>
                <p className="text-gray-700 mt-1">{prefab.description}</p>
                <small className="text-gray-500 mt-2 block text-sm">
                  {prefab.is_free ? "Free" : "Paid"} · {prefab.licence_type} ·{" "}
                  {prefab.categories.join(", ")} · {prefab.use_cases.join(", ")}
                </small>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}
