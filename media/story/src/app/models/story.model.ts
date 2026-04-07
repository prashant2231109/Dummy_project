export interface SourceModel {
  id: number;
  name: string;
  url: string;
  tagged_companies_data: {
    id: number;
    name: string;
  }[];
  is_owner: boolean
  is_staff:boolean
}


export interface StoryModel {
  id: number;
  title: string;
  url: string;
  body_text: string;

  source: number;
  source_data: SourceModel;

  company_data: CompanyModel | null;
  tagged_companies_data: CompanyModel[];

  is_owner: boolean;
  is_staff: boolean;
}

export interface StoryResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: StoryModel[];
}


export interface StoryInput {
  title: string;
  url: string;
  body_text: string;
}

export interface CompanyModel {
  id: number;
  name: string;
}