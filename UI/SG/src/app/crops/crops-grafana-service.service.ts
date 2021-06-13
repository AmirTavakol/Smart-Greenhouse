import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { MessageService } from '../message.service';
import { ICrop } from '../crops/crop';
@Injectable({
  providedIn: 'root'
})
export class CropsGrafanaService {

  private backendAPI = "http://80.210.98.95:1628";
  constructor(private http: HttpClient,
    private messageService: MessageService) { }

    /** Log a HeroService message with the MessageService */
    private log(message: string) {
      this.messageService.add(`CropsService: ${message}`);
  }

  private handleError<T>(operation = 'operation', result?: T) {
      return (error: any): Observable<T> => {
    
        // TODO: send the error to remote logging infrastructure
        console.error(error); // log to console instead
    
        // TODO: better job of transforming error for user consumption
        this.log(`${operation} failed: ${error.message}`);
    
        // Let the app keep running by returning an empty result.
        return of(result as T);
      };
    }

    //to get data
    getCropData(cropId:any): Observable<any>{
        let crops = {};
        let url = this.backendAPI + "/getCropData?cropId=" + cropId; 
        return this.http.get<any>(url).pipe(
            tap(_ => this.log('fetched crop data')),
            catchError(this.handleError<any>('getCropData'))
          );
        }
}
