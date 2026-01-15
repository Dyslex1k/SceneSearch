import { Routes, Route } from "react-router-dom";
import Home from "./routes/Home";
import DiscoverPrefabs from "./routes/DiscoverPrefabs";
import PrefabDetail from "./routes/PrefabDetail";

// 404 Error page component
function NotFound() {
  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>404</h1>
      <p>Page not found</p>
    </div>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/discover/prefabs" element={<DiscoverPrefabs />} />
      <Route path="/prefab/:id" element={<PrefabDetail />} />

      {/* Catch-all route for 404 errors */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
