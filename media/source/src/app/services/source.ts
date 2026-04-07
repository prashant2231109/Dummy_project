import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { CompanyModel,SourceModel, SourceResponse, SourceInput } from '../models/source';
import { catchError} from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class SourceService {

private apiUrl = 'http://127.0.0.1:8000/source/drf/viewsets/';
private companyUrl = 'http://127.0.0.1:8000/company/drf/list/';

constructor(private http: HttpClient) {}


private handleError<T>(operation = 'operation', result?: T, rethrow: boolean = false) {
  return (error: any): Observable<T> => {
    const errorMsg = error?.error?.message || error?.message || 'Unknown error';
    console.error(`${operation} failed: ${errorMsg}`);

   if (rethrow) {
      return throwError(() => error.error);
    }
    return of(result as T);
  };
}


getCompanies(): Observable<CompanyModel[]> {
  return this.http.get<CompanyModel[]>(this.companyUrl).pipe(
    catchError(this.handleError<CompanyModel[]>('getCompanies', []))
  );
}

getSources(page: number = 1, query: string = ''): Observable<SourceResponse> {
  return this.http.get<SourceResponse>(
    `${this.apiUrl}?page=${page}&search=${query}`
  ).pipe(
    catchError(this.handleError<SourceResponse>('getSources', {
      count: 0,
      next: null,
      previous: null,
      results: []
    }))
  );
}


 addSource(data: SourceInput): Observable<SourceModel> {
  return this.http.post<SourceModel>(this.apiUrl, data, {
   
  }).pipe(
    catchError(this.handleError<SourceModel>('addSource', undefined  , true)
  ));
}

deleteSource(id: number): Observable<void> {
  return this.http.delete(`${this.apiUrl}${id}/`, {

  }).pipe(
    catchError(this.handleError<any>('deleteSource'))
  );
}

updateSource(id: number, data: SourceInput): Observable<SourceModel> {
  return this.http.put<SourceModel>(`${this.apiUrl}${id}/`, data, {
  }).pipe(
    catchError(this.handleError<SourceModel>('updateSource', undefined  , true))
  );
}
}






