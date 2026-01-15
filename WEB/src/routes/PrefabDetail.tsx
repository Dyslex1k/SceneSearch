import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import ReactMarkdown, { type Components } from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";

import "highlight.js/styles/github-dark.css";

type ExternalLink = {
  type: string;
  url: string;
};

type PrefabDetailType = {
  _id: string;
  name: string;
  description: string;
  content: string;
  use_cases: string[];
  categories: string[];
  external_links?: ExternalLink[];
  licence_type: string;
  is_free: boolean;
  creator_id: string;
  created_at: string;
  updated_at: string | null;
};

const API_BASE_URL = "http://localhost:8000";

const testMarkdown = `
\`\`\`json
{
  "test": "test"
}
\`\`\`
`;

/* ---------------- Markdown Components (Typed) ---------------- */

const markdownComponents: Components = {
  h1: ({ children }) => (
    <h1 className="text-4xl font-bold mb-4 text-gray-900 dark:text-white">
      {children}
    </h1>
  ),
  h2: ({ children }) => (
    <h2 className="text-3xl font-semibold mb-3 text-gray-800 dark:text-gray-200">
      {children}
    </h2>
  ),
  p: ({ children }) => (
    <p className="text-base mb-4 text-gray-700 dark:text-gray-300 leading-relaxed">
      {children}
    </p>
  ),

  pre: ({ children }) => (
    <pre className="bg-[#0d1117] text-gray-100 rounded-lg p-4 overflow-x-auto mb-6">
      {children}
    </pre>
  ),

  code({ className, children }) {
    return (
      <code
        className={`${className ?? ""} font-mono text-sm`}
      >
        {children}
      </code>
    );
  },
};


/* ---------------- Component ---------------- */

export default function PrefabDetail() {
  const { id } = useParams<{ id: string }>();
  const [prefab, setPrefab] = useState<PrefabDetailType | null>(null);
  const [loading, setLoading] = useState(true);
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
          throw new Error(`Failed to fetch prefab (${response.status})`);
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

  /* ---------------- UI States ---------------- */

  if (loading) {
    return <p className="p-6 text-gray-600">Loading prefab details…</p>;
  }

  if (error) {
    return <p className="p-6 text-red-600">Error: {error}</p>;
  }

  if (!prefab) {
    return <p className="p-6 text-gray-600">Prefab not found.</p>;
  }

  /* ---------------- Render ---------------- */

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white dark:bg-gray-900 rounded-lg shadow-md">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
        {prefab.name}
      </h1>

      <p className="text-gray-700 dark:text-gray-300 mb-4">
        {prefab.description}
      </p>

      {/* Tags */}
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
          className={`text-sm px-2 py-1 rounded-full ${
            prefab.is_free
              ? "bg-teal-100 text-teal-800"
              : "bg-red-100 text-red-800"
          }`}
        >
          {prefab.is_free ? "Free" : "Paid"}
        </span>
      </div>

      <p className="text-gray-500 mb-6">
        Licence: <strong>{prefab.licence_type}</strong>
      </p>

      {/* External Links */}
      {prefab.external_links?.length ? (
        <div className="mb-6">
          <h2 className="text-lg font-semibold mb-2">External Links</h2>
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
      ) : null}

      {/* Markdown Content */}
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeHighlight]}
        components={markdownComponents}
      >
        {prefab.content}
      </ReactMarkdown>

      <p className="text-gray-400 mt-8 text-sm">
        Created at: {new Date(prefab.created_at).toLocaleString()}
      </p>
    </div>
  );
}
