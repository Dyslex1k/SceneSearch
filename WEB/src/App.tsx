import { Routes, Route } from "react-router-dom";
import Home from "./routes/Home";
import DiscoverPrefabs from "./routes/DiscoverPrefabs";
import PrefabDetail from "./routes/PrefabDetail";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/discover/prefabs" element={<DiscoverPrefabs />} />
      <Route path="/prefab/:id" element={<PrefabDetail />} />
    </Routes>
  );
}
