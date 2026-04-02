import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CompanyModel, SourceResponse } from '../models/source';

@Injectable({
  providedIn: 'root',
})
export class SourceService {

  private apiUrl = 'http://127.0.0.1:8000/source/drf/viewsets/';
  private companyUrl = 'http://127.0.0.1:8000/company/drf/list/';

  constructor(private http: HttpClient) {}

 
getCompanies(): Observable<CompanyModel> {
    return this.http.get<CompanyModel>(this.companyUrl, {
      withCredentials: true
    });
  }

  getSources(): Observable<SourceResponse> {
    return this.http.get<SourceResponse>(this.apiUrl);
  }

 deleteSource(id: number) {
    return this.http.delete(`${this.apiUrl}${id}/`, {
      withCredentials: true
    });
  }

}


