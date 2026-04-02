export interface SourceModel {
  id: number;
  name: string;
  url: string;
  tagged_companies_data: {
    id: number;
    name: string;
  }[];
}


export interface SourceResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: SourceModel[];
}

export interface CompanyModel {
  id: number;
  name: string;
}
