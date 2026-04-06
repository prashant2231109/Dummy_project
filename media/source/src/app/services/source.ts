import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CompanyModel, CompanyResponse, SourceResponse } from '../models/source';

@Injectable({
  providedIn: 'root',
})
export class SourceService {

  private apiUrl = 'http://127.0.0.1:8000/source/drf/viewsets/';
  private companyUrl = 'http://127.0.0.1:8000/company/drf/list/';

  constructor(private http: HttpClient) {}

 
//  getCompanies() : Observable<any> {
//   return this.http.get('http://127.0.0.1:8000/company/drf/list/', {
//     withCredentials: true   
//   });
// }

 getCompanies() {
  return this.http.get(this.companyUrl, {
    withCredentials: true   
  });
}

 getSources(page: number = 1, query: string = ''): Observable<SourceResponse> {
  return this.http.get<SourceResponse>(
    `${this.apiUrl}?page=${page}&search=${query}`
  );
}

 


  addSource(data: any) {
    return this.http.post(this.apiUrl, data, {
      withCredentials: true
    });
  }

 deleteSource(id: number) {
    return this.http.delete(`${this.apiUrl}${id}/`, {
      withCredentials: true
    });
  }

 updateSource(id: number, data: any) {
    return this.http.put(`${this.apiUrl}${id}/`, data, {
      withCredentials: true
    });
  }
}






