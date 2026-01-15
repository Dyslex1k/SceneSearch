import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import ReactMarkdown from "react-markdown";

type PrefabDetailType = {
  _id: string;
  name: string;
  description: string;
  content: string;
  use_cases: string[];
  categories: string[];
  external_links?: { type: string; url: string }[];
  licence_type: string;
  is_free: boolean;
  creator_id: string;
  created_at: string;
  updated_at: string | null;
};

const API_BASE_URL = "http://localhost:8000";

export default function PrefabDetail() {
  const { id } = useParams<{ id: string }>();
  const [prefab, setPrefab] = useState<PrefabDetailType | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;

    const fetchPrefab = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${API_BASE_URL}/prefabs/${id}`, {
          headers: { accept: "application/json" },
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch prefab: ${response.status}`);
        }

        const data: PrefabDetailType = await response.json();
        setPrefab(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
      } finally {
        setLoading(false);
      }
    };

    fetchPrefab();
  }, [id]);

  if (loading)
    return <p className="text-gray-700 p-6">Loading prefab details...</p>;

  if (error)
    return <p className="text-red-600 p-6">Error: {error}</p>;

  if (!prefab) return <p className="text-gray-700 p-6">Prefab not found.</p>;

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">{prefab.name}</h1>
      <p className="text-gray-700 mb-4">{prefab.description}</p>

      <div className="flex flex-wrap gap-2 mb-4">
        {prefab.categories.map((cat) => (
          <span
            key={cat}
            className="bg-indigo-100 text-indigo-800 text-sm px-2 py-1 rounded-full"
          >
            {cat}
          </span>
        ))}
        {prefab.use_cases.map((uc) => (
          <span
            key={uc}
            className="bg-green-100 text-green-800 text-sm px-2 py-1 rounded-full"
          >
            {uc}
          </span>
        ))}
        <span
          className={`${
            prefab.is_free ? "bg-teal-100 text-teal-800" : "bg-red-100 text-red-800"
          } text-sm px-2 py-1 rounded-full`}
        >
          {prefab.is_free ? "Free" : "Paid"}
        </span>
      </div>

      <p className="text-gray-500 mb-4">
        Licence: <strong>{prefab.licence_type}</strong>
      </p>

      {prefab.external_links && prefab.external_links.length > 0 && (
        <div className="mb-4">
          <h2 className="font-semibold text-gray-800 mb-2">External Links:</h2>
          <ul className="list-disc list-inside">
            {prefab.external_links.map((link) => (
              <li key={link.url}>
                <a
                  href={link.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-indigo-600 hover:underline"
                >
                  {link.type}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}

      <ReactMarkdown
        components={{
          h1: ({ children }) => <h1 className="text-4xl font-bold mb-4 text-gray-900 dark:text-white">{children}</h1>,
          h2: ({ children }) => <h2 className="text-3xl font-semibold mb-3 text-gray-800 dark:text-gray-200">{children}</h2>,
          h3: ({ children }) => <h3 className="text-2xl font-medium mb-2 text-gray-800 dark:text-gray-200">{children}</h3>,
          p: ({ children }) => <p className="text-base mb-4 text-gray-700 dark:text-gray-300 leading-relaxed">{children}</p>,
          ul: ({ children }) => <ul className="list-disc list-inside mb-4 space-y-1 text-gray-700 dark:text-gray-300">{children}</ul>,
          ol: ({ children }) => <ol className="list-decimal list-inside mb-4 space-y-1 text-gray-700 dark:text-gray-300">{children}</ol>,
          li: ({ children }) => <li className="ml-4">{children}</li>,
          strong: ({ children }) => <strong className="font-semibold text-gray-900 dark:text-white">{children}</strong>,
          em: ({ children }) => <em className="italic text-gray-700 dark:text-gray-300">{children}</em>,
          code: ({ children }) => <code className="bg-gray-100 dark:bg-gray-800 px-1 py-0.5 rounded text-sm font-mono">{children}</code>,
          pre: ({ children }) => <pre className="bg-gray-100 dark:bg-gray-800 p-4 rounded overflow-x-auto mb-4">{children}</pre>,
        }}
      >
        {prefab.content}
      </ReactMarkdown>


      <p className="text-gray-400 mt-6 text-sm">
        Created at: {new Date(prefab.created_at).toLocaleString()}
      </p>
    </div>
  );
}
