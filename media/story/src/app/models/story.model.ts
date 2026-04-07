export interface StoryModel {
  id: number;
  name: string;
  url: string;
  tagged_companies: Company[];
}

export interface Company {
  id: number;
  name: string;
}