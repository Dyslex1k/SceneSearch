import { useParams } from "react-router-dom";

export default function PrefabDetail() {
  const { id } = useParams();

  return (
    <div>
      <h1>Prefab Detail</h1>
      <p>Prefab ID: {id}</p>
    </div>
  );
}
