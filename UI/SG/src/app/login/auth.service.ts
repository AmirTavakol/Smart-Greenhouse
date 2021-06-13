import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { HttpRequest } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';

@Injectable()

export class AuthService {

private _registerUrl = "http://localhost:3000/api/register";
private _loginUrl = "http://80.210.98.95:1628/login";

  constructor(private http: HttpClient) { }

  registerUser(user: any) {
    return this.http.post<any>(this._registerUrl, user)
  }
  loginUser(user: any) {
    return this.http.post<any>(this._loginUrl, user)
}

}
