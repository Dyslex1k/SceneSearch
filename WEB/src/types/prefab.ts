export type UseCase =
  | "Worlds"
  | "Avatars"
  | "Osc";

export type Category =
  | "3D Models"
  | "Animations"
  | "Materials"
  | "Audio"
  | "Visual Effects"
  | "Particles"
  | "Tooling"
  | "Lighting"
  | "UI"
  | "Udon"
  | "Shaders";

export type LinkType =
  | "Gumroad"
  | "Booth"
  | "Jinxy"
  | "Github"
  | "Gitlab";

export type LicenceType =
  | "Open Source"
  | "Proprietary"
  | "Custom";

export interface ExternalLink {
  type: LinkType;
  url: string;
}

export interface Prefab {
  _id: string;
  name: string;
  description: string;
  content: string;
  use_cases: UseCase[];
  categories: Category[];
  external_links: ExternalLink[];
  licence_type: LicenceType;
  is_free: boolean;
  created_at: string;
  updated_at?: string | null;
}

export interface PrefabSearchResponse {
  total: number;
  results: Prefab[];
}
